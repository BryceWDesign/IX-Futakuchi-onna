"""
sim_GankyilOverlapTest.py
IX-Futakuchi-onna : Simulates phase-locked triple waveform generation using 3-6-9 Tesla/Gankyil logic
Author: Bryce Wooster
License: See LICENSE in project root

Description:
This test confirms the TeslaSignalEncoderV2 class produces phase-locked Gankyil waveforms.
Visualizes the 120-degree phase offset across three harmonic signals (X, Y, Z).
"""

import matplotlib.pyplot as plt
from TeslaSignalEncoder_v2 import TeslaSignalEncoderV2

if __name__ == "__main__":
    encoder = TeslaSignalEncoderV2()
    gankyil = encoder.generate_gankyil_triple()

    time = encoder.time

    # Plot each harmonic layer
    plt.figure(figsize=(12, 6))
    plt.plot(time, gankyil['X'], label='X Phase (0°)', linewidth=1)
    plt.plot(time, gankyil['Y'], label='Y Phase (120°)', linewidth=1)
    plt.plot(time, gankyil['Z'], label='Z Phase (240°)', linewidth=1)

    plt.title('Gankyil Triple-Phase Harmonic Signal (Tesla 3-6-9 Structure)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
