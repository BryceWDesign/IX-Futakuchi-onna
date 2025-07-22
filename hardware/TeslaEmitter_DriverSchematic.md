# Tesla Emitter Driver Schematic

This document outlines the driver hardware required to interface the modulated waveform output from the digital domain (via DAC or PWM) to a real-world Tesla-style EM emitter, including:

---

## ⚡ Electrical Configuration

### Input:
- Source: DAC output from `BeamEmitterController.py` (0.0–1.0 float audio waveform)
- Interface: 3.5mm TRS, USB DAC, or PWM GPIO
- Voltage range: 0.5V – 1.8V peak

### Amplification Stage:
- Component: Class D Amplifier (e.g. TPA3116D2 or IRF540-based MOSFET H-bridge)
- Input impedance: ≥10kΩ
- Output voltage: up to 35V RMS (audio modulated)
- Power supply: 24V–36V DC regulated input (LiFePO4 or bench PSU)

### Transformer Interface:
- Isolation Transformer: 1:10 audio transformer for signal gain + protection
- Primary: Amp output
- Secondary: Resonant base coil driver

### Coil:
- Design: Tesla single-resonant air-core coil
- Resonant frequency: Tuned to base_freq × 3 (333 Hz nominal)
- Topload: Toroidal capacitor or spherical terminal for field shaping
- Return path: Grounded base with Faraday shield loop

---

## 🔌 Real-World Output Options

- Option A: Plasma emitter window (argon + EM discharge)
- Option B: High-voltage air coil (visible corona, if desired)
- Option C: Helical IR beam pulse coil with fiber-fed output

---

## 🧰 Components Bill (Initial)

| Component | Spec | Quantity |
|-----------|------|----------|
| TPA3116D2 Audio Amp Board | 50W+50W Dual Channel | 1 |
| 3.5mm TRS Jack | Panel mount or breakout | 1 |
| Audio Transformer | 1:10 ratio | 1 |
| Tesla Coil | 10–15 turns, 3" dia, air core | 1 |
| Capacitor Topload | 100pF – 300pF equiv. | 1 |
| PSU | 24V–36V DC @ 5A+ | 1 |

---

## 📎 Notes:
- All components must be tested for thermal stability and EM shielding compliance.
- Use Faraday mesh enclosure to minimize stray emissions during lab testing.
- This schematic assumes non-lethal field strength for legal compliance.

---

More detailed circuit diagrams will follow in `.png` format under `hardware/schematics/`.

