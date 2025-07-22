"""
FieldLockKeyGenerator.py
IX-Futakuchi-onna : Time-dependent harmonic key generator based on Tesla 3-6-9 logic
Author: Bryce Wooster
License: See LICENSE

Description:
Generates phase-based lock keys using Tesla's 3-6-9 numerical resonance method.
Used for authenticating field return signals and re-syncing receiver modules to emitter-side logic.

Ensures temporal lockstep with harmonic signature enforcement.
Supports secure handshakes in high-noise or adversarial environments.
"""

import numpy as np
import hashlib
import time

class FieldLockKeyGenerator:
    def __init__(self, entropy_salt="IX-Futakuchi-onna", time_window=1.0):
        self.entropy_salt = entropy_salt
        self.time_window = time_window  # seconds per cycle window

    def _harmonic_seed(self, t):
        """
        Generates harmonic pattern seed using Tesla’s 3-6-9 additive rule.
        """
        h = (3 * np.sin(6 * t) + 9 * np.cos(3 * t))
        return int(abs(h * 1000)) % 9999

    def _hash_key(self, harmonic_seed):
        """
        Converts harmonic seed into cryptographic SHA-256 key
        """
        base = f"{harmonic_seed}-{self.entropy_salt}"
        return hashlib.sha256(base.encode()).hexdigest()

    def generate_key(self):
        current_time = time.time()
        aligned_time = int(current_time // self.time_window) * self.time_window
        harmonic = self._harmonic_seed(aligned_time)
        return self._hash_key(harmonic)

    def verify_key(self, test_key):
        return test_key == self.generate_key()
