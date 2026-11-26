import os
import FreeCAD as App
import MeshPart
import Part

# ==============================================================================
# PARAMETRIC DIMENSIONS (all units in mm)
# ==============================================================================
PARAMS = {
    # Overall envelope
    "WALL_THICK": 4.0,
    "CHAMBER_L480_W": 48.0,      # X = 4..52
    "DIVIDER_W": 4.0,            # X = 52..56
    "CHAMBER_HDD_W": 122.0,      # X = 56..178 (fits 120mm fan + 1mm/side)
    "TOTAL_W": 182.0,            # 4 + 48 + 4 + 122 + 4

    "BEZEL_D": 6.0,              # Y = 0..6
    "CHASSIS_FRONT_D": 152.0,    # Y = 6..158
    "CHASSIS_REAR_D": 132.0,     # Y = 158..290
    "REAR_PANEL_D": 4.0,         # Y = 290..294
    "SPLIT_Y": 158.0,
    "TOTAL_D": 294.0,

    "CHIN_H": 24.0,              # Z = 4..28
    "HDD_BAY_PITCH": 33.5,       # 4 bays: Z = 28..162
    "HDD_BAY_COUNT": 4,
    "TOP_CLEAR_H": 6.0,          # Z = 162..168
    "TOTAL_H": 172.0,            # 4 + 24 + 134 + 6 + 4

    # 3.5" HDD (SFF-8301) & Tray
    "HDD_W": 101.6,
    "HDD_D": 147.0,
    "HDD_H": 26.1,
    "TRAY_CRADLE_W": 108.4,      # X = 62.8..171.2
    "TRAY_WALL_T": 3.0,
    "TRAY_FLOOR_T": 2.5,
    "TRAY_WALL_H": 16.5,
    "TRAY_CRADLE_Y_START": 6.0,
    "TRAY_CRADLE_Y_END": 153.8,
    "TRAY_FACE_W": 110.0,        # X = 62.0..172.0
    "TRAY_FACE_H": 30.3,         # Z0 - 0.5 .. Z0 + 29.8
    "TRAY_FACE_Y_START": 1.0,
    "TRAY_FACE_Y_END": 6.0,
    "RAIL_TOP_T": 2.5,
    "TRAY_Z_CLEAR": 0.2,
    "HDD_HOLE_Z_OFFSET": 6.35,   # SFF-8301 side hole above HDD bottom
    "HDD_HOLE_FROM_REAR": (28.50, 69.85, 130.10),  # Y=153.5 - d -> 125.00, 83.65, 23.40

    # Cooling Fan (120x120x25 mm)
    "FAN_SIZE": 120.0,
    "FAN_THICK": 25.0,
    "FAN_CX": 117.0,
    "FAN_CZ": 90.0,
    "FAN_BORE_D": 114.0,
    "FAN_MOUNT_SPAN": 105.0,     # +/- 52.5 from center
    "FAN_MOUNT_HOLE_D": 4.5,

    # Fasteners
    "M3_CLEAR_D": 3.4,
    "M3_INSERT_D": 4.0,
    "M3_CSINK_D": 6.4,
    "SCREW_6_32_D": 4.0,
    "SCREW_6_32_HEAD_D": 7.0,

    # Electronics mockups & mounting
    "L480_PCB_X": 44.0,
    "L480_PCB_T": 1.6,
    "L480_Y_START": 12.0,
    "L480_Y_END": 287.0,
    "L480_Z_START": 22.0,
    "L480_Z_END": 152.0,
}

DOC_NAME = "ThinkPad_L480_NAS"
SAVE_PATH = r"c:\Users\Administrator\Documents\Thinkpad NAS\ThinkPad_L480_NAS.FCStd"
STL_DIR = r"c:\Users\Administrator\Documents\Thinkpad NAS\stl"

EXPORT_PARTS = [
    ("Chassis_Front", "Chassis_Front.stl"),
    ("Chassis_Rear", "Chassis_Rear.stl"),
    ("Front_Bezel", "Front_Bezel.stl"),
    ("ThinkPad_Red_Accent", "ThinkPad_Red_Accent.stl"),
    ("Front_Bezel_Text", "Front_Bezel_Text.stl"),
    ("Rear_Panel", "Rear_Panel.stl"),
    ("Left_Cover_Front", "Left_Cover_Front.stl"),
    ("Left_Cover_Rear", "Left_Cover_Rear.stl"),
    ("HDD_Tray_1", "HDD_Tray.stl"),  # Assembly coords (cradle floor parallel to XY, Z-up)
]


def box(x1, y1, z1, x2, y2, z2):
    return Part.makeBox(x2 - x1, y2 - y1, z2 - z1, App.Vector(x1, y1, z1))


def cyl_x(x1, x2, cy, cz, r):
    return Part.makeCylinder(r, x2 - x1, App.Vector(x1, cy, cz), App.Vector(1, 0, 0))


def cyl_y(cx, y1, y2, cz, r):
    return Part.makeCylinder(r, y2 - y1, App.Vector(cx, y1, cz), App.Vector(0, 1, 0))


def cyl_z(cx, cy, z1, z2, r):
    return Part.makeCylinder(r, z2 - z1, App.Vector(cx, cy, z1), App.Vector(0, 0, 1))


def add_part(doc, group, name, shape, color=(0.14, 0.14, 0.15), transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if group is not None:
        group.addObject(obj)
    if App.GuiUp and obj.ViewObject:
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = transparency
    return obj


def make_spreadsheet(doc):
    sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
    sheet.set("A1", "Parameter")
    sheet.set("B1", "Value")
    sheet.set("C1", "Unit")
    row = 2
    for k, v in PARAMS.items():
        if isinstance(v, (int, float)):
            sheet.set(f"A{row}", k)
            sheet.set(f"B{row}", str(v))
            sheet.set(f"C{row}", "mm" if "COUNT" not in k else "count")
            row += 1
        elif isinstance(v, tuple):
            sheet.set(f"A{row}", k)
            sheet.set(f"B{row}", ", ".join(str(x) for x in v))
            sheet.set(f"C{row}", "mm")
            row += 1
    return sheet


# ==============================================================================
# 1. CHASSIS FRONT & REAR
# ==============================================================================
def build_chassis_shell_base(y1, y2):
    """Build common bottom, top, right wall, center divider, left frame, and rails."""
    W = PARAMS["TOTAL_W"]
    H = PARAMS["TOTAL_H"]
    T = PARAMS["WALL_THICK"]
    DIV_X1 = T + PARAMS["CHAMBER_L480_W"]        # 52.0
    DIV_X2 = DIV_X1 + PARAMS["DIVIDER_W"]        # 56.0
    RW_X1 = W - T                                # 178.0

    solids = [
        box(0.0, y1, 0.0, W, y2, T),             # Bottom (full width, flush under left cover)
        box(0.0, y1, H - T, W, y2, H),           # Top
        box(RW_X1, y1, T, W, y2, H - T),         # Right wall
        box(DIV_X1, y1, T, DIV_X2, y2, H - T),   # Center divider
        # Left access recess frame strips (X=4..12) along bottom & top
        box(T, y1, T, T + 8.0, y2, T + 8.0),
        box(T, y1, H - T - 8.0, T + 8.0, y2, H - T),
    ]
    return solids


def build_chassis_front():
    W = PARAMS["TOTAL_W"]
    H = PARAMS["TOTAL_H"]
    T = PARAMS["WALL_THICK"]
    DIV_X1 = T + PARAMS["CHAMBER_L480_W"]        # 52.0
    DIV_X2 = DIV_X1 + PARAMS["DIVIDER_W"]        # 56.0
    RW_X1 = W - T                                # 178.0
    y1 = PARAMS["BEZEL_D"]                       # 6.0
    y2 = PARAMS["SPLIT_Y"]                       # 158.0

    solids = build_chassis_shell_base(y1, y2)

    # Vertical left access frame pillars at front (Y=6..16) and rear (Y=148..158)
    solids.append(box(T, y1, T + 8.0, T + 8.0, y1 + 10.0, H - T - 8.0))
    solids.append(box(T, y2 - 10.0, T + 8.0, T + 8.0, y2, H - T - 8.0))

    # 4-Bay HDD Guide Rails (Y=6..156)
    rail_y2 = y2 - 2.0  # 156.0
    for i in range(PARAMS["HDD_BAY_COUNT"]):
        zb = T + PARAMS["CHIN_H"] + i * PARAMS["HDD_BAY_PITCH"]
        rt = PARAMS["RAIL_TOP_T"]
        # Bottom ledges
        solids.append(box(DIV_X2, y1, zb, DIV_X2 + 9.0, rail_y2, zb + rt))
        solids.append(box(RW_X1 - 9.0, y1, zb, RW_X1, rail_y2, zb + rt))
        # Side centering guides (0.6mm clearance to 108.4mm tray: 62.2..171.8)
        solids.append(box(DIV_X2, y1, zb + rt, 62.2, rail_y2, zb + 14.0))
        solids.append(box(171.8, y1, zb + rt, RW_X1, rail_y2, zb + 14.0))
        # Rear end-stops (Y=154..156)
        solids.append(box(DIV_X2, 154.0, zb + rt, 64.0, rail_y2, zb + 10.0))
        solids.append(box(170.0, 154.0, zb + rt, RW_X1, rail_y2, zb + 10.0))

    # Universal L480 Slotted Standoff Rails on left face of divider (X=46..52)
    rail_cuts = []
    for z_lo, z_hi in ((34.0, 48.0), (124.0, 138.0)):
        solids.append(box(46.0, 16.0, z_lo, DIV_X1, 152.0, z_hi))
        zc = 0.5 * (z_lo + z_hi)
        rail_cuts.append(box(45.0, 22.0, zc - 1.7, DIV_X1 + 1.0, 146.0, zc + 1.7))

    # Front bezel corner M3 bosses (at Y=6..14)
    bezel_bosses = [
        (8.0, 8.0),
        (8.0, 164.0),
        (173.0, 14.0),
        (54.0, 164.0),
    ]
    for bx, bz in bezel_bosses:
        r_boss = 4.0 if bx <= 10.0 else 4.5  # keep left bosses flush inside X>=4 (clear of Left_Cover_Front)
        solids.append(cyl_y(bx, y1, y1 + 8.0, bz, r_boss))
    # Bridge bottom-right bezel boss (173, 14) solidly to right wall & bottom floor
    solids.append(box(168.5, y1, T, RW_X1, y1 + 8.0, 14.0))
    solids.append(box(173.0, y1, 9.5, RW_X1, y1 + 8.0, 18.5))

    # Rear mating lugs at Y=150..158 (plus top-right flange at Y=154.2..158)
    mating_lugs = [
        (16.0, 4.0, 28.0, 16.0, 150.0, 22.0, 10.0),    # Left-chamber bottom
        (56.0, 4.0, 68.0, 16.0, 150.0, 62.0, 10.0),    # Divider right bottom
        (166.0, 4.0, 178.0, 16.0, 150.0, 172.0, 10.0), # Right-wall bottom
        (16.0, 156.0, 28.0, 168.0, 150.0, 22.0, 162.0),# Left-chamber top
        (40.0, 156.0, 52.0, 168.0, 150.0, 46.0, 162.0),# Divider left top
        (166.0, 154.5, 178.0, 168.0, 154.2, 172.0, 161.25), # Right-wall top (clears tray Y<=153.8)
    ]
    for x1, z1, x2, z2, ly1, _, _ in mating_lugs:
        solids.append(box(x1, ly1, z1, x2, y2, z2))

    # Alignment tongue at Y=158..161 (1.2mm thick, recessed inside 4mm walls)
    solids.append(box(6.0, y2, 1.4, W - 2.0, y2 + 3.0, 2.6))          # Bottom tongue
    solids.append(box(6.0, y2, H - 2.6, W - 2.0, y2 + 3.0, H - 1.4))  # Top tongue
    solids.append(box(RW_X1 + 1.4, y2, 2.6, RW_X1 + 2.6, y2 + 3.0, H - 2.6))  # Right wall
    solids.append(box(DIV_X1 + 1.4, y2, 4.0, DIV_X1 + 2.6, y2 + 3.0, H - 4.0)) # Divider

    base = solids[0]
    for s in solids[1:]:
        base = base.fuse(s)

    # Collect all cuts
    cuts = list(rail_cuts)

    # Bottom ventilation slots (HDD chamber X=68..166, L480 chamber X=18..44; clear of front foot pockets Y<=28)
    for x_start, x_end in ((18.0, 44.0), (68.0, 166.0)):
        for yy in range(34, 146, 12):
            cuts.append(box(x_start, float(yy), -1.0, x_end, float(yy + 6), T + 1.0))

    # Front rubber-foot pockets (Ø12 x 2mm deep)
    cuts.append(cyl_z(16.0, 22.0, -1.0, 2.0, 6.0))
    cuts.append(cyl_z(166.0, 22.0, -1.0, 2.0, 6.0))

    # Left cover M3 insert holes (4 corners of Left_Cover_Front; Y=20 clears front bezel inserts at Y=6..13.5)
    for cy, cz in ((20.0, 8.0), (20.0, 164.0), (153.0, 8.0), (153.0, 164.0)):
        cuts.append(cyl_x(T - 1.0, T + 7.0, cy, cz, PARAMS["M3_INSERT_D"] * 0.5))

    # Front bezel M3 insert holes
    for bx, bz in bezel_bosses:
        cuts.append(cyl_y(bx, y1 - 1.0, y1 + 7.5, bz, PARAMS["M3_INSERT_D"] * 0.5))

    # Mating lug M3 through-holes
    for _, _, _, _, ly1, hx, hz in mating_lugs:
        cuts.append(cyl_y(hx, ly1 - 1.0, y2 + 1.0, hz, PARAMS["M3_CLEAR_D"] * 0.5))

    return base.cut(Part.makeCompound(cuts))


def build_chassis_rear():
    W = PARAMS["TOTAL_W"]
    H = PARAMS["TOTAL_H"]
    T = PARAMS["WALL_THICK"]
    DIV_X1 = T + PARAMS["CHAMBER_L480_W"]        # 52.0
    DIV_X2 = DIV_X1 + PARAMS["DIVIDER_W"]        # 56.0
    RW_X1 = W - T                                # 178.0
    y1 = PARAMS["SPLIT_Y"]                       # 158.0
    y2 = y1 + PARAMS["CHASSIS_REAR_D"]           # 290.0

    solids = build_chassis_shell_base(y1, y2)

    # Vertical left access frame pillars at Y=158..168 and Y=280..290
    solids.append(box(T, y1, T + 8.0, T + 8.0, y1 + 10.0, H - T - 8.0))
    solids.append(box(T, y2 - 10.0, T + 8.0, T + 8.0, y2, H - T - 8.0))

    # Continuation of L480 universal slotted standoff rails (Y=164..280)
    rail_cuts = []
    for z_lo, z_hi in ((34.0, 48.0), (124.0, 138.0)):
        solids.append(box(46.0, 164.0, z_lo, DIV_X1, 280.0, z_hi))
        zc = 0.5 * (z_lo + z_hi)
        rail_cuts.append(box(45.0, 170.0, zc - 1.7, DIV_X1 + 1.0, 274.0, zc + 1.7))

    # Matching mating lugs at Y=158..166
    mating_lugs = [
        (16.0, 4.0, 28.0, 16.0, 22.0, 10.0),
        (56.0, 4.0, 68.0, 16.0, 62.0, 10.0),
        (166.0, 4.0, 178.0, 16.0, 172.0, 10.0),
        (16.0, 156.0, 28.0, 168.0, 22.0, 162.0),
        (40.0, 156.0, 52.0, 168.0, 46.0, 162.0),
        (166.0, 154.5, 178.0, 168.0, 172.0, 161.25),
    ]
    for x1, z1, x2, z2, _, _ in mating_lugs:
        solids.append(box(x1, y1, z1, x2, y1 + 8.0, z2))

    # ASM1166 M.2-to-SATA mounting standoffs (X=64..86, Y=172..252, Z=4..10)
    asm_pts = [(67.0, 175.0), (83.0, 175.0), (67.0, 249.0), (83.0, 249.0)]
    for sx, sy in asm_pts:
        solids.append(cyl_z(sx, sy, T, 10.0, 3.0))

    # Pico PSU mounting standoffs (X=108..162, Y=192..234, Z=4..10)
    pico_pts = [(111.0, 195.0), (159.0, 195.0), (111.0, 231.0), (159.0, 231.0)]
    for sx, sy in pico_pts:
        solids.append(cyl_z(sx, sy, T, 10.0, 3.0))

    # Rear panel M3 insert bosses (Y=282..290), positioned outside 120mm fan envelope
    rear_bosses = [
        (12.0, 16.0),
        (12.0, 160.0),
        (48.0, 16.0),
        (48.0, 160.0),
        (117.0, 16.0),
        (117.0, 162.0),
    ]
    for bx, bz in rear_bosses:
        solids.append(cyl_y(bx, y2 - 8.0, y2, bz, 4.5))
    # Bridge center-bottom (117, 16) and center-top (117, 162) rear bosses to bottom/top walls
    solids.append(box(112.5, y2 - 8.0, T, 121.5, y2, 16.0))
    solids.append(box(112.5, y2 - 8.0, 162.0, 121.5, y2, H - T))

    base = solids[0]
    for s in solids[1:]:
        base = base.fuse(s)

    cuts = list(rail_cuts)

    # Alignment groove at Y=158..161.3 (0.25mm clearance around 1.2mm tongue)
    cuts.append(box(5.75, y1 - 1.0, 1.15, W - 1.75, y1 + 3.3, 2.85))
    cuts.append(box(5.75, y1 - 1.0, H - 2.85, W - 1.75, y1 + 3.3, H - 1.15))
    cuts.append(box(RW_X1 + 1.15, y1 - 1.0, 2.35, RW_X1 + 2.85, y1 + 3.3, H - 2.35))
    cuts.append(box(DIV_X1 + 1.15, y1 - 1.0, 3.8, DIV_X1 + 2.85, y1 + 3.3, H - 3.8))

    # Center divider cable pass-through window (Y=172..232, Z=56..118)
    cuts.append(box(DIV_X1 - 1.0, 172.0, 56.0, DIV_X2 + 1.0, 232.0, 118.0))

    # Bottom ventilation slots (clear of ASM1166, Pico PSU, rear foot pockets X>=160, and rear boss pedestal Y>=282)
    for yy in range(170, 254, 12):
        cuts.append(box(18.0, float(yy), -1.0, 44.0, float(yy + 6), T + 1.0))
    for yy in range(256, 278, 12):
        cuts.append(box(68.0, float(yy), -1.0, 154.0, float(yy + 6), T + 1.0))

    # Pico PSU zip-tie slots
    cuts.append(box(122.0, 184.0, -1.0, 148.0, 188.0, T + 1.0))
    cuts.append(box(122.0, 238.0, -1.0, 148.0, 242.0, T + 1.0))

    # Rear rubber-foot pockets (Ø12 x 2mm deep)
    cuts.append(cyl_z(16.0, 274.0, -1.0, 2.0, 6.0))
    cuts.append(cyl_z(166.0, 274.0, -1.0, 2.0, 6.0))

    # Standoff pilot holes (Ø2.6mm)
    for sx, sy in asm_pts + pico_pts:
        cuts.append(cyl_z(sx, sy, T + 1.0, 11.0, 1.3))

    # Left cover M3 insert holes (Y=276 clears rear panel inserts at Y=282.5..290)
    for cy, cz in ((163.0, 8.0), (163.0, 164.0), (276.0, 8.0), (276.0, 164.0)):
        cuts.append(cyl_x(T - 1.0, T + 7.0, cy, cz, PARAMS["M3_INSERT_D"] * 0.5))

    # Mating lug M3 insert holes
    for _, _, _, _, hx, hz in mating_lugs:
        cuts.append(cyl_y(hx, y1 - 1.0, y1 + 7.5, hz, PARAMS["M3_INSERT_D"] * 0.5))

    # Rear panel M3 insert holes
    for bx, bz in rear_bosses:
        cuts.append(cyl_y(bx, y2 - 7.5, y2 + 1.0, bz, PARAMS["M3_INSERT_D"] * 0.5))

    return base.cut(Part.makeCompound(cuts))


# ==============================================================================
# 2. PANELS & THINKBOX BEZEL
# ==============================================================================
def build_front_bezel():
    W = PARAMS["TOTAL_W"]
    H = PARAMS["TOTAL_H"]
    BD = PARAMS["BEZEL_D"]  # 6.0

    bezel = box(0.0, 0.0, 0.0, W, BD, H)

    # Subtle 2mm outer chamfer on front edges
    front_edges = [
        e for e in bezel.Edges
        if abs(e.BoundBox.YMin) < 0.01 and abs(e.BoundBox.YMax) < 0.01
    ]
    if front_edges:
        bezel = bezel.makeChamfer(2.0, front_edges)

    cuts = [
        # Right 4-bay HDD window cutout
        box(61.5, -1.0, 27.5, 172.5, BD + 1.0, 162.5),
        # Decorative 1.5mm stepped frame around 4-bay window
        box(58.5, -1.0, 24.5, 175.5, 1.5, 165.5),
        # Left I/O & power strip cutouts
        cyl_y(19.0, -1.0, BD + 1.0, 152.0, 6.1),           # Power button Ø12.2
        cyl_y(19.0, -1.0, BD + 1.0, 138.0, 1.6),           # Power LED Ø3.2
        box(12.0, -1.0, 118.5, 26.0, BD + 1.0, 125.5),     # Front USB-A
        box(14.0, -1.0, 105.75, 24.0, BD + 1.0, 110.25),   # Front USB-C
        # ThinkPad red accent recess (Y=0..4)
        box(10.0, -1.0, 82.0, 28.0, 4.0, 92.0),
    ]

    # Perforated vertical airflow mesh (Ø3.6mm staggered pitch)
    pitch = 5.6
    r_mesh = 1.8
    # Column 1: X=31..49, Z=10..162
    row = 0
    z = 12.0
    while z <= 160.0:
        x_off = 2.8 if (row % 2 == 1) else 0.0
        x = 32.5 + x_off
        while x <= 48.0:
            cuts.append(cyl_y(x, -1.0, BD + 1.0, z, r_mesh))
            x += pitch
        z += pitch * 0.866
        row += 1

    # Column 2 below red accent: X=10..28, Z=10..78
    row = 0
    z = 12.0
    while z <= 76.0:
        x_off = 2.8 if (row % 2 == 1) else 0.0
        x = 11.5 + x_off
        while x <= 27.0:
            cuts.append(cyl_y(x, -1.0, BD + 1.0, z, r_mesh))
            x += pitch
        z += pitch * 0.866
        row += 1

    # 4 corner mounting holes + front countersinks
    for bx, bz in ((8.0, 8.0), (8.0, 164.0), (173.0, 14.0), (54.0, 164.0)):
        cuts.append(cyl_y(bx, -1.0, BD + 1.0, bz, PARAMS["M3_CLEAR_D"] * 0.5))
        cuts.append(Part.makeCone(
            PARAMS["M3_CSINK_D"] * 0.5, PARAMS["M3_CLEAR_D"] * 0.5, 2.2,
            App.Vector(bx, 0.0, bz), App.Vector(0, 1, 0)
        ))

    return bezel.cut(Part.makeCompound(cuts))


def build_red_accent():
    return box(10.2, 0.0, 82.2, 27.8, 3.8, 91.8)


def build_thinkbox_text():
    """Create raised THINKBOX lettering using Arial Bold with proper Bullseye hollow faces."""
    try:
        wire_groups = Part.makeWireString("THINKBOX", "C:/Windows/Fonts/", "arialbd.ttf", 11.0)
        solids = []
        for glyph_wires in wire_groups:
            if not glyph_wires:
                continue
            face = Part.makeFace(glyph_wires, "Part::FaceMakerBullseye")
            # Rotate from XY plane into XZ plane (normal pointing -Y)
            face.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 90.0)
            solid = face.extrude(App.Vector(0, -1.2, 0))
            solids.append(solid)
        comp = Part.makeCompound(solids)
        bb = comp.BoundBox
        target_cx = 117.0
        target_cz = 14.0
        dx = target_cx - 0.5 * (bb.XMin + bb.XMax)
        dz = target_cz - 0.5 * (bb.ZMin + bb.ZMax)
        dy = -bb.YMax  # sits flush on Y=0, protrudes to Y=-1.2
        comp.translate(App.Vector(dx, dy, dz))
        return comp
    except Exception as exc:
        print(f"Warning: THINKBOX text fallback triggered: {exc}")
        return box(75.0, -1.2, 11.0, 159.0, 0.0, 17.0)


def build_rear_panel():
    W = PARAMS["TOTAL_W"]
    H = PARAMS["TOTAL_H"]
    y1 = PARAMS["SPLIT_Y"] + PARAMS["CHASSIS_REAR_D"]  # 290.0
    y2 = y1 + PARAMS["REAR_PANEL_D"]                   # 294.0
    fcx = PARAMS["FAN_CX"]                             # 117.0
    fcz = PARAMS["FAN_CZ"]                             # 90.0
    span_half = PARAMS["FAN_MOUNT_SPAN"] * 0.5         # 52.5

    panel = box(0.0, y1, 0.0, W, y2, H)

    cuts = [
        # 120mm fan circular bore
        cyl_y(fcx, y1 - 1.0, y2 + 1.0, fcz, PARAMS["FAN_BORE_D"] * 0.5),
        # L480 upper CPU exhaust louver slots (6x 32x4.5mm)
    ]
    for i in range(6):
        zz = 118.0 + i * 7.0
        cuts.append(box(12.0, y1 - 1.0, zz, 44.0, y2 + 1.0, zz + 4.5))

    # Mid auxiliary I/O cutout
    cuts.append(box(14.0, y1 - 1.0, 68.0, 42.0, y2 + 1.0, 106.0))
    # Cat6 RJ45 Ethernet cutout
    cuts.append(box(12.0, y1 - 1.0, 38.0, 28.5, y2 + 1.0, 55.5))
    # USB-C 65W charger pass-through
    cuts.append(box(31.0, y1 - 1.0, 42.0, 47.0, y2 + 1.0, 52.0))
    # 12V DC barrel jack hole (Ø12.2mm)
    cuts.append(cyl_y(28.0, y1 - 1.0, y2 + 1.0, 20.0, 6.1))

    # 4x 120mm fan mounting holes (105x105mm)
    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            cuts.append(cyl_y(fcx + sx * span_half, y1 - 1.0, y2 + 1.0, fcz + sz * span_half,
                              PARAMS["FAN_MOUNT_HOLE_D"] * 0.5))

    # 6x Rear panel M3 mounting holes
    for bx, bz in ((12.0, 16.0), (12.0, 160.0), (48.0, 16.0), (48.0, 160.0), (117.0, 16.0), (117.0, 162.0)):
        cuts.append(cyl_y(bx, y1 - 1.0, y2 + 1.0, bz, PARAMS["M3_CLEAR_D"] * 0.5))

    panel = panel.cut(Part.makeCompound(cuts))

    # Open protective fan grille (2 concentric rings + 4 radial spokes at Y=291.5..294)
    gy1, gy2 = y1 + 1.5, y2
    grille_parts = []
    for r_mid in (24.0, 42.0):
        ring = cyl_y(fcx, gy1, gy2, fcz, r_mid + 1.25).cut(cyl_y(fcx, gy1 - 1.0, gy2 + 1.0, fcz, r_mid - 1.25))
        grille_parts.append(ring)
    for ang in (45.0, 135.0):
        spoke = box(fcx - 58.0, gy1, fcz - 1.25, fcx + 58.0, gy2, fcz + 1.25)
        spoke.rotate(App.Vector(fcx, gy1, fcz), App.Vector(0, 1, 0), ang)
        grille_parts.append(spoke)

    for gp in grille_parts:
        panel = panel.fuse(gp)
    return panel


def build_left_cover(y1, y2, hole_ys):
    T = PARAMS["WALL_THICK"]
    H = PARAMS["TOTAL_H"]
    cover = box(0.0, y1, T, T, y2, H - T)
    cuts = []
    # Horizontal intake vent slots over L480 motherboard
    for zz in range(38, 138, 12):
        cuts.append(box(-1.0, y1 + 18.0, float(zz), T + 1.0, y2 - 18.0, float(zz + 5)))
    # 4 corner M3 mounting holes
    for hy in hole_ys:
        for hz in (8.0, 164.0):
            cuts.append(cyl_x(-1.0, T + 1.0, hy, hz, PARAMS["M3_CLEAR_D"] * 0.5))
    return cover.cut(Part.makeCompound(cuts))


# ==============================================================================
# 3. 3.5" HDD REMOVABLE TRAYS
# ==============================================================================
def build_hdd_tray(bay_idx):
    """bay_idx: 0 (bottom, HDD_Tray_4) .. 3 (top, HDD_Tray_1)."""
    T = PARAMS["WALL_THICK"]
    zb = T + PARAMS["CHIN_H"] + bay_idx * PARAMS["HDD_BAY_PITCH"]
    z0 = zb + PARAMS["RAIL_TOP_T"] + PARAMS["TRAY_Z_CLEAR"]  # zb + 2.7

    cx1 = 62.8
    cx2 = cx1 + PARAMS["TRAY_CRADLE_W"]  # 171.2
    cy1 = PARAMS["TRAY_CRADLE_Y_START"]  # 6.0
    cy2 = PARAMS["TRAY_CRADLE_Y_END"]    # 153.8
    wt = PARAMS["TRAY_WALL_T"]           # 3.0
    ft = PARAMS["TRAY_FLOOR_T"]          # 2.5
    wh = PARAMS["TRAY_WALL_H"]           # 16.5

    fx1 = 62.0
    fx2 = fx1 + PARAMS["TRAY_FACE_W"]    # 172.0
    fy1 = PARAMS["TRAY_FACE_Y_START"]    # 1.0
    fy2 = PARAMS["TRAY_FACE_Y_END"]      # 6.0
    fz1 = z0 - 0.5
    fz2 = z0 + 29.8

    # Base cradle + walls + front sled face
    floor = box(cx1, cy1, z0, cx2, cy2, z0 + ft)
    lwall = box(cx1, cy1, z0 + ft, cx1 + wt, cy2, z0 + wh)
    rwall = box(cx2 - wt, cy1, z0 + ft, cx2, cy2, z0 + wh)
    face = box(fx1, fy1, fz1, fx2, fy2, fz2)

    tray = floor.fuse(lwall).fuse(rwall).fuse(face)

    cuts = []
    # Floor cooling vent windows
    for vy1, vy2 in ((20.0, 56.0), (66.0, 102.0), (112.0, 144.0)):
        cuts.append(box(74.0, vy1, z0 - 1.0, 160.0, vy2, z0 + ft + 1.0))

    # SFF-8301 side mounting holes + outer 1.5mm counterbore
    hz = z0 + ft + PARAMS["HDD_HOLE_Z_OFFSET"]
    for dist_from_rear in PARAMS["HDD_HOLE_FROM_REAR"]:
        hy = 153.5 - dist_from_rear
        # Left wall
        cuts.append(cyl_x(cx1 - 1.0, cx1 + wt + 1.0, hy, hz, PARAMS["SCREW_6_32_D"] * 0.5))
        cuts.append(cyl_x(cx1 - 0.5, cx1 + 1.5, hy, hz, PARAMS["SCREW_6_32_HEAD_D"] * 0.5))
        # Right wall
        cuts.append(cyl_x(cx2 - wt - 1.0, cx2 + 1.0, hy, hz, PARAMS["SCREW_6_32_D"] * 0.5))
        cuts.append(cyl_x(cx2 - 1.5, cx2 + 0.5, hy, hz, PARAMS["SCREW_6_32_HEAD_D"] * 0.5))

    # Front sled styling: finger pull pocket, indicator ring groove, intake grid, badge recess
    # Left handle pocket (2.0mm deep, floor at Y=3.0) + recessed Ø16/Ø12mm circular ring groove (1.2mm deep, Y=3.0..4.2)
    cuts.append(box(64.5, fy1 - 0.5, fz1 + 3.5, 84.5, fy1 + 2.0, fz2 - 3.5))
    rcx = 74.5
    rcz = 0.5 * (fz1 + fz2)
    ring_groove = cyl_y(rcx, fy1 + 1.5, fy1 + 3.2, rcz, 8.0).cut(
        cyl_y(rcx, fy1 + 1.0, fy1 + 3.7, rcz, 6.0)
    )
    cuts.append(ring_groove)
    # Front airflow slot grid across middle (X=88..152)
    for gx in range(90, 152, 8):
        for gz_off in (5.0, 16.0):
            cuts.append(box(float(gx), fy1 - 1.0, fz1 + gz_off, float(gx + 5), fy2 + 1.0, fz1 + gz_off + 9.0))
    # Right badge recess
    cuts.append(box(156.0, fy1 - 0.5, fz1 + 5.0, 169.0, fy1 + 1.6, fz2 - 5.0))

    return tray.cut(Part.makeCompound(cuts))


# ==============================================================================
# 4. REFERENCE HARDWARE MOCKUPS
# ==============================================================================
def build_ref_l480():
    pcb = box(PARAMS["L480_PCB_X"], PARAMS["L480_Y_START"], PARAMS["L480_Z_START"],
              PARAMS["L480_PCB_X"] + PARAMS["L480_PCB_T"], PARAMS["L480_Y_END"], PARAMS["L480_Z_END"])
    heatsink = box(24.0, 140.0, 85.0, 44.0, 255.0, 142.0)
    ram1 = box(38.0, 75.0, 40.0, 44.0, 145.0, 56.0)
    ram2 = box(38.0, 75.0, 62.0, 44.0, 145.0, 78.0)
    ssd = box(40.0, 40.0, 95.0, 44.0, 82.0, 117.0)
    return Part.makeCompound([pcb, heatsink, ram1, ram2, ssd])


def build_ref_hdd(bay_idx):
    T = PARAMS["WALL_THICK"]
    zb = T + PARAMS["CHIN_H"] + bay_idx * PARAMS["HDD_BAY_PITCH"]
    z0 = zb + PARAMS["RAIL_TOP_T"] + PARAMS["TRAY_Z_CLEAR"]
    z_bot = z0 + PARAMS["TRAY_FLOOR_T"]
    return box(66.2, 6.5, z_bot, 66.2 + PARAMS["HDD_W"], 6.5 + PARAMS["HDD_D"], z_bot + PARAMS["HDD_H"])


def build_ref_fan_120():
    fcx = PARAMS["FAN_CX"]
    fcz = PARAMS["FAN_CZ"]
    half = PARAMS["FAN_SIZE"] * 0.5
    y1 = 264.5
    y2 = y1 + PARAMS["FAN_THICK"]
    frame = box(fcx - half, y1, fcz - half, fcx + half, y2, fcz + half)
    bore = cyl_y(fcx, y1 - 1.0, y2 + 1.0, fcz, PARAMS["FAN_BORE_D"] * 0.5)
    hub = cyl_y(fcx, y1 + 2.0, y2 - 2.0, fcz, 21.0)
    return frame.cut(bore).fuse(hub)


def build_ref_asm1166():
    pcb = box(64.0, 172.0, 10.0, 86.0, 252.0, 14.0)
    sata_ports = box(68.0, 180.0, 14.0, 82.0, 244.0, 24.0)
    return Part.makeCompound([pcb, sata_ports])


def build_ref_picopsu():
    return box(108.0, 192.0, 10.0, 162.0, 234.0, 30.0)


# ==============================================================================
# MAIN BUILDER
# ==============================================================================
def build_all():
    if DOC_NAME in App.listDocuments():
        App.closeDocument(DOC_NAME)
    doc = App.newDocument(DOC_NAME)

    make_spreadsheet(doc)

    g_chassis = doc.addObject("App::DocumentObjectGroup", "01_Chassis")
    g_panels = doc.addObject("App::DocumentObjectGroup", "02_Panels_and_Bezel")
    g_trays = doc.addObject("App::DocumentObjectGroup", "03_HDD_Trays")
    g_refs = doc.addObject("App::DocumentObjectGroup", "04_Reference_Hardware")

    # 1. Chassis
    add_part(doc, g_chassis, "Chassis_Front", build_chassis_front(), (0.14, 0.14, 0.15))
    add_part(doc, g_chassis, "Chassis_Rear", build_chassis_rear(), (0.14, 0.14, 0.15))

    # 2. Panels & Bezel
    add_part(doc, g_panels, "Front_Bezel", build_front_bezel(), (0.10, 0.10, 0.11))
    add_part(doc, g_panels, "ThinkPad_Red_Accent", build_red_accent(), (0.85, 0.08, 0.08))
    add_part(doc, g_panels, "Front_Bezel_Text", build_thinkbox_text(), (0.76, 0.56, 0.32))
    add_part(doc, g_panels, "Rear_Panel", build_rear_panel(), (0.14, 0.14, 0.15))
    add_part(doc, g_panels, "Left_Cover_Front",
             build_left_cover(6.0, 158.0, (20.0, 153.0)), (0.14, 0.14, 0.15))
    add_part(doc, g_panels, "Left_Cover_Rear",
             build_left_cover(158.0, 290.0, (163.0, 276.0)), (0.14, 0.14, 0.15))

    # 3. 4x HDD Trays (HDD_Tray_1 top .. HDD_Tray_4 bottom)
    for idx in range(4):
        tray_num = 4 - idx
        add_part(doc, g_trays, f"HDD_Tray_{tray_num}", build_hdd_tray(idx), (0.20, 0.21, 0.23))

    # 4. Reference Hardware Mockups
    add_part(doc, g_refs, "Ref_L480_Motherboard", build_ref_l480(), (0.12, 0.45, 0.22), transparency=55)
    for idx in range(4):
        hdd_num = 4 - idx
        add_part(doc, g_refs, f"Ref_HDD_{hdd_num}", build_ref_hdd(idx), (0.65, 0.68, 0.72), transparency=60)
    add_part(doc, g_refs, "Ref_Fan_120mm", build_ref_fan_120(), (0.58, 0.44, 0.32), transparency=55)
    add_part(doc, g_refs, "Ref_ASM1166_SATA", build_ref_asm1166(), (0.15, 0.35, 0.55), transparency=55)
    add_part(doc, g_refs, "Ref_PicoPSU", build_ref_picopsu(), (0.65, 0.50, 0.15), transparency=55)

    doc.recompute()
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    doc.saveAs(SAVE_PATH)
    print(f"Saved {DOC_NAME} to {SAVE_PATH}")

    os.makedirs(STL_DIR, exist_ok=True)
    for obj_name, stl_name in EXPORT_PARTS:
        obj = doc.getObject(obj_name)
        if obj is None:
            raise RuntimeError(f"Missing object for STL export: {obj_name}")
        mesh = MeshPart.meshFromShape(
            Shape=obj.Shape,
            LinearDeflection=0.1,
            AngularDeflection=0.35,
            Relative=False,
        )
        stl_path = os.path.join(STL_DIR, stl_name)
        mesh.write(stl_path)
    print(f"Exported {len(EXPORT_PARTS)} STL files to {STL_DIR}")
    return doc


if __name__ == "__main__":
    build_all()
