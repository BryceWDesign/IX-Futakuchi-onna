"""
HarmonicEncryptor.py
IX-Futakuchi-onna : Tesla-harmonic signature encryptor using pseudo-random harmonic displacement
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Encrypts a 3-6-9 harmonic signature vector by pseudo-randomly altering each harmonic’s
carrier frequency using a symmetric Gankyil-inspired frequency key.
The key must be known to the receiver to reverse the shift and decode the original message.
"""

import numpy as np
import hashlib


class HarmonicEncryptor:
    def __init__(self, encryption_key="IX369", max_offset_hz=12.0):
        self.key = encryption_key
        self.max_offset = max_offset_hz
        self.seed = self._generate_seed()

    def _generate_seed(self):
        """
        Hash the key into a reproducible seed using SHA-256.
        """
        digest = hashlib.sha256(self.key.encode()).digest()
        return int.from_bytes(digest[:4], 'big')  # 32-bit int

    def encrypt(self, harmonic_vector, base_freq):
        """
        Encrypt harmonic vector by shifting each frequency slightly
        based on the hashed encryption key.

        Inputs:
            harmonic_vector (dict): {3: amplitude, 6: amplitude, 9: amplitude}
            base_freq (float): Fundamental frequency
        Returns:
            encrypted_vector (list of tuples): [(freq1, amp1), (freq2, amp2), ...]
        """
        rng = np.random.RandomState(self.seed)
        encrypted_vector = []

        for harmonic, amp in harmonic_vector.items():
            base_hz = base_freq * harmonic
            offset = rng.uniform(-self.max_offset, self.max_offset)
            encrypted_freq = base_hz + offset
            encrypted_vector.append((encrypted_freq, amp))

        return encrypted_vector

    def decrypt(self, encrypted_vector, base_freq):
        """
        Reverse the encryption assuming the same key is used.

        Returns:
            decrypted_vector (dict): {harmonic: amplitude}
        """
        rng = np.random.RandomState(self.seed)
        decrypted_vector = {}

        for i, (enc_freq, amp) in enumerate(encrypted_vector):
            offset = rng.uniform(-self.max_offset, self.max_offset)
            true_freq = enc_freq - offset
            harmonic = int(round(true_freq / base_freq))
            decrypted_vector[harmonic] = amp

        return decrypted_vector


if __name__ == "__main__":
    # Example usage
    base_freq = 111
    harmonic_vector = {3: 0.8, 6: 0.5, 9: 0.3}

    encryptor = HarmonicEncryptor(encryption_key="GANKYIL-369")
    encrypted = encryptor.encrypt(harmonic_vector, base_freq)
    print("Encrypted Harmonics:")
    for freq, amp in encrypted:
        print(f"Freq: {freq:.2f} Hz | Amplitude: {amp:.2f}")

    decrypted = encryptor.decrypt(encrypted, base_freq)
    print("\nDecrypted Harmonics:")
    for h, a in decrypted.items():
        print(f"{h}x: {a:.2f}")
