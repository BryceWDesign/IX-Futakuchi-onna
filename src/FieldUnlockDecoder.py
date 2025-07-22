"""
FieldUnlockDecoder.py
IX-Futakuchi-onna : Decodes received obfuscated harmonic waveform into original beam pattern
Author: Bryce Wooster
License: See LICENSE in root

Description:
Applies inverse transformations to restore the original harmonic signal,
assuming it was scrambled via SignalObfuscatorV2 with known key properties.
Performs:
- Spectral de-smearing
- Phase de-scrambling
- Signal normalization

Use this on received field returns before downstream analysis or lock validation.
"""

import numpy as np

class FieldUnlockDecoder:
    def __init__(self, known_seed=None):
        if known_seed is not None:
            np.random.seed(known_seed)

    def _desmear_spectrum(self, signal, smear_strength=0.03):
        """
        Applies inverse smear logic — assumes known smear parameters.
        """
        fft = np.fft.fft(signal)
        spectrum = np.abs(fft)
        phase = np.angle(fft)

        smear = np.random.normal(1.0, smear_strength, size=spectrum.shape)
        corrected_fft = (spectrum / smear) * np.exp(1j * phase)
        return np.real(np.fft.ifft(corrected_fft))

    def _descramble_phase(self, signal, block_size=1024):
        """
        Applies reverse phase alignment assuming known uniform shifts.
        """
        num_blocks = len(signal) // block_size
        restored = np.zeros_like(signal)

        for i in range(num_blocks):
            block = signal[i * block_size:(i + 1) * block_size]
            phase_shift = np.random.uniform(-np.pi, np.pi)
            restored[i * block_size:(i + 1) * block_size] = block / np.cos(phase_shift)
        return restored

    def decode(self, signal):
        desmeared = self._desmear_spectrum(signal)
        restored = self._descramble_phase(desmeared)
        normalized = restored / np.max(np.abs(restored))
        return normalized
