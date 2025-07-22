"""
GankyilPhaseValidator.py
IX-Futakuchi-onna : Validates triple-phase Tesla/Gankyil waveform integrity via phase angle calculation
Author: Bryce Wooster
License: See LICENSE in project root

Description:
This module validates the relative phase offsets of three harmonic signals (X, Y, Z).
Used after waveform generation or transformation to confirm Gankyil symmetry is preserved.
Ideal for automated lab validation, transmission integrity checks, or signal tampering detection.
"""

import numpy as np

class GankyilPhaseValidator:
    def __init__(self, x_signal, y_signal, z_signal, sample_rate=44100):
        self.x = x_signal
        self.y = y_signal
        self.z = z_signal
        self.sample_rate = sample_rate
        self.N = len(x_signal)
        self.time = np.linspace(0, self.N / sample_rate, self.N, endpoint=False)

    def _calc_phase_offset(self, a, b):
        """
        Returns the average phase difference between two signals in degrees.
        """
        analytic_a = np.angle(np.fft.fft(a))
        analytic_b = np.angle(np.fft.fft(b))
        phase_diff = np.unwrap(analytic_b - analytic_a)
        avg_diff_deg = np.mean(np.rad2deg(phase_diff)) % 360
        return avg_diff_deg

    def validate(self):
        x_y = self._calc_phase_offset(self.x, self.y)
        y_z = self._calc_phase_offset(self.y, self.z)
        z_x = self._calc_phase_offset(self.z, self.x)

        print("[GANKYIL VALIDATOR]")
        print(f"X → Y phase diff: {x_y:.2f}°")
        print(f"Y → Z phase diff: {y_z:.2f}°")
        print(f"Z → X phase diff: {z_x:.2f}°")

        valid = all(
            abs(angle - 120) <= 10 for angle in [x_y, y_z, (360 - z_x) % 360]
        )

        print("✔️ Gankyil structure VALID" if valid else "❌ Gankyil structure BROKEN")
        return valid
