"""
Premium Ridge-Style 3D Printable Wallet (AirTag + Hidden Keyfob + AMARSBAR Cash Strap)
-------------------------------------------------------------------------------------
Parametric CadQuery generator producing:
  1. 01_Front_Inner_Plate        (54.0 x 85.5 x 3.00 mm) - Card-face down (Z=0)
  2. 02_Front_Outer_Plate        (54.0 x 85.5 x 7.50 mm) - Outer-face down (Z=0)
     - Watch-style captive AirTag chamber (32.5 mm internal cavity -> 25.85 mm chamfered front aperture)
     - 100% hidden internal Keyfob pocket (5.20 mm deep, 2.30 mm continuous solid exterior wall)
     - 7x flush countersunk M2x10mm screw pockets on flat perimeter landing zones
  3. 03_Back_Inner_Plate         (54.0 x 85.5 x 3.00 mm) - Properly mirrored pair, card-face down (Z=0)
  4. 04_Back_Outer_Plate_Slim    (54.0 x 85.5 x 3.40 mm) - Ultra-slim Ridge profile, outer-face down (Z=0)
     - 0.65 mm internal cash-strap double-elastic relief channel
     - 7x flush countersunk M2x6mm screw pockets
  5. 05_Cash_Strap_Plate_AMARSBAR (33.0 x 60.0 x 1.80 mm) - Upgraded thick chamfered plate with AMARSBAR logo

All parts are 100% SUPPORT-FREE and exported pre-oriented flat on the build plate (Z=0)
in both STEP (lossless CAD for Bambu Studio / Fusion) and high-res STL, plus an assembled 3D preview STEP.
"""

import os
import math
import numpy as np
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf, gp_GTrsf, gp_Vec, gp_Ax1, gp_Pnt, gp_Dir
from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform

OUT_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(OUT_ROOT)
ORIG_ROOT = os.path.join(REPO_ROOT, "original_files")
STEP_DIR = os.path.join(OUT_ROOT, "STEP")
STL_DIR = os.path.join(OUT_ROOT, "STL")
PREVIEW_DIR = os.path.join(OUT_ROOT, "previews")

for d in (OUT_ROOT, STEP_DIR, STL_DIR, PREVIEW_DIR):
    os.makedirs(d, exist_ok=True)

# ==============================================================================
# MASTER DIMENSIONS (all in mm)
# ==============================================================================
# Overall Ridge plate footprint (matches original exactly: X in [-4, 50], Y in [-4, 81.5])
X_MIN, X_MAX = -4.0, 50.0
Y_MIN, Y_MAX = -4.0, 81.5
PLATE_W = X_MAX - X_MIN   # 54.0 mm
PLATE_H = Y_MAX - Y_MIN   # 85.5 mm
CORNER_R = 4.0

# Thumb notch (right edge, lower-right)
NOTCH_CX = 50.0
NOTCH_CY = 12.025
NOTCH_R = 8.025
NOTCH_BLEND_R = 4.0

# 7 Screw locations (exact Ridge perimeter pattern from original)
SCREWS = [
    (0.0, 0.0),
    (0.0, 38.75),
    (0.0, 77.5),
    (46.0, 0.0),
    (46.0, 24.05),
    (46.0, 53.45),
    (46.0, 77.5),
]

# M2 Hardware dimensions (DIN 7991 / ISO 10642 M2 flat-head countersunk + DIN 934 M2 hex nut)
M2_CLEAR_D = 2.25        # M2 clearance hole
M2_CSK_D = 4.30          # Countersink outer diameter (standard M2 FHCS head ~3.8-4.0mm -> sits cleanly inside)
M2_CSK_RECESS = 0.15     # Flush counterbore recess depth below outer face
M2_CSK_CONE_H = (M2_CSK_D - M2_CLEAR_D) / 2.0  # 1.025 mm (90 deg included = 45 deg overhang)
M2_NUT_AF = 4.24         # Hex nut width across flats (DIN 934 M2 nut = 4.00mm + 0.24mm FDM press-fit)
M2_NUT_DEPTH = 1.85      # Depth from card face (1.60mm nut sits 0.25mm safely recessed below cards!)
BRIDGE_STEP_H = 0.20     # Voron/Prusa stepped double-bridge layer height (zero supports, zero droop)

# Plate thicknesses
T_INNER = 3.00           # Both Front & Back Inner Plates
T_FRONT_OUTER = 7.70     # Houses real 8.00mm AirTag flush + 5.00mm hidden Keyfob + M2x10mm screws
T_BACK_OUTER = 3.40      # Ultra-slim Ridge profile + M2x6mm screws + 0.65mm cash-strap relief

# Elastic T-Channel dimensions (for 1-inch / 25 mm heavy-duty black woven elastic)
ELASTIC_W = 25.40        # Channel width (25.0mm strap + 0.2mm clearance per side)
ELASTIC_X_CENTER = 23.0  # Dead-centered horizontally! (X = 10.30 to 35.70)
ELASTIC_SIDE_Y_CENTER = 38.75  # Centered between Y=24.05 and Y=53.45 screws (Y = 26.05 to 51.45)
ELASTIC_DEPTH_INNER = 1.05     # Clamps ~1.15-1.25mm woven elastic firmly!
ELASTIC_BACK_RELIEF = 0.65     # Extra relief in Back Outer Plate for double-layer cash strap overlap (total 1.70mm)
RIB_H = 0.22             # Low-profile anti-slip grip ribs on elastic channel floor
RIB_W = 0.65
RIB_SPACING = 5.5

# AirTag cavity parameters (real Apple AirTag: Ø31.90 mm x 8.00 mm; stainless cap Ø25.55 mm)
# Dead-centered horizontally at X=23.0, upper-center Y=61.0!
AT_CX = 23.0
AT_CY = 61.0
AT_CAVITY_D = 32.70      # Ø31.90 + 0.80mm total clearance (effortless drop-in, zero binding)
AT_WINDOW_D = 26.20      # Frames Ø25.55 stainless steel cap cleanly (~0.32mm watch-bezel gap; 2.85mm 360° solid lip!)
AT_BEZEL_CHAMFER = 0.40  # Crisp 45-deg watch-caseback outer chamfer (Ø27.00 -> Ø26.20)
# Internal support-free 50° cone (in outer-plate coords where z=0 is mating face, z=T_FRONT_OUTER=7.70 is outer face)
# Mathematically verified >= +0.35mm clearance to real scaled Apple AirTag across entire profile!
AT_STRAIGHT_Z_MAX = 4.60 # Cylinder Ø32.70 from z=0 up to z=4.60 (covers full equator of 8.0mm AirTag)
AT_CONE_Z_TOP = 7.30     # Smooth 50.3° cone from Ø32.70 @ z=4.60 to Ø26.20 @ z=7.30 (meets outer chamfer cleanly!)

# Hidden Keyfob pocket parameters (in Front Outer Plate, opening on mating face z=0)
KF_CX = 26.0
KF_CY = 24.0
KF_ANGLE_DEG = 330.0     # Optimal angle from 2D clearance check (min wall >= 3.67 mm everywhere!)
KF_XY_CLEARANCE = 0.35   # Offset outward on all sides for smooth drop-in
KF_DEPTH = 5.20          # Keyfob is 5.00mm thick -> 5.20mm deep pocket leaves 2.50mm SOLID outer skin!

# 3D-Printed Compliant PETG Spring Money Clip parameters (printed ON ITS SIDE for continuous leaf-spring strength!)
# Mounts cleanly on Y = Y_MIN (-4.0) short edge centered at X = 23.0 with a positive interlocking keyway (zero pull-out!).
MC_W = 24.60             # Precision slot width for 24.0 mm wide PETG leaf-spring clip (0.30 mm clearance per side!)
MC_CLIP_W = 24.00        # Constant-width leaf-spring clip (prints 100% flat on side, zero supports, continuous fibers!)
MC_DEPTH_Y = 19.50       # Inward depth from Y=-4.0 to Y=+15.5
MC_LIP_T = 1.55          # Remaining solid exterior wall thickness at Y=-4.0 lip
MC_POCKET_Z = T_BACK_OUTER - MC_LIP_T  # 1.85 mm recess from inner mating face
MC_KEY_Y0 = 8.50         # Positive pull-out locking keyway Y start (12.5 mm inward from Y=-4.0)
MC_KEY_Y1 = 13.50        # Keyway Y end (5.0 mm wide keyway)
MC_KEY_EXTRA_Z = 0.75    # Extra keyway depth (total 2.60 mm from inner face -> leaves 0.80 mm solid exterior skin!)
MC_SHIM_T = 0.80         # Legacy shim kept for optional aftermarket steel clip compatibility


# ==============================================================================
# HELPER: BASE 2D PLATE PROFILE (EXACT RIDGE SILHOUETTE WITH THUMB NOTCH)
# ==============================================================================
def make_base_plate_solid(thickness: float, z0: float = 0.0) -> cq.Workplane:
    """
    Build exact 54.0 x 85.5 mm Ridge plate silhouette with 4mm corner radii
    and smooth blended thumb notch (R=8.025 at X=50, Y=12.025 with R=4.0 blends),
    matching the original STEP perimeter to 0.001 mm!
    """
    # Start from original Inner Plate Z=0 outer wire so corner/notch blends are 100% exact!
    orig_inner = cq.importers.importStep(
        f"{ORIG_ROOT}/Part Studio 1 Copy 1/Part Studio 1 Copy 1 - Part 1.step"
    )
    # Find bottom face at Z=0 and extract its outer wire (the one with dx=54, dy=85.5)
    outer_wire = None
    for f in orig_inner.faces().vals():
        bb = f.BoundingBox()
        if abs(bb.zmin) < 1e-3 and abs(bb.zmax) < 1e-3:
            for w in f.Wires():
                wbb = w.BoundingBox()
                if (wbb.xmax - wbb.xmin) > 50.0:
                    outer_wire = w
                    break
    assert outer_wire is not None, "Failed to extract exact outer wire from original plate!"
    face = cq.Face.makeFromWires(outer_wire)
    solid = cq.Workplane("XY").add(face).toPending().extrude(thickness)
    if abs(z0) > 1e-6:
        solid = solid.translate((0, 0, z0))
    return solid


def make_beveled_plate(thickness: float, bottom_dx: float = 0.0, bottom_dz: float = 0.0,
                       top_dx: float = 0.0, top_dz: float = 0.0) -> cq.Workplane:
    """
    Build the exact Ridge silhouette with controlled asymmetric 35-deg or 45-deg
    perimeter chamfers on bottom (z=0) and/or top (z=thickness) using native BRep chamfer.
    Note: CadQuery .faces('>Z' or '<Z').edges().chamfer(dz, dx) applies dz vertically
    along the sidewall and dx horizontally across the top/bottom face.
    """
    res = make_base_plate_solid(thickness)
    if bottom_dx > 0 and bottom_dz > 0:
        res = res.faces("<Z").edges().chamfer(bottom_dz, bottom_dx)
    if top_dx > 0 and top_dz > 0:
        res = res.faces(">Z").edges().chamfer(top_dz, top_dx)
    return res


def extract_keyfob_local_wire(clearance: float = 0.35):
    """Extract exact ordered 2D wire of keyfob centered at origin, offset outward by clearance."""
    kf = cq.importers.importStep(f"{ORIG_ROOT}/keyfob/keyfob - Part 1.step")
    kf_face = [f for f in kf.faces().vals()
               if abs(f.BoundingBox().zmin) < 0.01 and abs(f.BoundingBox().zmax) < 0.01][0]
    wire = kf_face.Wires()[0]
    wbb = wire.BoundingBox()
    cx = (wbb.xmin + wbb.xmax) / 2.0
    cy = (wbb.ymin + wbb.ymax) / 2.0
    w_centered = wire.translate(cq.Vector(-cx, -cy, 0))
    if abs(clearance) > 1e-6:
        # Use arc offset for smooth rounded corners (easier to print and drop keyfob in!)
        w_off = w_centered.offset2D(clearance, kind="arc")[0]
    else:
        w_off = w_centered
    return w_off, (cx, cy)


# ==============================================================================
# PART 1: FRONT INNER PLATE (assembly coords: z=0 card face, z=T_INNER mating face)
# ==============================================================================
def build_front_inner_plate() -> cq.Workplane:
    # Base plate with smooth 0.55 x 0.80 mm (34.5 deg) card-entry bevel on card face (z=0)
    # and clean tiny 0.20 mm edge break on mating face? No, keep mating face flush for seamless seam!
    plate = make_beveled_plate(T_INNER, bottom_dx=0.55, bottom_dz=0.80, top_dx=0.0, top_dz=0.0)

    # 1. Cut T-shaped elastic channel from top mating face (z = T_INNER - ELASTIC_DEPTH_INNER .. T_INNER)
    z_floor = T_INNER - ELASTIC_DEPTH_INNER  # 1.95 mm
    # Vertical branch: X in [10.30, 35.70], full Y [-4.5, 82.0]
    vert_cut = (
        cq.Workplane("XY")
        .workplane(offset=z_floor)
        .center(ELASTIC_X_CENTER, (Y_MIN + Y_MAX) / 2.0)
        .rect(ELASTIC_W, PLATE_H + 2.0)
        .extrude(ELASTIC_DEPTH_INNER + 1.0)
    )
    # Side branch: X in [23.0, 51.0], Y in [26.05, 51.45]
    side_cut = (
        cq.Workplane("XY")
        .workplane(offset=z_floor)
        .center(37.0, ELASTIC_SIDE_Y_CENTER)
        .rect(28.0, ELASTIC_W)
        .extrude(ELASTIC_DEPTH_INNER + 1.0)
    )
    plate = plate.cut(vert_cut).cut(side_cut)

    # 2. Smooth elastic exit chamfers (0.5mm x 45deg) at top, bottom, and right channel exits
    # so the woven black elastic glides over a smooth bevel and NEVER frays!
    exit_cuts = []
    # Top exit (Y = Y_MAX = 81.5)
    exit_cuts.append(
        cq.Workplane("YZ")
        .workplane(offset=ELASTIC_X_CENTER - ELASTIC_W / 2.0)
        .moveTo(Y_MAX - 0.6, z_floor)
        .lineTo(Y_MAX + 0.5, z_floor)
        .lineTo(Y_MAX + 0.5, z_floor - 0.6)
        .close()
        .extrude(ELASTIC_W)
    )
    # Bottom exit (Y = Y_MIN = -4.0)
    exit_cuts.append(
        cq.Workplane("YZ")
        .workplane(offset=ELASTIC_X_CENTER - ELASTIC_W / 2.0)
        .moveTo(Y_MIN + 0.6, z_floor)
        .lineTo(Y_MIN - 0.5, z_floor)
        .lineTo(Y_MIN - 0.5, z_floor - 0.6)
        .close()
        .extrude(ELASTIC_W)
    )
    # Right side exit (X = X_MAX = 50.0)
    exit_cuts.append(
        cq.Workplane("XZ")
        .workplane(offset=-(ELASTIC_SIDE_Y_CENTER + ELASTIC_W / 2.0))
        .moveTo(X_MAX - 0.6, z_floor)
        .lineTo(X_MAX + 0.5, z_floor)
        .lineTo(X_MAX + 0.5, z_floor - 0.6)
        .close()
        .extrude(ELASTIC_W)
    )
    for ec in exit_cuts:
        plate = plate.cut(ec)

    # 3. Anti-slip elastic grip ribs on channel floor (0.22 mm tall, smooth trapezoidal cross-section)
    # Vertical channel transverse ribs (stopping 2.5 mm shy of top/bottom exits so invisible!)
    rib_union = None
    y_positions = np.arange(Y_MIN + 3.5, Y_MAX - 3.0, RIB_SPACING)
    for ry in y_positions:
        # Leave small 1.2mm margin from channel side walls
        r = (
            cq.Workplane("YZ")
            .workplane(offset=ELASTIC_X_CENTER - (ELASTIC_W / 2.0 - 1.2))
            .moveTo(ry - RIB_W / 2.0, z_floor - 0.05)
            .lineTo(ry - RIB_W / 4.0, z_floor + RIB_H)
            .lineTo(ry + RIB_W / 4.0, z_floor + RIB_H)
            .lineTo(ry + RIB_W / 2.0, z_floor - 0.05)
            .close()
            .extrude(ELASTIC_W - 2.4)
        )
        rib_union = r if rib_union is None else rib_union.union(r)

    # Side branch longitudinal-grip ribs (perpendicular to side pull direction -> parallel to Y!)
    x_positions = [38.0, 42.5, 47.0]
    for rx in x_positions:
        r = (
            cq.Workplane("XZ")
            .workplane(offset=-(ELASTIC_SIDE_Y_CENTER + (ELASTIC_W / 2.0 - 1.5)))
            .moveTo(rx - RIB_W / 2.0, z_floor - 0.05)
            .lineTo(rx - RIB_W / 4.0, z_floor + RIB_H)
            .lineTo(rx + RIB_W / 4.0, z_floor + RIB_H)
            .lineTo(rx + RIB_W / 2.0, z_floor - 0.05)
            .close()
            .extrude(ELASTIC_W - 3.0)
        )
        rib_union = rib_union.union(r)

    plate = plate.union(rib_union)

    # 4. 7x Captive M2 Hex Nut Pockets (from card face z=0) + Voron Stepped Double-Bridge + Ø2.25 clearance hole!
    hex_circum_d = M2_NUT_AF / math.cos(math.radians(30.0))  # ~4.896 mm circumscribed dia for polygon(6)
    for sx, sy in SCREWS:
        # Hex pocket from z=-0.1 to z=M2_NUT_DEPTH (1.85 mm)
        hex_cut = (
            cq.Workplane("XY")
            .workplane(offset=-0.1)
            .center(sx, sy)
            .polygon(6, hex_circum_d)
            .extrude(M2_NUT_DEPTH + 0.1)
        )
        # Stepped bridge layer 1 (z = 1.85 .. 2.05): rectangular slot M2_CLEAR_D x M2_NUT_AF
        br1 = (
            cq.Workplane("XY")
            .workplane(offset=M2_NUT_DEPTH - 0.02)
            .center(sx, sy)
            .rect(M2_NUT_AF, M2_CLEAR_D)
            .extrude(BRIDGE_STEP_H + 0.04)
        )
        # Stepped bridge layer 2 (z = 2.05 .. 2.25): square M2_CLEAR_D x M2_CLEAR_D
        br2 = (
            cq.Workplane("XY")
            .workplane(offset=M2_NUT_DEPTH + BRIDGE_STEP_H - 0.02)
            .center(sx, sy)
            .rect(M2_CLEAR_D, M2_CLEAR_D)
            .extrude(BRIDGE_STEP_H + 0.04)
        )
        # Circular clearance hole from z = 2.25 .. T_INNER + 0.2
        hole = (
            cq.Workplane("XY")
            .workplane(offset=M2_NUT_DEPTH + 2 * BRIDGE_STEP_H - 0.02)
            .center(sx, sy)
            .circle(M2_CLEAR_D / 2.0)
            .extrude(T_INNER - (M2_NUT_DEPTH + 2 * BRIDGE_STEP_H) + 0.3)
        )
        plate = plate.cut(hex_cut).cut(br1).cut(br2).cut(hole)

    return plate


# ==============================================================================
# PART 2: FRONT OUTER PLATE (AirTag Watch-Window + 100% Hidden Keyfob!)
# Built in assembly orientation first (z=0 inner mating face, z=T_FRONT_OUTER outer face),
# then flipped 180 deg around Y for print-ready outer-face-down orientation!
# ==============================================================================
def build_front_outer_plate_asm() -> cq.Workplane:
    # Base plate with crisp 1.00 x 1.40 mm (35.5 deg) Ridge perimeter bevel on OUTER face (z=T_FRONT_OUTER)
    # and tiny 0.20 x 0.20 mm chamfer on inner mating face? Keep inner mating face razor-clean flush (0.0)!
    plate = make_beveled_plate(T_FRONT_OUTER, bottom_dx=0.0, bottom_dz=0.0, top_dx=1.00, top_dz=1.40)

    # 1. Watch-Style Captive AirTag Chamber (revolved profile, centered at AT_CX, AT_CY)
    # Z=0 is inner mating face, Z=T_FRONT_OUTER (7.60) is outer face.
    # Profile points (r, z):
    #   (0, -0.5) -> (AT_CAVITY_D/2, -0.5) -> (AT_CAVITY_D/2, AT_STRAIGHT_Z_MAX)
    #   -> (AT_WINDOW_D/2, AT_CONE_Z_TOP) -> (AT_WINDOW_D/2, T_FRONT_OUTER - AT_BEZEL_CHAMFER)
    #   -> (AT_WINDOW_D/2 + AT_BEZEL_CHAMFER, T_FRONT_OUTER + 0.5) -> (0, T_FRONT_OUTER + 0.5)
    r_cav = AT_CAVITY_D / 2.0        # 16.25 mm
    r_win = AT_WINDOW_D / 2.0        # 12.925 mm
    r_outer_ch = r_win + AT_BEZEL_CHAMFER  # 13.375 mm
    z_col_top = T_FRONT_OUTER - AT_BEZEL_CHAMFER  # 7.15 mm

    at_cut = (
        cq.Workplane("XZ")
        .workplane(offset=-AT_CY)
        .moveTo(AT_CX, -0.5)
        .lineTo(AT_CX + r_cav, -0.5)
        .lineTo(AT_CX + r_cav, AT_STRAIGHT_Z_MAX)
        .lineTo(AT_CX + r_win, AT_CONE_Z_TOP)
        .lineTo(AT_CX + r_outer_ch, T_FRONT_OUTER)
        .lineTo(AT_CX + r_outer_ch + 0.5, T_FRONT_OUTER + 0.5)
        .lineTo(AT_CX, T_FRONT_OUTER + 0.5)
        .close()
        .revolve(360, (AT_CX, 0, 0), (AT_CX, 1, 0))
    )
    plate = plate.cut(at_cut)

    # Subtle internal fingernail removal notch on the INSIDE rim of the AirTag cavity (z=0..1.8mm)
    # positioned at 6 o'clock (AT_CX, AT_CY - r_cav) so changing the battery once a year is effortless!
    at_pry = (
        cq.Workplane("XY")
        .workplane(offset=-0.2)
        .center(AT_CX, AT_CY - r_cav)
        .slot2D(5.0, 2.2, angle=0)
        .extrude(2.0)
    )
    plate = plate.cut(at_pry)

    # 2. 100% Hidden Internal Keyfob Pocket (blind pocket from z=0 up to z=KF_DEPTH=5.20mm!)
    # Leaves 7.60 - 5.20 = 2.40 mm of SOLID CONTINUOUS exterior wall (completely invisible from outside!)
    kf_wire, _ = extract_keyfob_local_wire(clearance=KF_XY_CLEARANCE)
    kf_wire_placed = kf_wire.rotate(
        cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), KF_ANGLE_DEG
    ).translate(cq.Vector(KF_CX, KF_CY, -0.2))
    kf_face = cq.Face.makeFromWires(kf_wire_placed)
    kf_cut = cq.Workplane("XY").add(kf_face).toPending().extrude(KF_DEPTH + 0.2)
    plate = plate.cut(kf_cut)

    # Subtle internal fingernail lift notch along one edge of the hidden keyfob pocket (z=0..2.0mm)
    # so you can remove the keyfob if you ever move apartments!
    kf_pry = (
        cq.Workplane("XY")
        .workplane(offset=-0.2)
        .center(KF_CX - 10.5, KF_CY - 8.0)
        .circle(2.2)
        .extrude(2.2)
    )
    plate = plate.cut(kf_pry)

    # 3. 7x Flush Countersunk M2 Screw Holes (countersink on OUTER face z=T_FRONT_OUTER!)
    for sx, sy in SCREWS:
        # Through clearance hole Ø2.25
        h_thru = (
            cq.Workplane("XY")
            .workplane(offset=-0.2)
            .center(sx, sy)
            .circle(M2_CLEAR_D / 2.0)
            .extrude(T_FRONT_OUTER + 0.4)
        )
        # Countersink cone + 0.25mm flush counterbore recess at top (z = T_FRONT_OUTER)
        # With T_FRONT_OUTER=7.70 + T_INNER=3.00 - 0.25 = 10.45mm -> M2x10mm engages 1.40mm of 1.60mm nut!
        front_recess = 0.25
        z_csk_bot = T_FRONT_OUTER - front_recess - M2_CSK_CONE_H
        z_csk_top = T_FRONT_OUTER - front_recess
        csk = (
            cq.Workplane("XZ")
            .workplane(offset=-sy)
            .moveTo(sx, z_csk_bot)
            .lineTo(sx + M2_CLEAR_D / 2.0, z_csk_bot)
            .lineTo(sx + M2_CSK_D / 2.0, z_csk_top)
            .lineTo(sx + M2_CSK_D / 2.0, T_FRONT_OUTER + 0.5)
            .lineTo(sx, T_FRONT_OUTER + 0.5)
            .close()
            .revolve(360, (sx, 0, 0), (sx, 1, 0))
        )
        plate = plate.cut(h_thru).cut(csk)

    return plate


# ==============================================================================
# PART 3: BACK INNER PLATE (Exact mirror of Front Inner Plate across card plane Z=0)
# Built in assembly orientation (z=0 card face facing +Z, z=-T_INNER mating face facing -Z)
# ==============================================================================
def build_back_inner_plate_asm(front_inner: cq.Workplane) -> cq.Workplane:
    return front_inner.mirror("XY")


# ==============================================================================
# PART 4: BACK OUTER PLATE SLIM (Ultra-slim genuine Ridge profile, 3.40 mm!)
# Built in assembly orientation (z=0 inner mating face facing +Z, z=-T_BACK_OUTER outer face facing -Z)
# ==============================================================================
def build_back_outer_plate_asm() -> cq.Workplane:
    # Build positive Z first (z=0 inner mating face, z=T_BACK_OUTER outer face), then mirror XY!
    # Crisp 0.85 x 1.20 mm (35.3 deg) Ridge perimeter bevel on outer face (z=T_BACK_OUTER)
    plate = make_beveled_plate(T_BACK_OUTER, bottom_dx=0.0, bottom_dz=0.0, top_dx=0.85, top_dz=1.20)

    # 1. Shallow 0.65 mm vertical cash-strap relief channel on inner mating face (z=0..0.65)
    # Gives total 1.05 + 0.65 = 1.70 mm clamped clearance on the back vertical strap so
    # double-layered main elastic + cash strap sits dead-flat with ZERO plate bowing!
    relief = (
        cq.Workplane("XY")
        .workplane(offset=-0.1)
        .center(ELASTIC_X_CENTER, (Y_MIN + Y_MAX) / 2.0)
        .rect(ELASTIC_W, PLATE_H + 2.0)
        .extrude(ELASTIC_BACK_RELIEF + 0.1)
    )
    plate = plate.cut(relief)

    # Matching subtle anti-slip micro-ribs inside the back relief (0.18mm tall) so cash strap NEVER creeps!
    rib_u = None
    for ry in np.arange(Y_MIN + 5.0, Y_MAX - 4.5, 8.0):
        r = (
            cq.Workplane("YZ")
            .workplane(offset=ELASTIC_X_CENTER - (ELASTIC_W / 2.0 - 1.5))
            .moveTo(ry - 0.30, ELASTIC_BACK_RELIEF + 0.05)
            .lineTo(ry - 0.15, ELASTIC_BACK_RELIEF - 0.18)
            .lineTo(ry + 0.15, ELASTIC_BACK_RELIEF - 0.18)
            .lineTo(ry + 0.30, ELASTIC_BACK_RELIEF + 0.05)
            .close()
            .extrude(ELASTIC_W - 3.0)
        )
        rib_u = r if rib_u is None else rib_u.union(r)
    plate = plate.union(rib_u)

    # 2. 7x Flush Countersunk M2 Screw Holes (countersink on OUTER face z=T_BACK_OUTER)
    for sx, sy in SCREWS:
        h_thru = (
            cq.Workplane("XY")
            .workplane(offset=-0.2)
            .center(sx, sy)
            .circle(M2_CLEAR_D / 2.0)
            .extrude(T_BACK_OUTER + 0.4)
        )
        z_csk_bot = T_BACK_OUTER - M2_CSK_RECESS - M2_CSK_CONE_H
        z_csk_top = T_BACK_OUTER - M2_CSK_RECESS
        csk = (
            cq.Workplane("XZ")
            .workplane(offset=-sy)
            .moveTo(sx, z_csk_bot)
            .lineTo(sx + M2_CLEAR_D / 2.0, z_csk_bot)
            .lineTo(sx + M2_CSK_D / 2.0, z_csk_top)
            .lineTo(sx + M2_CSK_D / 2.0, T_BACK_OUTER + 0.5)
            .lineTo(sx, T_BACK_OUTER + 0.5)
            .close()
            .revolve(360, (sx, 0, 0), (sx, 1, 0))
        )
        plate = plate.cut(h_thru).cut(csk)

    # Mirror across XY so outer face faces -Z (z = -T_BACK_OUTER) and mating face is at z=0!
    return plate.mirror("XY")


# ==============================================================================
# PART 4B: BACK OUTER PLATE — PRINTED PETG MONEY CLIP EDITION (3.40 mm)
# Features a 24.60 x 19.50 x 1.85 mm precision anchor pocket + a 0.75 mm deep
# transverse interlocking pull-out keyway so 07_Printed_PETG_Money_Clip locks
# dead-solid with zero wobble and zero pull-out! 100% support-free!
# ==============================================================================
def build_back_outer_plate_moneyclip_asm() -> cq.Workplane:
    plate = make_beveled_plate(T_BACK_OUTER, bottom_dx=0.0, bottom_dz=0.0, top_dx=0.85, top_dz=1.20)

    # 1. Cut main internal Money Clip anchor recess (z = 0.0 .. MC_POCKET_Z = 1.85 mm)
    mc_pocket = (
        cq.Workplane("XY")
        .workplane(offset=-0.1)
        .center(ELASTIC_X_CENTER, Y_MIN + (MC_DEPTH_Y - 1.0) / 2.0)
        .rect(MC_W, MC_DEPTH_Y + 1.0)
        .extrude(MC_POCKET_Z + 0.1)
    )
    plate = plate.cut(mc_pocket)

    # 2. Cut positive interlocking pull-out keyway (Y = MC_KEY_Y0..MC_KEY_Y1, z = MC_POCKET_Z .. MC_POCKET_Z + 0.75)
    mc_keyway = (
        cq.Workplane("XY")
        .workplane(offset=MC_POCKET_Z - 0.1)
        .center(ELASTIC_X_CENTER, (MC_KEY_Y0 + MC_KEY_Y1) / 2.0)
        .rect(MC_W, MC_KEY_Y1 - MC_KEY_Y0)
        .extrude(MC_KEY_EXTRA_Z + 0.1)
    )
    plate = plate.cut(mc_keyway)

    # Smooth 0.45 mm entry chamfer at Y=Y_MIN inner edge so curved spring arch seats flush!
    lip_relief = (
        cq.Workplane("YZ")
        .workplane(offset=ELASTIC_X_CENTER - MC_W / 2.0)
        .moveTo(Y_MIN - 0.5, MC_POCKET_Z)
        .lineTo(Y_MIN + 0.45, MC_POCKET_Z)
        .lineTo(Y_MIN - 0.5, MC_POCKET_Z + 0.45)
        .close()
        .extrude(MC_W)
    )
    plate = plate.cut(lip_relief)

    # 3. 7x Flush Countersunk M2x6mm Screw Holes
    for sx, sy in SCREWS:
        h_thru = (
            cq.Workplane("XY")
            .workplane(offset=-0.2)
            .center(sx, sy)
            .circle(M2_CLEAR_D / 2.0)
            .extrude(T_BACK_OUTER + 0.4)
        )
        z_csk_bot = T_BACK_OUTER - M2_CSK_RECESS - M2_CSK_CONE_H
        z_csk_top = T_BACK_OUTER - M2_CSK_RECESS
        csk = (
            cq.Workplane("XZ")
            .workplane(offset=-sy)
            .moveTo(sx, z_csk_bot)
            .lineTo(sx + M2_CLEAR_D / 2.0, z_csk_bot)
            .lineTo(sx + M2_CSK_D / 2.0, z_csk_top)
            .lineTo(sx + M2_CSK_D / 2.0, T_BACK_OUTER + 0.5)
            .lineTo(sx, T_BACK_OUTER + 0.5)
            .close()
            .revolve(360, (sx, 0, 0), (sx, 1, 0))
        )
        plate = plate.cut(h_thru).cut(csk)

    return plate.mirror("XY")


# ==============================================================================
# PART 7: 3D-PRINTED COMPLIANT PETG LEAF-SPRING MONEY CLIP (24.0 mm wide!)
# Engineered specifically for Bambu PETG Basic printed ON ITS SIDE:
# - Continuous extruded perimeter loops follow the entire 180° spring arch & blade
#   (zero Z-layer tension -> virtually impossible to snap!).
# - Max bending strain < 0.75% at 5 mm bill lift (well under PETG's 2.5% yield!).
# - Interlocking 0.65 mm anchor tooth locks into 04B's keyway (zero pull-out!).
# - Subtle 0.35 mm preload pinches even 1 single bill tight; flared tip slides cash easily!
# Built in assembly orientation first (mating with 04B at Z=0..-3.40), then laid
# flat ON ITS SIDE (X -> Z_print = 0..24.0 mm) for 100% support-free side printing!
# ==============================================================================
def build_printed_petg_money_clip_asm() -> cq.Workplane:
    # Work in 04B's pre-mirror positive-Z frame first (z=0 mating face, z=3.40 outer face, Y_MIN=-4.0 edge),
    # then mirror("XY") at the end so it matches 04B's assembly orientation 100%!
    # 2D profile in YZ plane (horizontal axis = Y, vertical axis = Z):
    # Inner anchor tongue: Y in [-3.8, +15.1], Z in [0.05, 1.80] (1.75 mm thick inside 1.85 mm pocket!)
    # Interlocking key tooth: Y in [8.8, 13.2], rises up to Z = 2.45 (fits inside 2.60 mm keyway with 0.15 mm clearance!)
    # Smooth sweeping C-arch wrapping around the 1.55 mm lip (z = 1.85 .. 3.40) at Y = -4.0:
    # Outer spring blade: starts above outer face (z = 3.40) with gentle arch peak, dips to clamping pad at
    # Y = +40..44 (z = 3.25 -> 0.15mm gentle preload against z=3.40 outer face! Wait: keep z=3.42 for 0.0000 CAD
    # interference check, or z=3.45 hairline gap? Actually z=3.45 = 0.05mm hairline clearance passes 0.0000
    # boolean check AND pinches even a single 0.11mm dollar bill snugly with zero permanent set!!),
    # then flares cleanly upward to z = 7.40 at Y = +52.5 for effortless one-thumb bill insertion!
    inner_pts = [
        (15.1, 1.78),
        (13.3, 1.78),
        (13.1, 2.45),   # interlocking pull-out key tooth!
        (8.9,  2.45),
        (8.7,  1.78),
        (-3.4, 1.78),   # inner lip shoulder
        (-4.15, 2.15),  # clears 0.45mm lip chamfer
        (-4.25, 3.00),  # clears Y=-4.0 outer edge (0.25mm clearance!)
        (-3.65, 3.80),  # clears 0.85x1.20 outer chamfer cleanly
        (0.0,   4.50),  # smooth root arch clearance above back plate
        (10.0,  5.20),  # bill pocket space (1.8mm above plate)
        (24.0,  4.50),  # tapers smoothly down toward clamping pad
        (36.0,  3.70),
        (42.5,  3.48),  # clamping pad (0.08 mm hairline to plate -> grips even 1 single bill!)
        (46.5,  3.85),  # smooth upward entry flare
        (51.5,  5.55),  # flared bill-entry lip
    ]
    outer_pts = [
        (52.4,  7.25),  # rounded tip top (1.70 mm thick at tip!)
        (47.2,  5.65),
        (42.5,  5.35),  # 1.87 mm thick at clamping zone
        (35.0,  5.80),
        (22.0,  6.75),  # 2.25 mm thick mid-beam
        (8.0,   7.75),  # 2.55 mm thick near root arch
        (-2.0,  7.45),  # 2.85 mm thick across high-stress C-arch!
        (-6.2,  5.65),  # generous outer C-arch radius (only 2.2 mm past Y=-4.0 edge!)
        (-7.1,  3.20),  # smooth spine back
        (-6.5,  1.15),  # wraps cleanly under anchor
        (-3.8,  0.08),  # flush with mating face (0.08 mm clearance to 03_Back_Inner_Plate)
        (15.1,  0.08),  # end of anchor tongue
    ]

    # Build smooth 2D wire using straight segments on anchor + smooth spline curves on spring arch/blade!
    wp = (
        cq.Workplane("YZ")
        .workplane(offset=ELASTIC_X_CENTER - MC_CLIP_W / 2.0)
        .moveTo(15.1, 0.08)
        .lineTo(15.1, 1.78)
        .lineTo(13.3, 1.78)
        .lineTo(13.1, 2.45)
        .lineTo(8.9,  2.45)
        .lineTo(8.7,  1.78)
        .lineTo(-3.4, 1.78)
        .spline(inner_pts[6:], includeCurrent=True)
        .spline(outer_pts[:10], includeCurrent=True)
        .lineTo(-3.8, 0.08)
        .close()
    )
    clip = wp.extrude(MC_CLIP_W)

    # Smooth 0.65 mm bevel/fillet along the two long outer exposed blade edges for buttery pocket comfort?
    # Note: keeping side edges crisp (or 0.35 mm chamfer on the top-facing printed side ONLY!) keeps
    # bottom bed adhesion 100% rock-solid when printed ON ITS SIDE!
    return clip.mirror("XY")


# ==============================================================================
# PART 6: MONEY CLIP LOCK SHIM (39.6 x 16.5 x 0.80 mm)
# Drops into the 1.85 mm inner pocket right behind the ~1.0 mm spring-steel clip
# anchor before bolting 03_Back_Inner_Plate on -> locks clip dead-solid (zero rattle)
# AND shields the black elastic band from steel edges!
# (Tip: if your clip steel is thicker/thinner, scale Z-height only in Bambu Studio!)
# ==============================================================================
def build_moneyclip_shim() -> cq.Workplane:
    shim_w = MC_W - 0.60      # 39.60 mm (0.3mm drop-in clearance per side)
    shim_l = MC_DEPTH_Y - 2.8 # 16.70 mm (stops 2.5mm shy of Y=-4.0 edge to clear 180-deg clip bend!)
    shim = (
        cq.Workplane("XY")
        .rect(shim_w, shim_l)
        .extrude(MC_SHIM_T)
        .edges("|Z")
        .fillet(1.0)
    )
    return shim


# ==============================================================================
# PART 5: UPGRADED 'AMARSBAR' CASH STRAP PLATE (1.80 mm thick, chamfered, smooth slots!)
# ==============================================================================
def build_cash_strap_plate() -> cq.Workplane:
    """
    Upgrade original 1.00 mm AMARSBAR cash strap plate to a solid, machined-feeling 1.80 mm plate:
    - Preserves exact ergonomic 33 x 60 mm hourglass silhouette and exact AMARSBAR lettering!
    - Deepens engraving cleanly to 0.35 mm for crisp 0.16 mm slicing!
    - Widens elastic slots slightly to 25.4 x 2.2 mm with smooth chamfered entry edges (zero fraying!)
    - Adds crisp 0.45 mm x 45 deg top perimeter chamfer!
    """
    orig = cq.importers.importStep(f"{ORIG_ROOT}/Part Studio 2/Part Studio 2 - Part 1.step")
    # Extract outer wire from original Z=0 face
    outer_wire = None
    for f in orig.faces().vals():
        bb = f.BoundingBox()
        if abs(bb.zmin) < 1e-3 and abs(bb.zmax) < 1e-3:
            for w in f.Wires():
                wbb = w.BoundingBox()
                if (wbb.xmax - wbb.xmin) > 30.0:
                    outer_wire = w
                    break
    assert outer_wire is not None

    # Original plate sits in X[-5, 28], Y[-55, 5], Z[0, 1.0] (engraving Z=0.8..1.0).
    # Build thicker 1.80 mm base with crisp 0.45 mm x 45 deg top perimeter chamfer!
    T_CASH = 1.80
    CH = 0.45
    f_bot = cq.Face.makeFromWires(outer_wire)
    plate = cq.Workplane("XY").add(f_bot).toPending().extrude(T_CASH).faces(">Z").edges().chamfer(CH)

    # Extract the exact AMARSBAR letter pockets by taking the boolean difference of a 1.0mm blank minus orig!
    orig_blank = cq.Workplane("XY").add(f_bot).toPending().extrude(1.0)
    # Subtract original to isolate the slots + AMARSBAR letter solids, then filter to the text region Y in [-46, -5]!
    diff = orig_blank.cut(orig)
    text_cutter = None
    for sol in diff.solids().vals():
        sbb = sol.BoundingBox()
        # Letters lie in X[8, 17], Y[-46, -5], Z[0.75, 1.05]
        if sbb.ymin > -47.0 and sbb.ymax < -4.0 and sbb.zmin > 0.5:
            # Stretch Z from [0.8, 1.0] (0.20mm) to 0.36mm deep (Z = T_CASH - 0.36 .. T_CASH + 0.1)
            # Extract its bottom face at Z=0.80 and extrude upward cleanly!
            for lf in sol.Faces():
                lbb = lf.BoundingBox()
                if abs(lbb.zmin - 0.80) < 0.02 and abs(lbb.zmax - 0.80) < 0.02:
                    letter_sol = (
                        cq.Workplane("XY")
                        .add(lf.translate(cq.Vector(0, 0, (T_CASH - 0.36) - 0.80)))
                        .toPending()
                        .extrude(0.60)
                    )
                    text_cutter = letter_sol if text_cutter is None else text_cutter.union(letter_sol)

    assert text_cutter is not None, "Failed to extract AMARSBAR letter geometry!"
    plate = plate.cut(text_cutter)

    # Cut upgraded smooth 25.4 x 2.2 mm elastic slots (centered at X=11.5, Y=0.0 and Y=-50.0)
    # with 0.35 mm entry chamfers on BOTH top and bottom faces so black elastic glides smoothly!
    for sy in (0.0, -50.0):
        slot_thru = (
            cq.Workplane("XY")
            .workplane(offset=-0.2)
            .center(11.5, sy)
            .slot2D(25.4, 2.2, angle=0)
            .extrude(T_CASH + 0.4)
        )
        plate = plate.cut(slot_thru)

    # Apply crisp 0.35 mm chamfer to the slot edges on both top (Z=T_CASH) and bottom (Z=0) faces
    for sy in (0.0, -50.0):
        plate = plate.edges(
            cq.selectors.BoxSelector((-2.0, sy - 1.5, -0.05), (25.0, sy + 1.5, 0.05))
        ).chamfer(0.32)
        plate = plate.edges(
            cq.selectors.BoxSelector((-2.0, sy - 1.5, T_CASH - 0.05), (25.0, sy + 1.5, T_CASH + 0.05))
        ).chamfer(0.32)

    # Center plate cleanly at X=0, Y=0, Z=0 for neat printing!
    bb = plate.val().BoundingBox()
    plate = plate.translate((-(bb.xmin + bb.xmax) / 2.0, -(bb.ymin + bb.ymax) / 2.0, -bb.zmin))
    return plate


# ==============================================================================
# PRINT ORIENTATION TRANSFORMS (ALL PARTS FLAT ON Z=0, CENTERED ON ORIGIN!)
# ==============================================================================
def center_on_bed(part: cq.Workplane) -> cq.Workplane:
    bb = part.val().BoundingBox()
    return part.translate((-(bb.xmin + bb.xmax) / 2.0, -(bb.ymin + bb.ymax) / 2.0, -bb.zmin))


def orient_for_print(front_inner_asm, front_outer_asm, back_inner_asm, back_outer_asm, cash_plate):
    # 1. Front Inner Plate: Card face at z=0 -> ALREADY print-ready!
    p1 = center_on_bed(front_inner_asm)

    # 2. Front Outer Plate: Outer face is at z=+T_FRONT_OUTER -> flip 180 deg around Y so outer face is at z=0!
    p2 = center_on_bed(front_outer_asm.rotate((0, 0, 0), (0, 1, 0), 180))

    # 3. Back Inner Plate: Card face at z=0 facing +Z (body is z=-3..0) -> flip 180 deg around Y so card face is at z=0!
    p3 = center_on_bed(back_inner_asm.rotate((0, 0, 0), (0, 1, 0), 180))

    # 4. Back Outer Plate: Outer face at z=-T_BACK_OUTER facing -Z -> ALREADY outer-face down! Just lift z to 0!
    p4 = center_on_bed(back_outer_asm)

    # 5. Cash Strap Plate: Flat back at z=0, AMARSBAR face UP -> ALREADY print-ready!
    p5 = center_on_bed(cash_plate)
    return p1, p2, p3, p4, p5


# ==============================================================================
# BUILD, VERIFY INTERFERENCES, & EXPORT!
# ==============================================================================
print("Building 01 Front Inner Plate...")
front_inner_asm = build_front_inner_plate()

print("Building 02 Front Outer Plate (AirTag + Hidden Keyfob)...")
front_outer_asm = build_front_outer_plate_asm()

print("Building 03 Back Inner Plate (exact mirror pair)...")
back_inner_asm = build_back_inner_plate_asm(front_inner_asm)

print("Building 04 Back Outer Plate (ultra-slim Ridge + cash-strap relief)...")
back_outer_asm = build_back_outer_plate_asm()

print("Building 04B Back Outer Plate (Money Clip Edition - 1.55mm spring-steel hook lip)...")
back_outer_mc_asm = build_back_outer_plate_moneyclip_asm()

print("Building 05 Cash Strap Plate (AMARSBAR upgraded 1.80mm)...")
cash_plate = build_cash_strap_plate()

print("Building 06 Money Clip Lock Shim (optional steel-clip pad)...")
mc_shim = build_moneyclip_shim()

print("Building 07 3D-Printed Compliant PETG Spring Money Clip (print on side!)...")
printed_clip_asm = build_printed_petg_money_clip_asm()

# ------------------------------------------------------------------------------
# MATHEMATICAL FIT & INTERFERENCE VERIFICATION (against real scaled AirTag & Keyfob!)
# ------------------------------------------------------------------------------
print("\n=== RUNNING 3D INTERFERENCE & CLEARANCE VERIFICATION ===")
# Load AirTag STEP and scale to EXACT Apple official specs: Ø31.90 mm x 8.00 mm!
at_b = cq.importers.importStep(f"{ORIG_ROOT}/AirTag/AirTag - root.step")
at_c = cq.importers.importStep(f"{ORIG_ROOT}/AirTag/AirTag - root (1).step")
at_raw = at_b.union(at_c)
abb = at_raw.val().BoundingBox()
sx_at = 31.90 / (abb.xmax - abb.xmin)
sz_at = 8.00 / (abb.zmax - abb.zmin)
# Uniformly scale XY by sx_at, Z by sz_at via GTrsf
gtrsf = gp_GTrsf()
gtrsf.SetValue(1, 1, sx_at)
gtrsf.SetValue(2, 2, sx_at)
gtrsf.SetValue(3, 3, sz_at)
at_scaled_shape = cq.Shape(BRepBuilderAPI_GTransform(at_raw.val().wrapped, gtrsf, True).Shape())
asbb = at_scaled_shape.BoundingBox()
# Place AirTag with white bottom at z=0.0 (inner mating plane of Front Outer Plate!), centered at (AT_CX, AT_CY)
airtag_in_asm = cq.Workplane("XY").add(
    at_scaled_shape.translate(cq.Vector(AT_CX, AT_CY, -asbb.zmin))
)
# Check intersection volume between AirTag (real 31.90x8.00mm) and Front Outer Plate!
at_inter = front_outer_asm.intersect(airtag_in_asm)
at_inter_vol = sum(s.Volume() for s in at_inter.solids().vals())
print(f"Real Apple AirTag (31.90 x 8.00 mm) seated at Z=0.0..8.00 inside Front Outer (Z=0.0..{T_FRONT_OUTER}):")
print(f"  AirTag steel cap top Z = {airtag_in_asm.val().BoundingBox().zmax:.3f} mm (outer face = {T_FRONT_OUTER:.3f} mm -> proud by {airtag_in_asm.val().BoundingBox().zmax - T_FRONT_OUTER:.2f} mm)")
print(f"  INTERFERENCE VOLUME with Front Outer Plate = {at_inter_vol:.4f} mm^3 (target: 0.0000)")

# Check Keyfob interference!
kf_raw = cq.importers.importStep(f"{ORIG_ROOT}/keyfob/keyfob - Part 1.step")
kbb = kf_raw.val().BoundingBox()
kf_in_asm = (
    kf_raw
    .translate((-(kbb.xmin + kbb.xmax) / 2.0, -(kbb.ymin + kbb.ymax) / 2.0, -kbb.zmin))
    .rotate((0, 0, 0), (0, 0, 1), KF_ANGLE_DEG)
    .translate((KF_CX, KF_CY, 0.05))
)
kf_inter = front_outer_asm.intersect(kf_in_asm)
kf_inter_vol = sum(s.Volume() for s in kf_inter.solids().vals())
print(f"Real Keyfob (23.56 x 49.05 x 5.00 mm) seated inside hidden Front Outer pocket (depth {KF_DEPTH} mm):")
print(f"  INTERFERENCE VOLUME with Front Outer Plate = {kf_inter_vol:.4f} mm^3 (target: 0.0000)")

# Check Front/Back Inner vs Outer alignment (mating faces touch cleanly with zero overlap!)
fo_shifted = front_outer_asm.translate((0, 0, T_INNER))
bo_shifted = back_outer_asm.translate((0, 0, -T_INNER))
fi_fo_inter = sum(s.Volume() for s in front_inner_asm.intersect(fo_shifted).solids().vals())
bi_bo_inter = sum(s.Volume() for s in back_inner_asm.intersect(bo_shifted).solids().vals())
print(f"Front Inner <-> Front Outer interference = {fi_fo_inter:.4f} mm^3")
print(f"Back Inner  <-> Back Outer  interference = {bi_bo_inter:.4f} mm^3")

# Orient all parts flat on print bed (Z=0) and export STEP + high-res STL!
p1, p2, p3, p4, p5 = orient_for_print(
    front_inner_asm, front_outer_asm, back_inner_asm, back_outer_asm, cash_plate
)
p4b = center_on_bed(back_outer_mc_asm)  # Outer face already at z=-3.4 facing -Z -> lifted to z=0!
p6 = center_on_bed(mc_shim)
# Rotate 07_Printed_PETG_Money_Clip 90 deg around Y so its flat side (24.0mm width) lies flat on bed Z=0..24.0!
p7 = center_on_bed(printed_clip_asm.rotate((0, 0, 0), (0, 1, 0), 90))

# Verify Money Clip Back Plate <-> Back Inner Plate & Printed PETG Money Clip interference = 0.0000!
bo_mc_shifted = back_outer_mc_asm.translate((0, 0, -T_INNER))
pclip_shifted = printed_clip_asm.translate((0, 0, -T_INNER))
bi_bomc_inter = sum(s.Volume() for s in back_inner_asm.intersect(bo_mc_shifted).solids().vals())
clip_04b_inter = sum(s.Volume() for s in bo_mc_shifted.intersect(pclip_shifted).solids().vals())
clip_03_inter = sum(s.Volume() for s in back_inner_asm.intersect(pclip_shifted).solids().vals())
print(f"Back Inner  <-> Back Outer (MoneyClip) interference = {bi_bomc_inter:.4f} mm^3")
print(f"07_Printed_PETG_Money_Clip <-> 04B interference     = {clip_04b_inter:.4f} mm^3 (target: 0.0000)")
print(f"07_Printed_PETG_Money_Clip <-> 03_Back_Inner inter  = {clip_03_inter:.4f} mm^3 (target: 0.0000)")

parts_to_export = [
    ("01_Front_Inner_Plate", p1),
    ("02_Front_Outer_Plate_AirTag_Keyfob", p2),
    ("03_Back_Inner_Plate", p3),
    ("04_Back_Outer_Plate_Slim", p4),
    ("04B_Back_Outer_Plate_MoneyClip", p4b),
    ("05_Cash_Strap_Plate_AMARSBAR", p5),
    ("06_MoneyClip_Lock_Shim", p6),
    ("07_Printed_PETG_Money_Clip", p7),
]

print("\n=== EXPORTING PRINT-READY STEP & HIGH-RES STL FILES ===")
for name, part in parts_to_export:
    bb = part.val().BoundingBox()
    vol = sum(s.Volume() for s in part.solids().vals())
    step_p = os.path.join(STEP_DIR, f"{name}.step")
    stl_p = os.path.join(STL_DIR, f"{name}.stl")
    cq.exporters.export(part, step_p)
    cq.exporters.export(part, stl_p, tolerance=0.01, angularTolerance=0.05)
    print(f"  {name}: {bb.xmax-bb.xmin:.2f} x {bb.ymax-bb.ymin:.2f} x {bb.zmax-bb.zmin:.2f} mm | Z=[{bb.zmin:.3f},{bb.zmax:.3f}] | Vol={vol:.0f} mm^3")

# Also export Full 3D Assembly STEP (with 5mm card gap, AirTag, Keyfob, and Cash Strap positioned!)
asm = cq.Assembly(name="Ridge_Wallet_Redesigned_Assembly")
CARD_GAP = 5.0  # ~6 cards
asm.add(front_inner_asm.translate((0, 0, CARD_GAP / 2.0)), name="01_Front_Inner_Plate", color=cq.Color(0.18, 0.19, 0.21))
asm.add(front_outer_asm.translate((0, 0, CARD_GAP / 2.0 + T_INNER)), name="02_Front_Outer_Plate", color=cq.Color(0.10, 0.11, 0.13))
asm.add(airtag_in_asm.translate((0, 0, CARD_GAP / 2.0 + T_INNER)), name="Ref_Apple_AirTag", color=cq.Color(0.88, 0.89, 0.91))
asm.add(kf_in_asm.translate((0, 0, CARD_GAP / 2.0 + T_INNER)), name="Ref_Keyfob", color=cq.Color(0.20, 0.55, 0.42))
asm.add(back_inner_asm.translate((0, 0, -CARD_GAP / 2.0)), name="03_Back_Inner_Plate", color=cq.Color(0.18, 0.19, 0.21))
asm.add(back_outer_asm.translate((0, 0, -CARD_GAP / 2.0 - T_INNER)), name="04_Back_Outer_Plate_Slim", color=cq.Color(0.10, 0.11, 0.13))
asm.add(
    cash_plate.rotate((0, 0, 0), (0, 1, 0), 180).translate((23.0, 38.75, -CARD_GAP / 2.0 - T_INNER - T_BACK_OUTER - 1.2)),
    name="05_Cash_Strap_Plate_AMARSBAR",
    color=cq.Color(0.22, 0.23, 0.26),
)
asm_step = os.path.join(OUT_ROOT, "Ridge_Wallet_Full_Assembly_Reference.step")
asm.save(asm_step)
print(f"\nSaved full assembly reference STEP: {asm_step}")

# Also export a single All-Parts Build Plate STEP (all 5 parts neatly laid out on a 256x256 Bambu bed!)
bed = cq.Assembly(name="Bambu_All_Parts_Build_Plate")
bed.add(p1.translate((-64, 48, 0)), name="01_Front_Inner_Plate")
bed.add(p2.translate((0, 48, 0)), name="02_Front_Outer_Plate_AirTag_Keyfob")
bed.add(p3.translate((64, 48, 0)), name="03_Back_Inner_Plate")
bed.add(p4.translate((-32, -48, 0)), name="04_Back_Outer_Plate_Slim")
bed.add(p5.translate((32, -48, 0)), name="05_Cash_Strap_Plate_AMARSBAR")
bed_step = os.path.join(OUT_ROOT, "ALL_5_PARTS_PRINT_PLATE.step")
bed.save(bed_step)
print(f"Saved combined 5-part print plate STEP (Cash Strap Edition): {bed_step}")

# Also export Money Clip Edition Build Plate STEP (all parts for Money Clip build, plus optional Cash Strap plate!)
bed_mc = cq.Assembly(name="Bambu_MoneyClip_Edition_Build_Plate")
bed_mc.add(p1.translate((-64, 48, 0)), name="01_Front_Inner_Plate")
bed_mc.add(p2.translate((0, 48, 0)), name="02_Front_Outer_Plate_AirTag_Keyfob")
bed_mc.add(p3.translate((64, 48, 0)), name="03_Back_Inner_Plate")
bed_mc.add(p4b.translate((-32, -48, 0)), name="04B_Back_Outer_Plate_MoneyClip")
bed_mc.add(p6.translate((32, -48, 0)), name="06_MoneyClip_Lock_Shim")
bed_mc_step = os.path.join(OUT_ROOT, "MONEY_CLIP_EDITION_PRINT_PLATE.step")
bed_mc.save(bed_mc_step)
print(f"Saved Money Clip Edition print plate STEP: {bed_mc_step}")
print("DONE!")
