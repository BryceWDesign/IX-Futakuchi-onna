"""
sim_DecodeNoiseInjected.py
IX-Futakuchi-onna : Tests decoding of harmonic field signal with injected EM noise
Author: Bryce Wooster
License: See LICENSE

Purpose:
Simulates realistic noise (thermal, RF interference, quantization error)
and verifies if FieldUnlockDecoder can still reconstruct the correct signal pattern.
"""

import numpy as np
import matplotlib.pyplot as plt

from SignalObfuscator_v2 import SignalObfuscatorV2
from FieldUnlockDecoder import FieldUnlockDecoder

def generate_clean_signal(duration=1.0, freq=440, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def add_noise(signal, noise_level=0.1):
    noise = np.random.normal(0, noise_level, len(signal))
    return signal + noise

if __name__ == "__main__":
    print("[TEST] Decoding harmonic signal with environmental noise...")

    # Step 1: Generate base "hello" waveform
    original = generate_clean_signal()

    # Step 2: Obfuscate it (as done in real-world transmission)
    obfuscator = SignalObfuscatorV2(seed=42)
    obfuscated = obfuscator.obfuscate(original)

    # Step 3: Simulate transmission through noisy environment
    noisy_signal = add_noise(obfuscated, noise_level=0.15)

    # Step 4: Attempt to decode it
    decoder = FieldUnlockDecoder(known_seed=42)
    decoded = decoder.decode(noisy_signal)

    # Step 5: Visual check
    plt.figure(figsize=(10, 4))
    plt.plot(decoded[:1000], label="Decoded w/ Noise", alpha=0.9)
    plt.plot(original[:1000], label="Original Signal", alpha=0.6)
    plt.title("Decoding Accuracy Under EM Interference")
    plt.legend()
    plt.tight_layout()
    plt.show()
