import csv
from statistics import mean
from time import sleep

from gpiozero import MCP3008

sensor = MCP3008(channel=0)

DISTANCES_CM = range(10, 151, 10)
SAMPLES_PER_STEP = 5
SAMPLE_DELAY_S = 0.2
OUTPUT_CSV = "distance_calibration.csv"


def read_voltage():
    return sensor.voltage


def main():
    readings = []

    for distance_cm in DISTANCES_CM:
        input(f"Place object at {distance_cm} cm, then press Enter...")

        samples = []
        for _ in range(SAMPLES_PER_STEP):
            samples.append(read_voltage())
            sleep(SAMPLE_DELAY_S)

        voltage = mean(samples)
        readings.append((distance_cm, voltage))
        print(f"  {distance_cm} cm -> {voltage:.3f} V")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["distance_cm", "voltage_v"])
        writer.writerows(readings)

    voltages_csv = ",".join(f"{v:.3f}" for _, v in readings)
    print(f"\nSaved {len(readings)} readings to {OUTPUT_CSV}")
    print(f"Voltages: {voltages_csv}")


if __name__ == "__main__":
    main()
