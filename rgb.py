# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import colorsys

import board

import adafruit_tcs34725

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

sensor.integration_time = 200
sensor.gain = 16


def classify_color(color_rgb):
    r, g, b = (c / 255 for c in color_rgb)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hue = h * 360

    if v < 0.08:
        return "No color detected (too dim)"
    if s < 0.15:
        return "White detected" if v > 0.5 else "Gray/neutral detected"

    if hue < 15 or hue >= 345:
        return "Red detected"
    elif hue < 45:
        return "Orange detected"
    elif hue < 75:
        return "Yellow detected"
    elif hue < 170:
        return "Green detected"
    elif hue < 260:
        return "Blue detected"
    else:
        return "Purple/Pink detected"


while True:
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(f"RGB color as 8 bits per channel int: #{color:02X} or as 3-tuple: {color_rgb}")

    print(classify_color(color_rgb))

    temp = sensor.color_temperature
    lux = sensor.lux
    print(f"Temperature: {temp}K Lux: {lux}\n")
    time.sleep(1.0)