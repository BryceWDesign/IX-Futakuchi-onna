# Electromagnetic Shielding Layout & Compliance Design

This document outlines the electromagnetic compatibility (EMC) containment and shielding strategy for the IX-Futakuchi-onna harmonic transmission platform. It is critical for:

- Preventing unintentional emissions
- Avoiding FCC/CE interference violations
- Reducing risk of backscatter feedback corrupting measurements
- Supporting legal operation during lab or field tests

---

## 🧱 Shielding Objectives

1. Prevent field leakage from Tesla coil / RF beam into environment
2. Shield MCU logic and analog stages from parasitic field coupling
3. Ensure safety of operators, nearby sensors, and other equipment
4. Provide documented EMC compliance pathway for DoD/DOE testing labs

---

## 📦 Physical Layout Recommendations

| Zone | Shielding Method | Notes |
|------|------------------|-------|
| Beam Emitter Coil | Faraday cage or copper mesh dome | Surround 120°, open-air front, grounded mesh |
| Field Modulator Board | Copper tape & EMI shielding enclosures | Wrap signal lines with ferrite clamps |
| Signal Amplifier | Mount in aluminum case with toroid input filtering | Avoid long unshielded leads |
| Feedback Receiver Coil | Enclosed in toroidal conductive cage, shielded from emitter | Differential mode rejection applied |
| MCU/Control Stack | Steel or shielded plastic with mesh window | Separate ground plane from emitter path |

---

## 🧲 Grounding Strategy

- All shields should **connect to a single-point star ground**
- Tesla coil secondary base → isolated earth ground rod (if legal in test environment)
- Shield grounds → local system ground (not shared with logic)
- Avoid ground loops — validate with continuity testing

---

## 🔌 Recommended Shielding Materials

| Material | Use Case |
|----------|-----------|
| Copper Mesh (100-300 mesh) | Coil dome, feedback receiver cage |
| EMI Copper Tape | PCB edges, cable wraps |
| Ferrite Beads | DC lines, sensor returns |
| Conductive Aluminum Foil | Internal reflective isolation |
| Shielded Ethernet Cable (Cat6a STP) | Sensor/control line runs |
| Shielded Metal Enclosure (Steel/Alu) | Amplifier and microcontroller housing |

---

## 🧪 Compliance Test Considerations

- Place system on **wood or acrylic test bench**
- Use **non-metallic test platforms** during field tuning
- Validate system radiated emissions using spectrum analyzer (9kHz–30MHz and 30MHz–1GHz bands)
- Document shielding resistance (<0.5Ω to GND) at all critical enclosures

---

This layout ensures the IX-Futakuchi-onna platform remains DARPA-compliant, FCC-safe, and legally deployable for research purposes, including beam output demonstration.

