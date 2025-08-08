from utils import setup_pin
# FOR OUTPUT PIN
led = setup_pin("LED", direction='out', initial_value=0)

# Toggle
led.toggle()

#FOR INPUT PIN
button = setup_pin(15, direction='in', pull='up')

if not button.value():
    print("Button is pressed")
#############
from utils import setup_pins
import time

pin_config = {
    "led": {
        "pin": "LED",
        "direction": "out",
        "initial_value": 0
    },
    "sensor_power": {
        "pin": 5,
        "direction": "out"
    },
    "button": {
        "pin": 15,
        "direction": "in",
        "pull": "up"
    }
}

pins = setup_pins(pin_config)

# Blink LED
for _ in range(5):
    pins["led"].toggle()
    time.sleep(0.5)

# Read button
if not pins["button"].value():
    print("Button pressed")

#######
from machine import ADC

solar_adc = ADC(27)  # assuming solar input is divided and connected to GPIO27

def read_solar_voltage():
    reading = solar_adc.read_u16()
    volts = (reading * 3.3 / 65535) * 2  # Adjust for voltage divider
    return round(volts, 2)

print("Solar Input Voltage:", read_solar_voltage(), "V")

########

from utils import read_battery_voltage, read_solar_voltage, is_charging
import time

while True:
    vbat = read_battery_voltage()
    vsolar = read_solar_voltage()
    charging = is_charging()

    print(f"Battery: {vbat:.2f} V | Solar: {vsolar:.2f} V | Charging: {'Yes' if charging else 'No'}")
    time.sleep(5)
###### Volateg to irradiance
from utils import solar_voltage_to_irradiance_ak50x50, read_solar_voltage

voltage = read_solar_voltage(adc_pin=27)  # ADC1 via voltage divider
irradiance = solar_voltage_to_irradiance_ak50x50(voltage)

print(f"Solar panel voltage: {voltage:.2f} V")
print(f"Estimated irradiance: {irradiance:.1f} W/m²")
