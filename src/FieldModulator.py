"""
FieldModulator.py
IX-Futakuchi-onna : Field-level beam modulator for Tesla-encoded harmonic vectors
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Transforms harmonic signature vectors into phase-locked, frequency-specific modulated fields.
Outputs amplitude-modulated waveforms for directional beam transmission hardware.
"""

import numpy as np


class FieldModulator:
    def __init__(self, base_freq=111, sample_rate=44100, duration=1.0):
        self.base_freq = base_freq  # Estimated from HarmonicEncoder
        self.sample_rate = sample_rate
        self.duration = duration

    def modulate(self, harmonic_vector):
        """
        Generates a modulated waveform from harmonic vector input.

        Input:
            harmonic_vector (dict): {3: amp1, 6: amp2, 9: amp3}
        Output:
            waveform (np.ndarray): Composite waveform ready for beam driver
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        waveform = np.zeros_like(t)

        for harmonic, amplitude in harmonic_vector.items():
            freq = self.base_freq * harmonic
            phase_shift = np.pi * (harmonic % 3)  # subtle variation: 0, pi, pi
            waveform += amplitude * np.sin(2 * np.pi * freq * t + phase_shift)

        # Normalize to prevent clipping
        max_val = np.max(np.abs(waveform))
        if max_val > 0:
            waveform = waveform / max_val

        return waveform


if __name__ == "__main__":
    # Example usage with test harmonic data
    harmonic_vector = {3: 0.8, 6: 0.4, 9: 0.2}
    modulator = FieldModulator(base_freq=111)
    output_waveform = modulator.modulate(harmonic_vector)

    import matplotlib.pyplot as plt
    plt.plot(output_waveform[:1000])  # Show first 1000 samples
    plt.title("Tesla-Encoded Modulated Field Waveform")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()
