"""
BeamEmitterController.py
IX-Futakuchi-onna : Real-world analog/digital interface for harmonic beam emission
Author: Bryce Wooster
License: See LICENSE file in root directory

Description:
Takes a modulated waveform and outputs it through a physical emitter device,
such as a Tesla coil, laser diode, or RF amplifier, using either digital audio output
(DAC/I2S) or GPIO-based PWM modulation for experimental hardware integration.
"""

import numpy as np
import sounddevice as sd
import time


class BeamEmitterController:
    def __init__(self, sample_rate=44100, device=None):
        """
        Initializes audio output system.
        Use default sound output or specify external DAC device.
        """
        self.sample_rate = sample_rate
        self.device = device  # Optional: specific DAC or audio interface name

    def emit_waveform(self, waveform, gain=0.95):
        """
        Plays the waveform using analog audio output, usable for EM or Tesla driver injection.
        """
        if not isinstance(waveform, np.ndarray):
            raise TypeError("Waveform must be a NumPy array")

        # Apply output gain
        waveform_out = waveform * gain

        # Ensure output is in range -1 to +1 for DAC or audio system
        max_val = np.max(np.abs(waveform_out))
        if max_val > 1.0:
            waveform_out = waveform_out / max_val

        print("[INFO] Emitting waveform to hardware...")
        sd.play(waveform_out, samplerate=self.sample_rate, device=self.device)
        sd.wait()
        print("[INFO] Beam emission complete.")

    def emit_loop(self, waveform, repetitions=3, delay=0.5):
        """
        Repeat emission several times for field resonance or handshake simulation.
        """
        for i in range(repetitions):
            print(f"[INFO] Emission cycle {i + 1} of {repetitions}")
            self.emit_waveform(waveform)
            time.sleep(delay)


if __name__ == "__main__":
    from FieldModulator import FieldModulator

    harmonic_vector = {3: 0.8, 6: 0.4, 9: 0.2}
    modulator = FieldModulator(base_freq=111)
    waveform = modulator.modulate(harmonic_vector)

    emitter = BeamEmitterController()
    emitter.emit_loop(waveform, repetitions=2, delay=1.0)
