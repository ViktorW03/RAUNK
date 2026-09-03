# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time

import board

import adafruit_tcs34725

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_tcs34725.TCS34725(i2c)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
sensor.gain = 4


def classify_color(color_rgb):
    r, g, b = color_rgb
    brightness = (r + g + b) / 3
    spread = max(r, g, b) - min(r, g, b)

    if brightness < 15:
        return "No color detected (too dim)"
    if brightness > 200 and spread < 30:
        return "White detected"
    if spread < 20:
        return "Gray/neutral detected"
    if r > g * 1.2 and r > b * 1.2:
        return "Red detected"
    elif g > r * 1.2 and g > b * 1.2:
        return "Green detected"
    elif b > r * 1.2 and b > g * 1.2:
        return "Blue detected"
    else:
        return "Uncertain/mixed color"


# Main loop reading color and printing it every second.
while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(f"RGB color as 8 bits per channel int: #{color:02X} or as 3-tuple: {color_rgb}")

    print(classify_color(color_rgb))

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print(f"Temperature: {temp}K Lux: {lux}\n")
    # Delay for a second and repeat.
    time.sleep(1.0)