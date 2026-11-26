# ThinkPad L480 4-Bay ThinkBox NAS — Assembly Guide & BOM

## 1. Overview & Outer Dimensions

A compact, quiet, modular 4-bay 3.5" SATA NAS enclosure engineered around a stripped **Lenovo ThinkPad L480** motherboard (`EL480` / `NM-B461`). The chassis splits at **`Y = 158 mm`** with a recessed tongue-and-groove alignment joint (`1.2 mm` tongue, `0.25 mm` per-side clearance) so every printable part fits a standard **`256 × 256 mm`** 3D print bed.

- **External dimensions:** `182 W × 294 D × 172 H mm` (`298.3 mm` overall D including `1.2 mm` raised `THINKBOX` front lettering and `3.1 mm` bolted `Rear_Brush_Plate`)
- **Wall thickness:** `4.0 mm` outer shell and center divider
- **Internal dual-chamber layout (along X):**
  - **Left access cover:** `4 mm` (`X = 0..4`), split into front/rear service panels
  - **L480 motherboard chamber:** `48 mm` (`X = 4..52`) with universal slotted standoff rails on the divider
  - **Center divider:** `4 mm` (`X = 52..56`) with a `60 × 62 mm` cable pass-through window (`Y = 172..232`, `Z = 56..118`)
  - **HDD & cooling chamber:** `122 mm` (`X = 56..178`) — 4× 3.5" removable trays in front (`Y = 6..154`), ASM1166 & Pico PSU on the rear floor plenum, and a `120 × 25 mm` rear exhaust fan (`1 mm` side clearance)
  - **Right outer wall:** `4 mm` (`X = 178..182`)
- **Vertical stack (along Z):** `4 mm` floor + `24 mm` lower chin + `4 × 33.5 mm` (`134 mm`) HDD bays + `6 mm` top clearance + `4 mm` roof = `172 mm`
- **Depth split (along Y):** `6 mm` front bezel (`0..6`) + `152 mm` front chassis (`6..158`) + `132 mm` rear chassis (`158..290`) + `4 mm` rear panel (`290..294`) = `294 mm`

---

## 2. 3D Printing Guide & STL Manifest

All 12 unique printable meshes are exported to `stl/`. Print **15 parts total** (`HDD_Tray.stl` × 4).

| STL File (`stl/`) | Qty | Dimensions (`W × D × H` mm) | Bed Orientation | Supports | ThinkBox Filament Color |
| --- | :-: | --- | --- | --- | --- |
| `Chassis_Front.stl` | 1 | `182.0 × 155.0 × 172.0` | Front face (`Y = 6`) down | Minimal local (rear mating lugs / rail starts) | Matte Black PETG / ASA |
| `Chassis_Rear.stl` | 1 | `182.0 × 132.0 × 172.0` | Rear face (`Y = 290`) down¹ | Minimal local (front mating lugs / floor standoffs) | Matte Black PETG / ASA |
| `Front_Bezel.stl` | 1 | `182.0 × 6.0 × 172.0` | Inner face (`Y = 6`) down | None (support-free) | Matte Black PETG / ASA |
| `ThinkPad_Red_Accent.stl` | 1 | `17.6 × 3.8 × 9.6` | Flat (`17.6 × 9.6 mm` face down) | None (support-free) | Matte / Signal Red PETG / ASA |
| `Front_Bezel_Text.stl` | 1 | `74.6 × 1.2 × 10.6` (`THINKBOX`) | Back face (`Y = 0`) down | None (support-free) | Bronze / Gold Metallic |
| `Rear_Panel.stl` | 1 | `182.0 × 4.0 × 172.0` | Outer face (`Y = 294`) down² | None (support-free) | Matte Black PETG / ASA |
| `Rear_Brush_Plate.stl` | 1 | `32.0 × 3.0 × 112.0` | Outer chamfered face (`Y = 297.1`) down⁴ | None (support-free) | Matte Black PETG / ASA |
| `Rear_Brush_Insert.stl` | 1 | `25.2 × 1.2 × 89.2` | Flat (`25.2 × 89.2 mm` face down) | None (support-free) | **95A TPU** (Black) *(or real strip brush)* |
| `Rear_Power_Grommet.stl` | 1 | `23.9 × 8.8 × 24.0` | Outer flange (`Y = 296.6`) down | None in 95A TPU (light tree under `Ø20` lip in PETG) | **95A TPU** (Black) or PETG |
| `Left_Cover_Front.stl` | 1 | `4.0 × 152.0 × 164.0` | Outer face (`X = 0`) down | None (support-free) | Matte Black PETG / ASA |
| `Left_Cover_Rear.stl` | 1 | `4.0 × 132.0 × 164.0` | Outer face (`X = 0`) down | None (support-free) | Matte Black PETG / ASA |
| `HDD_Tray.stl` | **4** | `110.0 × 152.8 × 30.3` | Cradle bottom down³ (or front face down + brim) | 0.5 mm under cradle floor³ (or none if front-down) | Matte Black / Dark Grey PETG / ASA |

> **Orientation notes:**
> 1. Printing `Chassis_Rear` with **`Y = 290` down** keeps the alignment groove (`Y = 158..161.3`) at the top, preventing first-layer elephant's foot from tightening the joint.
> 2. On `Rear_Panel`, the protective fan grille is flush with the outer face (`Y = 291.5..294`), so printing **outer face down** puts the grille flat on the bed with zero supports.
> 3. On `HDD_Tray`, the front sled face extends `0.5 mm` below the cradle floor (`fz1 = z0 - 0.5`). Printing **horizontal (cradle bottom down)** with build-plate-only support under the floor maximizes bending strength for ~650 g 3.5" drives; printing **front-face down with a brim** is completely support-free.
> 4. On `Rear_Brush_Plate`, printing **outer chamfered face (`Y = 297.1`) down** leaves the `1.5 mm` inner clamping recess facing upward so it prints cleanly without supports.

### Recommended Slicer Settings
- **Material:** **PETG** or **ASA** for structural parts (avoid PLA — sustained 40–55 °C HDD and CPU exhaust heat can creep/warp PLA trays and rails). Print **`Rear_Brush_Insert.stl`** and **`Rear_Power_Grommet.stl`** in **95A TPU** (or substitute a cut-to-length nylon strip brush clamped in the `1.5 mm` brush-plate recess; `Rear_Power_Grommet.stl` also prints in PETG).
- **Nozzle & Layers:** `0.4 mm` nozzle, `0.20 mm` layer height (`0.12–0.16 mm` for `Front_Bezel_Text.stl` for crisp `O`/`B` counters).
- **Walls & Infill:** `3–4` perimeters (`1.2–1.6 mm` walls), `4–5` top/bottom layers, `20–25%` gyroid infill (`100%` infill or `3` perimeters at slow speed for 95A TPU parts). Use `4` perimeters on `Chassis_Front`, `Chassis_Rear`, and `HDD_Tray` for strong heat-set insert engagement and rigid drive rails.
- **Brim:** Optional `4–5 mm` outer brim on `Chassis_Front` / `Chassis_Rear` (especially in ASA) to keep the split seam flat.

---

## 3. Hardware & Fastener BOM

### Compute, Storage & Power Electronics
| Qty | Component | Notes / Fitment |
| :-: | --- | --- |
| 1 | **Lenovo ThinkPad L480 motherboard** (`EL480` / `NM-B461`) | Stripped board with stock CPU heatsink/blower, DDR4 SO-DIMM(s), and NVMe boot SSD. Envelope fits `X = 4..45.6`, `Y = 12..287`, `Z = 22..152 mm`. |
| 1 | **M.2 B-key to M.2 M-key PCIe ribbon riser** | Connects L480 M.2 2242 WWAN (PCIe x2) slot to ASM1166 via divider window (~10–15 cm flexible FPC). |
| 1 | **6-port ASM1166 M.2-to-SATA III adapter** | Mounts on rear floor standoffs (`X = 64..86`, `Y = 172..252 mm`, `16 × 74 mm` hole pattern); 4 ports used, 2 spare. |
| 4 | **3.5" SATA HDDs** (SFF-8301 standard) | `101.6 × 147.0 × 26.1 mm`; trays support both 4-hole helium drives (`28.50`, `130.10 mm` from rear) and 6-hole drives (`69.85 mm` middle). |
| 4 | **Thin / flexible SATA data cables** (~20–30 cm) | Low-profile or right-angle connectors recommended for tidy routing in the rear plenum. |
| 1 | **120 × 25 mm quiet PWM exhaust fan** | e.g., **Noctua NF-A12x25 PWM** or **NF-S12A PWM** (`105 × 105 mm` mounting pattern, `Ø114 mm` bore). |
| 1 | **12V DC-ATX Pico PSU** (or 12V→5V/12V SATA power board) + 4-way SATA power splitter | Dedicated HDD + fan power rail; mounts on rear floor standoffs (`X = 108..162`, `Y = 192..234 mm`, `48 × 36 mm` pattern) and/or floor zip-tie slots. |
| 1 | **Silent fanless 12V DC power brick** (12V 8A–10A / 96–120W) | Sized for simultaneous 4× 3.5" HDD spin-up (~2A peak per drive); cable feeds directly through `Rear_Power_Grommet` (`Ø8 mm` bore, `3.5 mm` entry slit at `X = 158, Z = 16`) behind the Pico PSU. |
| 1 | **Lenovo 65W USB-C power adapter** | Dedicated power for L480 motherboard; cord routes cleanly through the bolted `Rear_Brush_Plate` pass-through (`16 × 82 mm` stadium slot). |
| 1 | **12 mm panel-mount momentary power button** | Fits front bezel `Ø12.2 mm` hole at `(X = 19, Z = 152)`, wired to L480 power switch pads/header. |
| Opt. | **Front/rear cables & strip brush** | `Ø3 mm` power LED (`Ø3.2 mm` hole), front USB-A (`14 × 7 mm`) & USB-C (`10 × 4.5 mm`) extensions; rear Cat6 Ethernet / HDMI / USB cables pass directly through `Rear_Brush_Plate` (with printable 95A TPU `Rear_Brush_Insert` or cut-to-length nylon strip brush in its `1.5 mm` clamping recess). |

### Fasteners & Mechanical Hardware
| Qty | Fastener / Hardware | Hole Spec in CAD | Location |
| :-: | --- | --- | --- |
| **24** | **M3 heat-set brass inserts** (`M3 × 5.7 mm`, OD `4.2–4.6 mm`) | `Ø4.0 mm × 7.0–7.5 mm` deep | 4× `Front_Bezel` bosses, 8× `Left_Cover` frames (4 front + 4 rear), 6× `Chassis_Rear` split mating lugs, 6× `Rear_Panel` bosses *(buy 30+ for spares)* |
| **4** | **M3 × 10 mm countersunk (FHCS)** | `Ø3.4 mm` thru, `Ø6.4 × 2.2 mm` csink | `Front_Bezel` (`6 mm`) → `Chassis_Front` |
| **4** | **M3 × 10 mm button-head (BHCS) + 4× M3 hex nuts / locknuts** | `Ø3.4 mm` thru (`4 mm` panel + `3 mm` plate) | Bolt `Rear_Brush_Plate` (clamping `Rear_Brush_Insert` / strip brush) to `Rear_Panel` at `(18, 34)`, `(38, 34)`, `(18, 134)`, `(38, 134)` |
| **14** | **M3 × 8 mm button/socket head (BHCS/SHCS)** | `Ø3.4 mm` thru | 8× `Left_Cover_Front` + `Left_Cover_Rear` (`4 mm`), 6× `Rear_Panel` (`4 mm`) |
| **5** | **M3 × 14 mm socket head (SHCS)** | `Ø3.4 mm` thru (`8 mm` front lug) | `Chassis_Front` ↔ `Chassis_Rear` split mating lugs (5 full-depth lugs) |
| **1** | **M3 × 10 mm socket head (SHCS)** | `Ø3.4 mm` thru (`3.8 mm` front lug) | Top-right split mating lug at `(X = 172, Z = 161.25)` (recessed to clear top HDD tray) |
| **4–6** | **M3 × 12 mm** (or **M2.5 × 12 mm**) screws + nuts + nylon washers | `3.4 mm` horizontal slots (`6 mm` rail) | L480 motherboard onto universal slotted standoff rails (`Z = 41` & `Z = 131 mm`) |
| **8** | **M3 × 6 mm** screws (+ 2× small zip ties) | `Ø2.6 mm × 5 mm` pilot holes | 4× ASM1166 floor standoffs, 4× Pico PSU floor standoffs (plus 2× floor zip-tie slots) |
| **16–24** | **#6-32 UNC × 1/4" (`6.35 mm`) low-profile pan/wafer HDD screws** | `Ø4.0 mm` thru, `Ø7.0 × 1.5 mm` cbore | 4× 3.5" HDDs into `HDD_Tray` (4/drive for helium drives, up to 6/drive; **head Ø must be `≤ 6.8 mm`** to sit flush and clear `0.6 mm` rail gap) |
| **4** | **Noctua silicone anti-vibration mounts** (or standard M5 fan screws) | `Ø4.5 mm` holes (`105 × 105 mm`) | `120 × 25 mm` exhaust fan → `Rear_Panel` |
| **4** | **`Ø12 mm` stick-on silicone/rubber feet** (`4–6 mm` tall) | `Ø12.0 × 2.0 mm` pockets | Bottom corners at `X = 16, 166`; `Y = 22, 274` |

---

## 4. Step-by-Step Assembly & Cabling

1. **Install all 24 M3 heat-set inserts & rubber feet**
   - Press inserts straight and flush using a soldering iron (~220–240 °C for PETG, ~250–265 °C for ASA):
     - `Chassis_Front` (8 inserts): 4 front bezel bosses at `(8, 8)`, `(8, 164)`, `(173, 14)`, `(54, 164)`; 4 left-cover frame holes (`Y = 20, 153`, `Z = 8, 164`).
     - `Chassis_Rear` (16 inserts): 6 split mating lugs at `Y = 158`; 4 left-cover frame holes (`Y = 163, 276`, `Z = 8, 164`); 6 rear panel bosses at `(12, 16)`, `(12, 160)`, `(48, 16)`, `(48, 160)`, `(117, 16)`, `(117, 162)`.
   - Press the 4× `Ø12 mm` rubber feet into the recessed bottom pockets so the bottom intake vents sit `2–4 mm` off the desk.

2. **Join `Chassis_Front` and `Chassis_Rear` (`Y = 158 mm`)**
   - Dry-fit the `1.2 mm` alignment tongue (`Chassis_Front`) into the groove (`Chassis_Rear`); lightly deburr any elephant's foot if tight.
   - Fasten the 6 mating lugs from inside `Chassis_Front`: **5× M3 × 14 mm** on the standard `8 mm` lugs, and **1× M3 × 10 mm** on the thinner top-right lug (`X = 172, Z = 161.25`).

3. **Assemble & mount `Front_Bezel`**
   - Press-fit (or glue with a drop of CA/epoxy) `ThinkPad_Red_Accent.stl` into the front recess (`X = 10..28, Z = 82..92`).
   - Align and glue `Front_Bezel_Text.stl` (`THINKBOX`) centered on the lower chin (`X = 117, Z = 14`).
   - Install the `Ø12 mm` momentary power button (and optional `Ø3 mm` LED / front USB pigtails) with leads coiled into the L480 chamber.
   - Attach `Front_Bezel` to `Chassis_Front` with **4× M3 × 10 mm FHCS**.

4. **Mount the ThinkPad L480 motherboard**
   - Position the stripped L480 motherboard vertically in the left chamber (`X = 4..46`, CPU heatsink facing outward toward `Left_Cover` vents, PCB resting against the `6 mm` slotted rails at `X = 46`).
   - Align 4–6 of the motherboard's mounting holes with the two horizontal slots (`Z = 41 mm` lower, `Z = 131 mm` upper, spanning `Y = 22..146` and `Y = 170..274`).
   - Secure with **M3 (or M2.5) × 12 mm screws, nuts behind the rail, and nylon insulating washers** under the screw heads. Connect the front power button and LED leads.

5. **Install rear floor plenum electronics & route cross-chamber cables**
   - Mount the **ASM1166 M.2-to-SATA adapter** on the 4 left-rear floor standoffs (`X = 67, 83`; `Y = 175, 249`) with **4× M3 × 6 mm** screws.
   - Mount the **Pico PSU** on the 4 right-rear floor standoffs (`X = 111, 159`; `Y = 195, 231`) with **4× M3 × 6 mm** screws and/or strap it through the two floor zip-tie slots (`Y = 184..188` and `238..242`).
   - Route the **M.2 B-key to M-key PCIe ribbon riser** from the L480 WWAN slot through the `60 × 62 mm` center divider window (`Y = 172..232, Z = 56..118`) and seat it cleanly into the ASM1166. Keep bend radii gentle.
   - Route the fan PWM/power wire cleanly along the rear floor away from the fan blades (the 12V Pico PSU cable enters directly behind the Pico PSU via the bottom-right `Rear_Power_Grommet`).

6. **Load the 4× 3.5" HDDs & connect SATA cabling**
   - Place each 3.5" drive into an `HDD_Tray` (SATA connectors facing the open rear of the tray, `Y = 153.8`) and fasten with **4–6× `#6-32 × 1/4"` low-profile screws** into the SFF-8301 side holes. Confirm screw heads sit flush inside the `Ø7.0 × 1.5 mm` counterbores.
   - Connect 4× SATA data cables to the ASM1166 and the 4-way SATA power harness to the Pico PSU.
   - Slide each tray along its chassis guide rails until it seats against the `Y = 154 mm` rear end-stops, then plug in SATA data and power through the open rear chamber, dressing slack neatly below the fan sweep.

7. **Install the 120 mm exhaust fan, rear cable pass-throughs & `Rear_Panel`**
   - Mount the **120 × 25 mm PWM fan** to the inner face of `Rear_Panel` (`Y = 290`, airflow arrow pointing **outward / `+Y` rear exhaust**) using 4× silicone anti-vibration mounts or fan screws.
   - Seat `Rear_Brush_Insert.stl` (95A TPU comb) — or a cut-to-length nylon strip brush — inside the `1.5 mm` inner clamping recess on `Rear_Brush_Plate.stl`, then bolt `Rear_Brush_Plate` to the rear face of `Rear_Panel` with **4× M3 × 10 mm BHCS + M3 hex/nyloc nuts** at `(18, 34)`, `(38, 34)`, `(18, 134)`, `(38, 134)`.
   - Feed the L480 rear cables (Lenovo 65W USB-C power cord, Cat6 Ethernet, optional HDMI/USB) through the bolted brush pass-through (`16 × 82 mm` stadium slot).
   - Slip the pre-terminated 12V DC power brick cable through the `3.5 mm` radial entry slit of `Rear_Power_Grommet.stl`, snap the grommet into the bottom-right `Ø18 mm` bore at `(X = 158, Z = 16)`, and connect it to the Pico PSU.
   - Plug in the fan power/PWM lead and fasten `Rear_Panel` to `Chassis_Rear` with **6× M3 × 8 mm** screws.
   - *Tip:* Power-test the Pico PSU + drives + L480 boot before buttoning up the side covers. (If using a separate 12V brick + Pico PSU, ensure the Pico PSU `PS_ON` pin is bridged or triggered by L480 USB 5V via a small relay/optocoupler so HDDs power on/off with the ThinkPad.)

8. **Close side access covers**
   - Install `Left_Cover_Front` and `Left_Cover_Rear` with **8× M3 × 8 mm** screws.

### Quiet Front-to-Back Airflow Path
- **Right chamber (HDDs + Plenum):** Cool room air enters through the slotted front sled faces (`HDD_Tray`) and bottom chassis vents → passes across all 4 drives (`7.4 mm` inter-bay gap + vented tray floors) → cools the ASM1166 and Pico PSU on the rear floor → exhausted out the rear by the low-RPM `120 × 25 mm` fan through the open protective grille.
- **Left chamber (ThinkPad L480):** Cool air enters through the front bezel perforated `Ø3.6 mm` mesh and `Left_Cover` horizontal slots → drawn in by the stock L480 blower over the CPU heatsink → exhausted out the **2× upper rear louver slots** (`X = 14..42, Z = 144..148.5` and `151..155.5`) above the sealed brush cable pass-through.

---

## 5. Parametric Customization

All critical dimensions live in the `PARAMS` dictionary at the top of [`build_thinkpad_nas.py`](build_thinkpad_nas.py) and are mirrored into the **`Parameters`** spreadsheet inside **`ThinkPad_L480_NAS.FCStd`** for quick inspection in FreeCAD.

To adjust clearances (e.g., for a thicker L480 heatsink, tighter/looser printer tolerances, different M3 heat-set insert OD, or thicker power cable):
1. Open `build_thinkpad_nas.py` and edit the relevant keys in `PARAMS`:
   - `CHAMBER_L480_W` (`48.0`) & `L480_PCB_X` (`44.0`) — L480 chamber width and heatsink clearance
   - `L480_Y_START` (`12.0`), `L480_Y_END` (`287.0`), `L480_Z_START` (`22.0`), `L480_Z_END` (`152.0`) — L480 reference mockup envelope
   - `HDD_BAY_PITCH` (`33.5`) & `TRAY_Z_CLEAR` (`0.2`) — vertical spacing and rail sliding clearance
   - `M3_INSERT_D` (`4.0`) & `M3_CLEAR_D` (`3.4`) — tune for your specific brass inserts and printer hole shrinkage
   - `BRUSH_SLOT_W` (`16.0`), `BRUSH_SLOT_H` (`82.0`), `GROMMET_CABLE_D` (`8.0`), `GROMMET_SLIT_W` (`3.5`) — rear brush pass-through and split power grommet sizing
   - `WALL_THICK` (`4.0`) & `SPLIT_Y` (`158.0`) — structural wall thickness and front/rear print-bed split plane
2. Re-run `build_thinkpad_nas.py` inside FreeCAD (macro or Python console: `exec(open(r"c:\Users\Administrator\Documents\Thinkpad NAS\build_thinkpad_nas.py").read())`). This rebuilds `ThinkPad_L480_NAS.FCStd`, updates the `Parameters` spreadsheet, and re-exports all 12 meshes in `stl/`.
