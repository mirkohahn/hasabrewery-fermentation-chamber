import sys
import os
import time
from smbus2 import SMBus
from PIL import Image, ImageDraw, ImageFont

# Ensure we can import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config  # Import config

I2C_ADDRESS = 0x3C  # Update with your actual display I2C address

def init_display():
    """Initialize the I2C OLED display."""
    try:
        bus = SMBus(1)
        bus.write_byte_data(I2C_ADDRESS, 0x00, 0xAE)  # Turn off display
        bus.write_byte_data(I2C_ADDRESS, 0x00, 0xAF)  # Turn on display
        bus.close()
        # print("✅ Display initialized.")
    except Exception as e:
        print(f"❌ Error initializing display: {e}")

def show_text(text):
    """Display text on the OLED screen."""
    width = 128
    height = 64

    # Create a blank image
    image = Image.new('1', (width, height), "black")
    draw = ImageDraw.Draw(image)

    # Load a basic font
    font = ImageFont.load_default()

    # Draw text in the center
    draw.text((10, 25), text, font=font, fill=255)

    # Send data to the OLED screen
    try:
        from luma.oled.device import ssd1306
        from luma.core.interface.serial import i2c
        from luma.core.render import canvas

        serial = i2c(port=1, address=I2C_ADDRESS)
        device = ssd1306(serial)

        with canvas(device) as draw:
            draw.text((10, 20), text, font=font, fill=255)

        # print(f"📟 Text displayed on OLED: {text}")

    except Exception as e:
        print(f"❌ Error displaying text: {e}")

def clear_display():
    """Clears the OLED display after initial message."""
    try:
        from luma.oled.device import ssd1306
        from luma.core.interface.serial import i2c
        from luma.core.render import canvas

        serial = i2c(port=1, address=I2C_ADDRESS)
        device = ssd1306(serial)

        with canvas(device) as draw:
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)  # Clear the screen

        # print("🧹 OLED display cleared.")

    except Exception as e:
        print(f"❌ Error clearing display: {e}")

if __name__ == "__main__":
    init_display()
    show_text(f"Welcome\nFirmware: {config.CONFIG['FIRMWARE_VERSION']}")
    time.sleep(5)  # Keep message for 5 seconds
    clear_display()
