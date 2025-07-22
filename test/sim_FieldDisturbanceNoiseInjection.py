"""
sim_FieldDisturbanceNoiseInjection.py
IX-Futakuchi-onna : Simulates EMI corruption in Tesla harmonic return loop
Author: Bryce Wooster
License: See LICENSE in root

Description:
Injects random Gaussian noise into the feedback signal to mimic external field interference.
Ensures the field lock logic can detect corrupted signals and prevent beam emission.
Validates real-world resilience against jamming, shielding failures, or signal spoofing attempts.
"""

import numpy as np
import matplotlib.pyplot as plt
from FieldResonanceDecoder import FieldResonanceDecoder
from BeamEmitterController import BeamEmitterController

def generate_noise_signal(duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    noise = np.random.normal(0, 0.5, size=t.shape)
    return t, noise

if __name__ == "__main__":
    print("[TEST] Injecting synthetic noise into field return channel...")

    decoder = FieldResonanceDecoder()
    t, noise_signal = generate_noise_signal()

    # Feed noise as if it were the return harmonic
    lock_status = decoder.validate_with_signal(noise_signal)

    if not lock_status:
        print("[PASS] Noise corrupted signal — lock correctly denied.")
    else:
        print("[FAIL] System falsely accepted interference — transmission risk detected.")

    # Visualization
    plt.plot(t, noise_signal, color='r', alpha=0.7)
    plt.title("Simulated EMI Noise Signal (Injected into Field Return)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    decoder.cleanup()
