"""
sim_HarmonicSpectrumVisualizer.py
IX-Futakuchi-onna : Lab debug tool for spectrum analysis of harmonic waveform post-processing
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Performs FFT and spectrum analysis of a waveform to validate harmonic alignment,
encryption offsets, and obfuscation levels. Supports visual confirmation that 3x, 6x, 9x 
Tesla frequencies remain dominant or properly masked depending on stage.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import hann
import soundfile as sf


def analyze_waveform(waveform, sample_rate=44100, title="Harmonic Spectrum"):
    window = hann(len(waveform))
    windowed = waveform * window
    spectrum = np.abs(fft(windowed))
    freqs = np.fft.fftfreq(len(waveform), d=1.0 / sample_rate)

    # Only positive frequencies
    mask = freqs > 0
    freqs = freqs[mask]
    spectrum = spectrum[mask]

    plt.figure(figsize=(12, 6))
    plt.plot(freqs, spectrum, color='cyan', linewidth=1.0)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Highlight Tesla harmonics
    base_freq = 111
    for mult in [3, 6, 9]:
        f = base_freq * mult
        plt.axvline(x=f, color='red', linestyle='--', label=f"{mult}x ({f} Hz)")

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load waveform output from prior pipeline stage (e.g., obfuscated waveform)
    path = "test/test_output_obfuscated.wav"
    waveform, sr = sf.read(path)

    if waveform.ndim > 1:
        waveform = waveform[:, 0]  # Use first channel if stereo

    analyze_waveform(waveform, sample_rate=sr, title="Spectrum of Obfuscated Tesla Harmonic Waveform")
