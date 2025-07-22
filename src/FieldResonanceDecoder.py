"""
FieldResonanceDecoder.py
IX-Futakuchi-onna : Tesla field resonance feedback decoder for hardware-integrated lock validation
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Interfaces with the field resonance sensor hardware described in FieldResonanceSensor.md.
Reads GPIO or ADC input and confirms Tesla-harmonic presence (3x, 6x, 9x).
Used as the software decoder that grants or denies secure transmission continuation.
"""

import time

try:
    import RPi.GPIO as GPIO  # Raspberry Pi
    import spidev  # If using MCP3008 for ADC
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False


class FieldResonanceDecoder:
    def __init__(self, gpio_pin=17, adc_channel=None, adc_vref=3.3):
        self.gpio_pin = gpio_pin
        self.adc_channel = adc_channel
        self.adc_vref = adc_vref

        if HAS_HARDWARE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.IN)

            if self.adc_channel is not None:
                self.spi = spidev.SpiDev()
                self.spi.open(0, 0)
                self.spi.max_speed_hz = 1350000

    def read_gpio_lock(self):
        """
        Reads simple GPIO pin for HIGH/LOW lock indication from hardware sensor.
        """
        if not HAS_HARDWARE:
            print("[MOCK] Simulating GPIO lock: returning True")
            return True  # Simulated pass

        state = GPIO.input(self.gpio_pin)
        print(f"[GPIO] Field lock state: {state}")
        return state == GPIO.HIGH

    def read_adc_voltage(self):
        """
        Optional: reads voltage level from ADC (MCP3008) on specified channel.
        """
        if not HAS_HARDWARE or self.adc_channel is None:
            return 0.0

        adc = self.spi.xfer2([1, (8 + self.adc_channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        voltage = (data * self.adc_vref) / 1023.0
        print(f"[ADC] Voltage reading: {voltage:.2f} V")
        return voltage

    def cleanup(self):
        if HAS_HARDWARE:
            GPIO.cleanup()


if __name__ == "__main__":
    decoder = FieldResonanceDecoder()
    locked = decoder.read_gpio_lock()

    if locked:
        print("[LOCK] Field resonance confirmed. Beam transmission permitted.")
    else:
        print("[BLOCKED] No field lock detected. Transmission aborted.")

    decoder.cleanup()
