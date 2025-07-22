"""
HarmonicEncoder.py
IX-Futakuchi-onna : Tesla-style harmonic signature generator
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Converts analog waveform (e.g. voice or tone signal) into a Tesla-encoded harmonic signature using
3x, 6x, and 9x harmonic extraction. Output is a frequency-domain vector prepared for field modulation.
"""

import numpy as np
from scipy.fftpack import fft
from scipy.signal import hann


class HarmonicEncoder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.target_harmonics = [3, 6, 9]  # Base Tesla harmonics

    def encode(self, waveform):
        """
        Main encoding function.
        Input:
            waveform (np.ndarray) - 1D array of time-domain samples (normalized)
        Output:
            harmonic_vector (dict) - {harmonic_multiple: amplitude}
        """
        if not isinstance(waveform, np.ndarray):
            raise TypeError("Waveform must be a NumPy array")

        window = hann(len(waveform))
        windowed = waveform * window
        spectrum = np.abs(fft(windowed))
        freqs = np.fft.fftfreq(len(waveform), 1.0 / self.sample_rate)

        # Only take positive frequencies
        mask = freqs > 0
        freqs = freqs[mask]
        spectrum = spectrum[mask]

        base_freq = self._estimate_fundamental(freqs, spectrum)
        harmonic_vector = {}

        for multiplier in self.target_harmonics:
            harmonic_freq = base_freq * multiplier
            idx = (np.abs(freqs - harmonic_freq)).argmin()
            harmonic_vector[multiplier] = spectrum[idx]

        return harmonic_vector

    def _estimate_fundamental(self, freqs, spectrum):
        """
        Estimate fundamental frequency by detecting peak in lower frequency band.
        """
        low_band = (freqs < 1000)  # Focus on speech-relevant band
        low_freqs = freqs[low_band]
        low_spectrum = spectrum[low_band]
        fundamental_idx = np.argmax(low_spectrum)
        return low_freqs[fundamental_idx]


if __name__ == "__main__":
    # Example usage
    import soundfile as sf
    import matplotlib.pyplot as plt

    # Load WAV file
    waveform, sr = sf.read("test_hello.wav")
    encoder = HarmonicEncoder(sample_rate=sr)
    output = encoder.encode(waveform)

    print("Harmonic Signature Output:")
    for harmonic, amplitude in output.items():
        print(f"{harmonic}x: {amplitude:.3f}")

    # Optional: visualize spectrum
    plt.title("Harmonic Signature")
    plt.bar([f"{k}x]()
