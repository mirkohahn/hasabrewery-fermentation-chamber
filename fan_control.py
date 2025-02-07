import subprocess
import config

def turn_fans_on():
    """Turns the fan on by enabling power on the specified USB port."""
    try:
        usb_port = config.CONFIG["FAN_USB_PORT_NO"]
        hub = "1-1"  # Adjust if necessary based on your system
        command = ["sudo", "uhubctl", "-a", "on", "-l", hub, "-p", str(usb_port)]
        subprocess.run(command, check=True)
        print(f"Fan turned ON at USB port {usb_port}.")
    except Exception as e:
        print(f"Error turning fan on: {e}")

def turn_fans_off():
    """Turns the fan off by disabling power on the specified USB port."""
    try:
        usb_port = config.CONFIG["FAN_USB_PORT_NO"]
        hub = "1-1"  # Adjust if necessary based on your system
        command = ["sudo", "uhubctl", "-a", "off", "-l", hub, "-p", str(usb_port)]
        subprocess.run(command, check=True)
        print(f"Fan turned OFF at USB port {usb_port}.")
    except Exception as e:
        print(f"Error turning fan off: {e}")

def get_fan_status():
    """Checks if the fan is on or off and returns 1 (on) or 0 (off)."""
    try:
        usb_port = config.CONFIG["FAN_USB_PORT_NO"]
        hub = "1-1"
        command = ["sudo", "uhubctl", "-l", hub, "-p", str(usb_port)]
        result = subprocess.run(command, capture_output=True, text=True)
        if "power" in result.stdout and "off" not in result.stdout:
            return 1  # Fan is ON
        return 0  # Fan is OFF
    except Exception as e:
        print(f"Error checking fan status: {e}")
        return 0

if __name__ == "__main__":
    # Example usage
    turn_fans_on()
    print(f"Fan status: {get_fan_status()}")
    input("Press Enter to turn the fan off...")
    turn_fans_off()
    print(f"Fan status: {get_fan_status()}")
