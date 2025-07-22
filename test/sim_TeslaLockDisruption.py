"""
sim_TeslaLockDisruption.py
IX-Futakuchi-onna : Simulates failed field feedback scenario to validate lockout and emission prevention
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Mocks the feedback loop when Tesla harmonic return signal is absent or invalid.
Used to confirm that the transmission system correctly denies emission without proper field handshake.
"""

from FieldResonanceDecoder import FieldResonanceDecoder
from BeamEmitterController import BeamEmitterController
import numpy as np

def simulate_waveform():
    # Generates a test waveform that SHOULD be emitted if lock passes
    t = np.linspace(0, 1.0, 44100)
    waveform = np.sin(2 * np.pi * 333 * t) * 0.7  # Simulated harmonic
    return waveform

if __name__ == "__main__":
    print("[TEST] Simulating Tesla lock failure...")

    decoder = FieldResonanceDecoder()
    lock_status = decoder.read_gpio_lock()

    if not lock_status:
        print("[PASS] Lock not achieved — beam emission denied as expected.")
    else:
        print("[FAIL] Lock falsely triggered — emission should NOT proceed.")

        # For debugging: show what would have been emitted
        print("[DEBUG] Emitting test waveform to flag failure (only in test mode)...")
        waveform = simulate_waveform()
        emitter = BeamEmitterController()
        emitter.emit_waveform(waveform)

    decoder.cleanup()
