"""
TransmissionOrchestrator.py
IX-Futakuchi-onna : System-level controller for full harmonic transmission pipeline
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
This orchestrates the full harmonic messaging chain:
 1. Accept analog signal
 2. Encode 3/6/9 harmonics
 3. Encrypt harmonic vector
 4. Modulate to waveform
 5. Apply entropy masking
 6. Emit waveform via hardware
 7. Listen for Tesla handshake feedback
"""

from HarmonicEncoder import HarmonicEncoder
from HarmonicEncryptor import HarmonicEncryptor
from FieldModulator import FieldModulator
from SignalObfuscator import SignalObfuscator
from BeamEmitterController import BeamEmitterController
from FeedbackLockMonitor import FeedbackLockMonitor
import soundfile as sf


class TransmissionOrchestrator:
    def __init__(self,
                 base_freq=111,
                 encryption_key="IX369",
                 noise_key="OBF-369",
                 sample_rate=44100):
        self.base_freq = base_freq
        self.encoder = HarmonicEncoder(sample_rate=sample_rate)
        self.encryptor = HarmonicEncryptor(encryption_key=encryption_key)
        self.modulator = FieldModulator(base_freq=base_freq, sample_rate=sample_rate)
        self.obfuscator = SignalObfuscator(noise_key=noise_key)
        self.emitter = BeamEmitterController(sample_rate=sample_rate)
        self.lock_monitor = FeedbackLockMonitor(sample_rate=sample_rate)
        self.sample_rate = sample_rate

    def transmit(self, wav_path, secure=True, require_lock=True):
        print(f"[START] Loading waveform: {wav_path}")
        waveform, sr = sf.read(wav_path)
        assert sr == self.sample_rate, "[ERROR] Sample rate mismatch."

        print("[STEP 1] Encoding harmonics...")
        harmonic_vector = self.encoder.encode(waveform)

        print("[STEP 2] Encrypting harmonic vector...")
        encrypted = self.encryptor.encrypt(harmonic_vector, base_freq=self.base_freq)

        print("[STEP 3] Modulating encrypted vector...")
        encrypted_dict = self.encryptor.decrypt(encrypted, base_freq=self.base_freq)
        modulated = self.modulator.modulate(encrypted_dict)

        if secure:
            print("[STEP 4] Applying signal obfuscation...")
            obfuscated, _ = self.obfuscator.apply_noise(modulated)
        else:
            obfuscated = modulated

        if require_lock:
            print("[STEP 5] Waiting for harmonic feedback...")
            if not self.lock_monitor.listen_for_feedback(base_freq=self.base_freq):
                print("[ABORTED] No valid field handshake received.")
                return
            else:
                print("[CONFIRMED] Feedback lock achieved.")

        print("[STEP 6] Emitting signal...")
        self.emitter.emit_waveform(obfuscated)
        print("[COMPLETE] Signal emission complete.")


if __name__ == "__main__":
    orchestrator = TransmissionOrchestrator()
    orchestrator.transmit("test_hello.wav", secure=True, require_lock=True)
