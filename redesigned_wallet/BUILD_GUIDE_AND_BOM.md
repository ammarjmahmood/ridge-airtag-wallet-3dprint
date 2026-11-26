# Redesigned Ridge-Style Wallet — Build Guide, Amazon BOM & Slicing Recipe

## 1. Key Engineering Upgrades

- **Watch-Style Captive AirTag Mount (Impossible to Pop Out)**: Loaded from the inside into a `Ø 32.70 mm` cavity tapering via a support-free cone into a chamfered `Ø 26.20 mm` front watch bezel. A `2.85 mm` solid 360° overhang lip traps the `31.90 mm` AirTag body permanently while framing the polished Apple steel cap flush (`0.30 mm` subtle center dome). Includes a discreet internal 6-o'clock pry notch for easy annual battery changes.
- **100% Hidden Internal Keyfob Pocket**: Packed into the lower half of `02_Front_Outer_Plate_AirTag_Keyfob` inside a blind `5.20 mm` deep pocket beneath a **solid 2.40 mm continuous exterior skin** — completely invisible from outside, scans RFID normally, with `>= 3.67 mm` solid walls to all edges, screws, and the AirTag.
- **Anti-Slip Clamped Elastic T-Channel**: Tightened channel depth to `1.05 mm` (down from 1.50 mm) with `0.22 mm` transverse anti-slip grip ribs and chamfered exit edges so dark woven elastic stays locked tightly without fraying. Added a `0.65 mm` opposing relief channel on `04_Back_Outer_Plate_Slim` (1.70 mm total clamped space) for double-layer cash-strap overlap without plate bowing.
- **Dead-Flush Ridge M2 Hardware (No Soldering Iron Needed)**: 7 flat-landed 90° flush countersunk M2 holes per side (`M2x10mm` front, `M2x6mm` back) mating with captive DIN 934 M2 hex nuts recessed `0.25 mm` safely below the card face (Voron stepped double-bridges print 100% support-free).
- **Properly Mirrored Inner Plates + Interchangeable Back Plates (`AMARSBAR` Cash Strap OR Spring-Steel Money Clip)**:
  - `04_Back_Outer_Plate_Slim` + upgraded `1.80 mm` chamfered `AMARSBAR` cash strap plate.
  - `04B_Back_Outer_Plate_MoneyClip` (`1.55 mm` thinned short-edge hook lip matching a real metal Ridge plate + `1.85 mm` internal anchor pocket) paired with `06_MoneyClip_Lock_Shim` (`0.80 mm` zero-wobble backing pad) — bolts onto the exact same `03_Back_Inner_Plate` with the exact same 7x `M2x6mm` screws so you can swap anytime!

## 2. Verified Amazon Canada (amazon.ca) BOM — Everything You Need to Buy

*(You already have the Apple AirTag, your Keyfob, and Black + White PETG!)*

1. **Matte Black Forged Spring-Steel Money Clip + Cash Strap Kit (Central T-Tab Ridge Style)**:
   - MINBERAND Accessories Kit for Ridge Wallet (Black & Army Green Forged Spring-Steel Money Clips + 2 Cash Straps + Torx Driver) — https://www.amazon.ca/dp/B0HJV2V9D5 (5.0 stars, In Stock, $33.40 CAD)
2. **Black Pre-Sewn Ridge Card-Holding Elastic Band Kit (Main Inner T-Band — NOT white!)**:
   - Moibunka 25-Pcs Wallet Screw & Black Elastic Band Replacement Kit — https://www.amazon.ca/dp/B0GQQN46XJ (4.6 stars / 38 reviews, In Stock, $19.05 CAD)
   - *(Optional DIY 1-inch non-roll woven spool backup: Dritz 9407B 1-Inch x 12-Yard Black Non-Roll Woven Elastic — https://www.amazon.ca/dp/B007XU23ZU, 4.7 stars / 1,796 reviews, $28.86 CAD)*
3. **Black M2 Flat-Head Countersunk Hex Screws + M2 Hex Nuts + Wrench Kit** *(explicitly verified to include M2x6mm [25 pcs], M2x10mm [25 pcs], M2 Hex Nuts [100 pcs], AND matching M2 Hex Wrench!)*:
   - HanTof 900-Pcs Black Grade 10.9 DIN7991 Flat-Head Countersunk Hex Socket Screws & Nuts Kit (M2/M2.5/M3) — https://www.amazon.ca/dp/B0FF4TVQ7G (5.0 stars, In Stock, $28.18 CAD, FREE delivery)
4. **(Optional Filament Upgrade) Matte Black Carbon-Fiber PETG-CF** *(only if upgrading later — requires hardened steel nozzle)*:
   - FLASHFORGE Carbon Fiber PETG-CF 1.75mm Black 1kg — https://www.amazon.ca/dp/B0D7VXC38N (4.7 stars / 332 reviews, In Stock, $43.09 CAD, FREE delivery)

## 3. Pre-Sliced Bambu Lab P1S (0.4 mm Nozzle, PETG) Ready-to-Print Plates

Already sliced with Bambu Studio (`0.12 mm` layer height, Arachne walls, 4 wall loops, `inner-outer-inner` precision order, 40% Gyroid infill, 55 mm/s satin outer walls, 35 mm/s first layer, 0.12 mm elephant foot comp, 255 °C nozzle / 70 °C Textured PEI Plate, 0 supports):
- **Tuxedo Stealth Plate 1 (Load BLACK PETG — 4h 08m, 52.3 g, ironing ON for AMARSBAR):** `sliced_for_bambu_P1S/Plate1_BLACK_OuterPlates_SLICED_P1S_PETG.3mf`
- **Tuxedo Stealth Plate 2 (Load WHITE PETG — 1h 17m, 24.5 g, ironing OFF to keep grip ribs crisp):** `sliced_for_bambu_P1S/Plate2_WHITE_InnerPlates_SLICED_P1S_PETG.3mf`
- **All-in-One Single-Color Money Clip Plate (Load BLACK PETG — 3h 34m, 59.6 g):** `sliced_for_bambu_P1S/AllInOne_MoneyClip_Wallet_SLICED_P1S_PETG.3mf`

- **Plate**: Textured PEI Plate (or Carbon-Fiber pattern sheet)
- **Layer Height**: `0.16 mm` (or `0.12 mm` for razor-sharp chamfers & `AMARSBAR` text)
- **Wall Generator**: Arachne | **Walls**: 4 loops | **Infill**: 30–40% Gyroid (or 100% for premium metal-like heft)
- **Supports**: OFF (0 supports required)
- **Ironing**: Enable Top-Surface Ironing on `05_Cash_Strap_Plate_AMARSBAR`
- **Outer Wall Speed**: 60–80 mm/s | **Elephant Foot Compensation**: 0.12 mm

## 4. Hardware Quick-Reference

- **Front Half (`01_Front_Inner_Plate` + `02_Front_Outer_Plate_AirTag_Keyfob`)**: 7x **M2 x 10 mm** black flat-head countersunk screws + 7x **M2 hex nuts**
- **Back Half (`03_Back_Inner_Plate` + `04_Back_Outer_Plate_Slim`)**: 7x **M2 x 6 mm** black flat-head countersunk screws + 7x **M2 hex nuts**
- **Optional**: Tiny drop of Blue Loctite 242 on the nut threads during final tightening.
