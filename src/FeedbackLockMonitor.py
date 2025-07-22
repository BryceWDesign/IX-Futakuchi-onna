"""
FeedbackLockMonitor.py
IX-Futakuchi-onna : Real-time field handshake monitor to validate resonant feedback from authorized receiver
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
This module passively listens for field-based return signals in the Tesla 3-6-9 harmonic band.
If the expected feedback pattern is detected within a specified time window, it unlocks emitter continuation.
Otherwise, the transmission is terminated to prevent signal leakage.
"""

import numpy as np
import sounddevice as sd
from scipy.fft import fft
import time


class FeedbackLockMonitor:
    def __init__(self, sample_rate=44100, duration=1.0, target_harmonics=(3, 6, 9), lock_threshold=0.3):
        self.sample_rate = sample_rate
        self.duration = duration
        self.target_harmonics = target_harmonics
        self.lock_threshold = lock_threshold  # Amplitude threshold to consider feedback valid

    def listen_for_feedback(self, base_freq):
        """
        Listens to incoming field signal and performs spectral analysis
        to confirm harmonic lock response from paired device.
        """
        print("[INFO] Listening for Tesla harmonic handshake...")

        try:
            recording = sd.rec(int(self.sample_rate * self.duration),
                               samplerate=self.sample_rate,
                               channels=1,
                               dtype='float64')
            sd.wait()

            spectrum = np.abs(fft(recording[:, 0]))
            freqs = np.fft.fftfreq(len(spectrum), 1.0 / self.sample_rate)

            lock_confirmed = True
            for harmonic in self.target_harmonics:
                target_freq = base_freq * harmonic
                idx = np.argmin(np.abs(freqs - target_freq))
                amplitude = spectrum[idx]

                print(f"  Detected amplitude at {harmonic}x ({int(target_freq)} Hz): {amplitude:.3f}")
                if amplitude < self.lock_threshold:
