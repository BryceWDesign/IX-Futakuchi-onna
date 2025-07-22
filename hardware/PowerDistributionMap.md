# Power Distribution Map: IX-Futakuchi-onna

This document outlines the full power infrastructure of the IX-Futakuchi-onna platform. All voltages, current limits, isolation strategies, and interconnects are documented to ensure thermal, electrical, and safety compliance under lab and field testing.

---

## 🔋 System Power Overview

| Subsystem | Voltage | Typical Current | Notes |
|-----------|---------|-----------------|-------|
| Raspberry Pi / MCU | 5V DC | 1.5A | Logic, control, FFT, and sensor interface |
| DAC Output Stage | 3.3V / 5V | 100mA | Optional level shifter if needed |
| Signal Amplifier | 24–36V DC | 3–5A | Drives Tesla coil or laser module |
| Feedback Sensor | 3.3V or 5V | <100mA | Isolated ADC / GPIO return logic |
| Cooling Fans | 12V DC | 0.3–1A | Recommended: independent power rail |
| Optional Field PSU | 48V DC | 1–2A | For high-energy experimental field emitter (isolated rail) |

---

## ⚙️ Isolation & Grounding Strategy

- MCU ground isolated from amplifier ground
- Star-ground topology used at DC power bus for all returns
- Feedback sensor is optically or magnetically isolated from emitter stage
- Tesla secondary base grounded to independent Earth spike (optional, legal-permitting)
- USB DAC → isolated via USB optical coupler if needed

---

## 🔌 Suggested Power Distribution Block

| Rail | Source | Devices |
|------|--------|---------|
| 5V Logic | USB-PD or buck converter from 12V | Raspberry Pi, ADC, sensors |
| 24V Bus | Industrial DC supply (e.g., MeanWell LRS-350-24) | Class D amp, coil interface |
| 12V Utility | Linear or switching PSU | Cooling fan, optional optics |
| Ground Reference | Star-ground tie point | All shields, case grounds, PSU returns |

---

## 🧯 Safety & Protection

- All rails fused: 5A fuse for 24V, 2A for logic line
- TVS diodes on amplifier input/output rails
- Inline current limiter for field emitter stage
- Ground fault interrupter (GFI) recommended for wall power
- Chassis earth bonded to all enclosures

---

## 📐 Cable Layout Guidance

- Keep coil wires >4" from logic lines
- Use shielded twisted pair for analog signal routing
- Keep DAC-to-amp cable short (<12")
- Avoid ground loops by enforcing one ground path per rail

---

This power map ensures full buildability, safety, and lab-rated compliance for energy delivery and feedback-sensitive systems used in IX-Futakuchi-onna.

