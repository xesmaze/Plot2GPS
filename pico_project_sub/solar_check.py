from machine import ADC
import time

def read_solar_voltage(adc_pin=27, r1=100_000, r2=100_000):
    adc = ADC(adc_pin)
    conversion_factor = 3.3 / 65535
    raw = adc.read_u16()
    measured = raw * conversion_factor
    voltage = measured * (r1 + r2) / r2
    return round(voltage, 2)

def solar_voltage_to_irradiance_ak50x50(voltage, full_sun_voc=2.0):
    if voltage <= 0:
        return 0.0
    irradiance = (voltage / full_sun_voc) * 1000
    return round(min(irradiance, 1000.0), 1)

while True:
    vsolar = read_solar_voltage()
    irradiance = solar_voltage_to_irradiance_ak50x50(vsolar)
    print(f"Solar: {vsolar:.2f} V | Irradiance: {irradiance:.1f} W/m²")
    time.sleep(5)
