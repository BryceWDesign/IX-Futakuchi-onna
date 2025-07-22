"""
generate_test_output_obfuscated.py
IX-Futakuchi-onna : Generates test waveform output used in system validation
Creates: test_output_obfuscated.wav
"""

import numpy as np
import soundfile as sf
from HarmonicEncryptor import HarmonicEncryptor
from FieldModulator import FieldModulator
from SignalObfuscator import SignalObfuscator

# Setup parameters
base_freq = 111
sample_rate = 44100
duration = 2.0  # seconds
harmonic_vector = {3: 0.9, 6: 0.6, 9: 0.4}
encryption_key = "IX369"
noise_key = "OBF-369"

# Step 1: Encrypt harmonics
encryptor = HarmonicEncryptor(encryption_key=encryption_key)
encrypted = encryptor.encrypt(harmonic_vector, base_freq=base_freq)
decrypted_vector = encryptor.decrypt(encrypted, base_freq=base_freq)

# Step 2: Modulate to waveform
modulator = FieldModulator(base_freq=base_freq, sample_rate=sample_rate, duration=duration)
waveform = modulator.modulate(decrypted_vector)

# Step 3: Obfuscate signal
obfuscator = SignalObfuscator(noise_key=noise_key, noise_strength=0.25)
obf_wave, _ = obfuscator.apply_noise(waveform)

# Step 4: Save to .wav
sf.write("test/test_output_obfuscated.wav", obf_wave, sample_rate)
print("✅ Generated test_output_obfuscated.wav")
