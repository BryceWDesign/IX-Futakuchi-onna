"""
SignalObfuscator.py
IX-Futakuchi-onna : Adds entropy-based field noise to beam signal for obfuscation; reversible with key
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
This module adds a controlled layer of pseudo-random spectral noise to an existing waveform
to make frequency analysis or signal reconstruction nearly impossible without the key.
Intended for pre-emission signal masking. Fully reversible for matched receivers.
"""

import numpy as np
import hashlib


class SignalObfuscator:
    def __init__(self, noise_key="OBF-369", noise_strength=0.2):
        """
        noise_strength: 0.0 to 1.0 — proportion of added noise relative to signal amplitude
        """
        self.key = noise_key
        self.noise_strength = noise_strength
        self.seed = self._generate_seed()

    def _generate_seed(self):
        digest = hashlib.sha256(self.key.encode()).digest()
        return int.from_bytes(digest[:4], 'big')

    def apply_noise(self, waveform):
        rng = np.random.RandomState(self.seed)
        noise = rng.normal(loc=0.0, scale=1.0, size=waveform.shape)
        noise = noise * self.noise_strength

        obfuscated = waveform + noise
        max_val = np.max(np.abs(obfuscated))
        if max_val > 1.0:
            obfuscated = obfuscated / max_val  # Prevent clipping

        return obfuscated, noise

    def remove_noise(self, obfuscated_waveform):
        rng = np.random.RandomState(self.seed)
        noise = rng.normal(loc=0.0, scale=1.0, size=obfuscated_waveform.shape)
        noise = noise * self.noise_strength

        restored = obfuscated_waveform - noise
        return restored


if __name__ == "__main__":
    # Demo test
    from FieldModulator import FieldModulator

    base_freq = 111
    harmonic_vector = {3: 0.7, 6: 0.5, 9: 0.3}
    modulator = FieldModulator(base_freq=base_freq)
    clean_wave = modulator.modulate(harmonic_vector)

    obfuscator = SignalObfuscator(noise_key="OBF-369", noise_strength=0.3)
    obf_wave, _ = obfuscator.apply_noise(clean_wave)

    restored_wave = obfuscator.remove_noise(obf_wave)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(clean_wave[:1000], label="Original")
    plt.plot(obf_wave[:1000], label="Obfuscated", alpha=0.6)
    plt.plot(restored_wave[:1000], label="Restored", linestyle='dashed')
    plt.title("Signal Obfuscation & Restoration")
    plt.legend()
    plt.grid(True)
    plt.show()
