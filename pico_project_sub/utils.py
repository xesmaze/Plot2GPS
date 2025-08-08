from machine import ADC, Pin

def read_battery_voltage(adc_pin=26, r1=100_000, r2=100_000):
    """
    Reads battery voltage via ADC with a voltage divider.

    Parameters:
        adc_pin (int): GPIO pin number used for voltage sensing (default=26)
        r1 (int): Resistance of the top resistor in ohms (connected to battery+)
        r2 (int): Resistance of the bottom resistor in ohms (connected to GND)

    Returns:
        float: Calculated battery voltage in volts.
    """
    adc = ADC(adc_pin)
    conversion_factor = 3.3 / 65535
    raw = adc.read_u16()
    measured = raw * conversion_factor

    # Correct for the voltage divider
    battery_voltage = measured * (r1 + r2) / r2

    return round(battery_voltage, 2)


def setup_pin(pin_number, direction='out', pull=None, initial_value=None):
    """
    Initializes and returns a Pin object with the specified configuration.

    Parameters:
        pin_number (int or str): The GPIO pin number or special label (e.g., "LED")
        direction (str): 'in' or 'out'. Default is 'out'.
        pull (str or None): 'up', 'down', or None. Only applies to input pins.
        initial_value (0 or 1 or None): Initial output value. Applies only to output pins.

    Returns:
        machine.Pin: Configured Pin object
    """
    # Map direction to machine.Pin constant
    mode = Pin.OUT if direction == 'out' else Pin.IN

    # Set pull resistor if applicable
    pull_arg = None
    if direction == 'in':
        if pull == 'up':
            pull_arg = Pin.PULL_UP
        elif pull == 'down':
            pull_arg = Pin.PULL_DOWN

    pin = Pin(pin_number, mode, pull_arg)

    if direction == 'out' and initial_value is not None:
        pin.value(initial_value)

    return pin

def setup_pins(config):
    """
    Batch-initializes pins from a configuration dictionary.

    Parameters:
        config (dict): Dictionary with keys as labels and values as dictionaries
                       of pin config (see below).

    Returns:
        dict: Dictionary of label → Pin object
    """
    pins = {}
    for label, params in config.items():
        pin_number = params.get('pin')
        direction = params.get('direction', 'out')
        pull = params.get('pull')
        initial_value = params.get('initial_value')
        pins[label] = setup_pin(pin_number, direction, pull, initial_value)
    return pins

def read_solar_voltage(adc_pin=27, r1=100_000, r2=100_000):
    """
    Reads solar panel voltage via voltage divider to an ADC pin.

    Parameters:
        adc_pin (int): GPIO ADC pin number connected to solar input divider
        r1 (int): Resistor R1 (solar+ to ADC)
        r2 (int): Resistor R2 (ADC to GND)

    Returns:
        float: Solar voltage in volts, rounded to 2 decimal places
    """
    adc = ADC(adc_pin)
    conversion_factor = 3.3 / 65535
    raw = adc.read_u16()
    measured = raw * conversion_factor
    solar_voltage = measured * (r1 + r2) / r2
    return round(solar_voltage, 2)

def is_charging(chrg_pin=14):
    """
    Detects if the battery is charging using TP4056 CHRG pin logic.

    Parameters:
        chrg_pin (int): GPIO pin connected to TP4056 CHRG (open-drain, active-low)

    Returns:
        bool: True if charging (CHRG pulled low), False otherwise
    """
    pin = Pin(chrg_pin, Pin.IN, Pin.PULL_UP)
    return pin.value() == 0  # Low = charging

### Solar voltage to irradiance
def solar_voltage_to_irradiance_ak50x50(voltage, full_sun_voc=2.0):
    """
    Estimate solar irradiance (W/m²) from AK50x50 solar cell voltage.

    Parameters:
        voltage (float): Measured open-circuit voltage of the solar cell
        full_sun_voc (float): Expected Voc under full sun (~2.0V typical for AK50x50)

    Returns:
        float: Estimated irradiance in W/m² (0–1000 scale)
    """
    if voltage <= 0:
        return 0.0

    # Cap at 1000 W/m² for full sun equivalent
    irradiance = (voltage / full_sun_voc) * 1000
    return round(min(irradiance, 1000.0), 1)
