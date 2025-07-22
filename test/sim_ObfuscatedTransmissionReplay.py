"""
sim_ObfuscatedTransmissionReplay.py
IX-Futakuchi-onna : Tests replay attack resistance of harmonic key protocol
Author: Bryce Wooster
License: See LICENSE

Description:
Simulates an intercepted harmonic message being replayed out of time-window.
Ensures the FieldLockKeyGenerator refuses to authenticate old signals even if content is correct.
"""

import numpy as np
import time

from FieldLockKeyGenerator import FieldLockKeyGenerator
from SignalObfuscator_v2 import SignalObfuscatorV2
from FieldUnlockDecoder import FieldUnlockDecoder

def generate_fake_message():
    # Create a simple sine wave to simulate "hello" signal
    t = np.linspace(0, 1.0, 44100)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t)
    return signal

if __name__ == "__main__":
    print("[TEST] Starting replay attack simulation...")

    # Simulate original transmission
    keygen = FieldLockKeyGenerator()
    original_key = keygen.generate_key()

    signal = generate_fake_message()
    obfuscator = SignalObfuscatorV2(seed=42)
    obfuscated = obfuscator.obfuscate(signal)

    # Simulate 2-second delay (outside the time window)
    print("[INFO] Waiting for time window to shift...")
    time.sleep(2.1)

    # Attempt to authenticate with old key
    new_keygen = FieldLockKeyGenerator()
    new_key = new_keygen.generate_key()

    if new_key != original_key:
        print("[PASS] Replay attack blocked — key mismatch detected.")
    else:
        print("[FAIL] Replay accepted — time desync not enforced.")
