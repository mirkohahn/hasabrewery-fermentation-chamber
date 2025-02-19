#!/usr/bin/env python3

import RPi.GPIO as GPIO

# Hardcoded GPIO pin numbers (BCM numbering)
GPIO_LOW = 16   # This pin will be set to LOW
GPIO_HIGH = 5  # This pin will be set to HIGH

# Disable warnings about channels already in use
GPIO.setwarnings(False)

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Configure the pins as outputs
GPIO.setup(GPIO_LOW, GPIO.OUT)
GPIO.setup(GPIO_HIGH, GPIO.OUT)

# Set GPIO_LOW to LOW and GPIO_HIGH to HIGH
GPIO.output(GPIO_LOW, GPIO.LOW)
GPIO.output(GPIO_HIGH, GPIO.HIGH)
