import mqtt_subscriber
import config
import relay_control
import fan_control


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9/5) + 32, 2)


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return round((fahrenheit - 32) * 5/9, 2)


# Global variables for holding temperature values
current_temp_brew = 0.0
current_temp_ambient = 0.0
current_temp_top = 0.0
current_temp_bottom = 0.0
goal_chamber_temperature = 0.0  # Dynamically calculated during the process

def get_stage_name():
    """Retrieve the current fermentation stage name from state.json."""
    state_data = mqtt_subscriber.load_persistent_data()
    return state_data.get("fermentation", {}).get("schedule", [{}])[0].get("stage", "Unknown")

def get_goal_brew_temp():
    """Retrieve goal brew temperature from state.json and convert if necessary."""
    state_data = mqtt_subscriber.load_persistent_data()
    fermentation_data = state_data.get("fermentation", {}).get("schedule", [{}])[0].get("temperature", {})

    goal_brew_temp_value = fermentation_data.get("value", 18)  # Default to 18°C if missing
    goal_brew_temp_unit = fermentation_data.get("unit", "Celsius")

    # Normalize unit names
    if goal_brew_temp_unit in ["°C", "C"]:
        goal_brew_temp_unit = "Celsius"
    elif goal_brew_temp_unit in ["°F", "F"]:
        goal_brew_temp_unit = "Fahrenheit"

    # Convert goal temperature if necessary
    if config.CONFIG.get("IMPERIAL_UNITS", False):
        return goal_brew_temp_value if goal_brew_temp_unit == "Fahrenheit" else celsius_to_fahrenheit(goal_brew_temp_value)
    return goal_brew_temp_value if goal_brew_temp_unit == "Celsius" else fahrenheit_to_celsius(goal_brew_temp_value)


def get_current_temperatures():
    """Return the stored global temperature values."""
    global current_temp_brew, current_temp_ambient, current_temp_top, current_temp_bottom
    return {
        "temp_brew": current_temp_brew,
        "temp_ambient": current_temp_ambient,
        "temp_top": current_temp_top,
        "temp_bottom": current_temp_bottom,
    }


def evaluate(temp_data):
    """Update global variables and determine control actions."""
    global current_temp_brew, current_temp_ambient, current_temp_top, current_temp_bottom, goal_chamber_temperature
    
    # Update global temperature variables
    current_temp_brew = temp_data["temp_brew"]
    current_temp_ambient = temp_data["temp_ambient"]
    current_temp_top = temp_data["temp_top"]
    current_temp_bottom = temp_data["temp_bottom"]

    # Retrieve goal brew temperature
    goal_brew_temp = get_goal_brew_temp()

    # Load config variables
    brew_temp_exceed = config.CONFIG["BREW_TEMP_EXCEED"]
    brew_temp_undershoot = config.CONFIG["BREW_TEMP_UNDERSHOOT"]
    chamber_temp_diff_max = config.CONFIG["CHAMBER_TEMP_DIFFERENCE_MAX"]
    chamber_temp_diff_min = config.CONFIG["CHAMBER_TEMP_DIFFERENCE_MIN"]
    min_chamber_temp = config.CONFIG["MINIMIM_CHAMBER_TEMP"]
    min_brew_temp = config.CONFIG["MINIMIM_BREW_TEMP"]
    chamber_temp_idle_range = config.CONFIG["CHAMBER_TEMP_IDLE_RANGE"]
    intensity_factor = config.CONFIG["INTENSITY_FACTOR"]

    # Calculate derived values
    chamber_temp_difference = current_temp_top - current_temp_bottom
    brew_temp_offset = current_temp_brew - goal_brew_temp
    chamber_temp = (current_temp_top + current_temp_bottom) / 2

    # Compute dynamic goal chamber temperature
    goal_chamber_temperature = goal_brew_temp + (brew_temp_offset * intensity_factor)

    # Debugging: Print all values
    # print(f"🌡️ Temperature Readings:")
    # print(f"   Ambient: {current_temp_ambient}°{'F' if config.CONFIG['IMPERIAL_UNITS'] else 'C'}")
    # print(f"   Top: {current_temp_top}°{'F' if config.CONFIG['IMPERIAL_UNITS'] else 'C'}")
    # print(f"   Bottom: {current_temp_bottom}°{'F' if config.CONFIG['IMPERIAL_UNITS'] else 'C'}")
    # print(f"   Brew: {current_temp_brew}°{'F' if config.CONFIG['IMPERIAL_UNITS'] else 'C'}")
    # print(f"   Goal Brew Temp: {goal_brew_temp}°{'F' if config.CONFIG['IMPERIAL_UNITS'] else 'C'}")

    # print("\n🔧 Configuration Variables:")
    # print(f"   BREW_TEMP_EXCEED: {brew_temp_exceed}°")
    # print(f"   BREW_TEMP_UNDERSHOOT: {brew_temp_undershoot}°")
    # print(f"   CHAMBER_TEMP_DIFFERENCE_MAX: {chamber_temp_diff_max}°")
    # print(f"   CHAMBER_TEMP_DIFFERENCE_MIN: {chamber_temp_diff_min}°")
    # print(f"   MINIMIM_CHAMBER_TEMP: {min_chamber_temp}°")
    # print(f"   MINIMIM_BREW_TEMP: {min_brew_temp}°")
    # print(f"   CHAMBER_TEMP_IDLE_RANGE: {chamber_temp_idle_range}°")
    # print(f"   INTENSITY_FACTOR: {intensity_factor}")

    # print("\n📊 Derived Calculations:")
    # print(f"   Chamber Temp Difference: {chamber_temp_difference}°")
    # print(f"   Brew Temp Offset: {brew_temp_offset}°")
    # print(f"   Chamber Temp: {chamber_temp}°")
    # print(f"   Goal Chamber Temp: {goal_chamber_temperature}°")

    # ✅ **New Logic Implementation**
    # 1️⃣ Emergency heating if too cold
    if chamber_temp <= min_chamber_temp or current_temp_brew <= min_brew_temp:
        relay_control.turn_heater_on()
        fan_control.turn_fans_on()

    # 2️⃣ Brew temperature control
    if current_temp_brew >= goal_brew_temp + brew_temp_exceed:
        relay_control.turn_cooler_on()
    if current_temp_brew <= goal_brew_temp - brew_temp_undershoot:
        relay_control.turn_heater_on()

    # 3️⃣ Dynamic chamber temperature control
    if chamber_temp > goal_chamber_temperature:
        relay_control.turn_heater_off()
    if chamber_temp >= goal_chamber_temperature + chamber_temp_idle_range:
        relay_control.turn_cooler_on()
    if chamber_temp < goal_chamber_temperature:
        relay_control.turn_cooler_off()
    if chamber_temp - chamber_temp_idle_range < goal_chamber_temperature:
        relay_control.turn_heater_on()

    # 4️⃣ Fan control based on chamber temperature difference
    if chamber_temp_difference >= chamber_temp_diff_max:
        fan_control.turn_fans_on()
    if chamber_temp_difference <= chamber_temp_diff_min:
        fan_control.turn_fans_off()

    # Return control status
    return {
        "heater": relay_control.get_relay_status("heater"),
        "cooler": relay_control.get_relay_status("cooler"),
        "fan": fan_control.get_fan_status(),
    }
