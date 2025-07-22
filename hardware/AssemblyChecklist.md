# IX-Futakuchi-onna: Assembly & Integration Checklist

Use this document during system construction to ensure correct physical, electrical, and signal-layer assembly. Designed for DARPA lab evaluation, private test bench builds, or advanced university R&D setups.

---

## ✅ Physical Components

- [ ] Enclosure mounted (non-conductive or shielded aluminum housing)
- [ ] Tesla coil emitter secured and isolated from chassis
- [ ] Field feedback coil mounted on tuned standoff away from emitter
- [ ] Cooling system installed (12V fan or Peltier, optional)
- [ ] Cable strain reliefs installed on all DC, signal, and coil lines

---

## 🔌 Power Systems

- [ ] All DC rails verified with multimeter before system power-on
- [ ] Ground isolation confirmed between MCU and amplifier rails
- [ ] Amplifier powered from 24–36V with inline fuse (5A or less)
- [ ] DAC-to-Amp connection <12” using shielded cable
- [ ] Power supply fans unobstructed; airflow path validated

---

## 📡 Signal Chain

- [ ] `generate_test_output_obfuscated.py` run successfully
- [ ] Waveform test output (via FFT visualizer) shows 3x, 6x, 9x peaks
- [ ] Obfuscator, modulator, and encryptor output valid phase-mapped signal
- [ ] Field feedback loop reads correct HIGH/LOW GPIO signal from sensor
- [ ] Lock confirmed before `BeamEmitterController.emit_waveform()` is called

---

## 🧪 Safety & Legal

- [ ] Tesla coil ground rod (if used) is legal in your jurisdiction
- [ ] All enclosures grounded (star topology)
- [ ] Operator standing surface is non-conductive (rubber mat or wood)
- [ ] GFI (ground fault interrupter) used on main power input
- [ ] EMC shielding validated using handheld spectrum analyzer (optional)

---

## 📂 Data Output Verification

- [ ] All `.wav` test files excluded from repo per policy
- [ ] FFT plots or CSV logs captured for validation
- [ ] External observer (DARPA/lab) able to verify transmission log
- [ ] No proprietary formats used; all output reproducible from `.py` only

---

## 🧾 Documentation & Labeling

- [ ] README.md printed or displayed near system
- [ ] All cables labeled (e.g., `5V Logic`, `24V AMP`, `Sensor GND`)
- [ ] FieldModulator and HarmonicEncryptor settings documented per test
- [ ] Serial numbers (if used) recorded in deployment log

---

This checklist is designed for real-world builds with reproducible logic chain from waveform generation to transmission, reception, and validation. No fluff, no fiction — 100% grounded system engineering.

