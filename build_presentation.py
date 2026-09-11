#!/usr/bin/env python3
"""
=============================================================================
Presentation Builder: EXAELIA 80m Hydrogen BWB (MMS236 DT1)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Authors: Johan Persson, Sai Srinivasa Manideep Jakka, Tobias Hilltorp, William Gustavsson (Group 13)

Creates a modern, aerospace dark-mode PowerPoint presentation (16:9 Widescreen)
with clean typography, structured glassmorphic cards, KPI grids, and embedded high-res CAD & blueprint assets.
=============================================================================
"""

import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette Constants (Aerospace Midnight Dark Mode)
# -----------------------------------------------------------------------------
BG_COLOR       = RGBColor(10, 15, 29)      # #0A0F1D Deep Aerospace Navy
CARD_BG        = RGBColor(17, 28, 53)      # #111C35 Dark Slate Card
CARD_BORDER    = RGBColor(30, 58, 138)     # #1E3A8A Dark Blue Border
CYAN_ACCENT    = RGBColor(56, 189, 248)    # #38BDF8 Electric Cyan
GOLD_ACCENT    = RGBColor(250, 204, 21)    # #FACC15 Aerodynamic Gold
EMERALD_ACCENT = RGBColor(16, 185, 129)    # #10B981 Hydrogen Green
ROSE_ACCENT    = RGBColor(244, 63, 94)     # #F43F5E Coral/Rose Accent
TEXT_WHITE     = RGBColor(255, 255, 255)   # Pure White Title
TEXT_LIGHT     = RGBColor(226, 232, 240)   # #E2E8F0 Body Text
TEXT_MUTED     = RGBColor(148, 163, 184)   # #94A3B8 Secondary Text

FONT_TITLE = "Helvetica Neue"
FONT_BODY  = "Arial"

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text="MMS236 AIRCRAFT DESIGN | GROUP 13"):
    # Category / Breadcrumb
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_BODY
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = CYAN_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

def add_kpi_card(slide, left, top, width, height, value_text, label_text, unit_text="", value_color=CYAN_ACCENT):
    add_card(slide, left, top, width, height)
    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    # Label
    p1 = tf.paragraphs[0]
    p1.text = label_text.upper()
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MUTED

    # Value
    p2 = tf.add_paragraph()
    p2.text = value_text + (" " + unit_text if unit_text else "")
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = value_color

def create_presentation(output_path="/Users/jakkasaisrinivasamanideep/Documents/MMS236/Aircraft_Design_DT1_EXAELIA_Group13.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    blank_layout = prs.slide_layouts[6]

    # Path to assets
    asset_dir = "/Users/jakkasaisrinivasamanideep/Documents/MMS236/04_Presentation_Assets"
    img1_sketch   = os.path.join(asset_dir, "image1.jpeg")
    img2_mission  = os.path.join(asset_dir, "image2.jpeg")
    img3_sfc      = os.path.join(asset_dir, "image3.png")
    img4_concept  = os.path.join(asset_dir, "image4.jpeg")
    img_cad_3d    = "/Users/jakkasaisrinivasamanideep/Documents/MMS236/03_CAD_OpenVSP_Models/exaelia_bwb_80m_3d_views.png"

    # =========================================================================
    # SLIDE 1: Title & Hero Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Hero Banner Card
    add_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=CARD_BG, border_color=CYAN_ACCENT)

    # Chalmers Badge
    tb_badge = slide1.shapes.add_textbox(Inches(1.2), Inches(1.15), Inches(10.0), Inches(0.35))
    tf_b = tb_badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "CHALMERS UNIVERSITY OF TECHNOLOGY  |  MMS236 AIRCRAFT DESIGN  |  DESIGN TASK 1"
    p_b.font.name = FONT_BODY
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN_ACCENT

    # Main Project Name
    tb_main = slide1.shapes.add_textbox(Inches(1.2), Inches(1.55), Inches(10.5), Inches(1.2))
    tf_m = tb_main.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "EXAELIA"
    p_m.font.name = FONT_TITLE
    p_m.font.size = Pt(46)
    p_m.font.bold = True
    p_m.font.color.rgb = TEXT_WHITE

    # Subtitle
    p_sub = tf_m.add_paragraph()
    p_sub.text = "80m Long-Range Liquid Hydrogen Blended Wing Body Transport"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = GOLD_ACCENT

    # Authors Card
    tb_auth = slide1.shapes.add_textbox(Inches(1.2), Inches(3.2), Inches(10.5), Inches(0.8))
    tf_a = tb_auth.text_frame
    p_a1 = tf_a.paragraphs[0]
    p_a1.text = "Group 13 Design Team:"
    p_a1.font.name = FONT_BODY
    p_a1.font.size = Pt(12)
    p_a1.font.bold = True
    p_a1.font.color.rgb = TEXT_MUTED

    p_a2 = tf_a.add_paragraph()
    p_a2.text = "Johan Persson  •  Sai Srinivasa Manideep Jakka  •  Tobias Hilltorp  •  William Gustavsson"
    p_a2.font.name = FONT_BODY
    p_a2.font.size = Pt(14)
    p_a2.font.bold = True
    p_a2.font.color.rgb = TEXT_LIGHT

    # Metric Badges (Bottom of Slide 1)
    metrics = [
        ("PASSENGER CAPACITY", "430", "Pax (2-Class)"),
        ("DESIGN RANGE", "12,500", "km (6,750 nm)"),
        ("CRUISE SPEED", "Mach 0.85", "at FL350"),
        ("WINGSPAN", "80.0 m", "(ICAO Code F)")
    ]
    for i, (lbl, val, unt) in enumerate(metrics):
        bx = Inches(1.2 + i * 2.75)
        add_kpi_card(slide1, bx, Inches(4.3), Inches(2.6), Inches(1.9), val, lbl, unt, value_color=CYAN_ACCENT)

    # =========================================================================
    # SLIDE 2: First Sketch to Architectural Evolution
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Concept Origin: From Initial Sketch to Blended Body Architecture")

    # Left Card (Sketch Image Container)
    add_card(slide2, Inches(0.8), Inches(1.4), Inches(5.4), Inches(5.5))
    if os.path.exists(img1_sketch):
        slide2.shapes.add_picture(img1_sketch, Inches(1.0), Inches(1.6), width=Inches(5.0))

    # Right Card (Design Decisions)
    add_card(slide2, Inches(6.4), Inches(1.4), Inches(6.133), Inches(5.5))
    tb_dec = slide2.shapes.add_textbox(Inches(6.65), Inches(1.65), Inches(5.65), Inches(5.0))
    tf_dec = tb_dec.text_frame
    tf_dec.word_wrap = True

    decisions = [
        ("1. Pure 80m Wingspan (ICAO Code F Gate Box)",
         "Full span compliant with existing international airport gates (A380/B777X class) without requiring folding wings."),
        ("2. Muscular Lifting Centerbody (t/c = 19.5%)",
         "A 7.41 m maximum centerbody depth easily houses a stand-up widebody passenger cabin and multi-layer cryogenic tanks."),
        ("3. Unified Single-Deck Theater Cabin (430 Pax)",
         "Continuous 14.0 m wide central passenger deck with uninterrupted longitudinal aisles, eliminating claustrophobic isolated rows."),
        ("4. Symmetrical Outboard & Aft Cryotanks (610 m³)",
         "6 double-walled vacuum-insulated cylinders placed in wing shoulders and aft core to minimize CG excursion during fuel burn."),
        ("5. Upper-Deck Acoustically Shielded Turbofans",
         "Twin geared turbofans mounted above the trailing deck to shield airport communities from engine fan and jet noise.")
    ]
    for i, (title, desc) in enumerate(decisions):
        p_t = tf_dec.paragraphs[0] if i == 0 else tf_dec.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = CYAN_ACCENT
        p_t.space_before = Pt(8) if i > 0 else Pt(0)

        p_d = tf_dec.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 3: Sizing Mission Profile
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Mission Profile & Flight Operational Envelope")

    # Top Card (Mission Diagram)
    add_card(slide3, Inches(0.8), Inches(1.35), Inches(11.733), Inches(3.4))
    if os.path.exists(img2_mission):
        slide3.shapes.add_picture(img2_mission, Inches(1.5), Inches(1.45), width=Inches(10.3))

    # Bottom 3 Segment Summary Cards
    add_kpi_card(slide3, Inches(0.8), Inches(4.95), Inches(3.7), Inches(1.95), 
                 "12,500 km", "MAIN CRUISE SEGMENT", "at FL350 (M0.85)", value_color=CYAN_ACCENT)
    add_kpi_card(slide3, Inches(4.8), Inches(4.95), Inches(3.7), Inches(1.95), 
                 "200 nm", "ALTERNATE AIRPORT DIVERSION", "at FL250 (CS-25)", value_color=GOLD_ACCENT)
    add_kpi_card(slide3, Inches(8.8), Inches(4.95), Inches(3.733), Inches(1.95), 
                 "30 min + 3%", "STATUTORY LOITER & CONTINGENCY", "at 1,500 ft (ICAO)", value_color=EMERALD_ACCENT)

    # =========================================================================
    # SLIDE 4: Engine Performance & Hydrogen SFC
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Propulsion Modeling: Liquid Hydrogen SFC & Energy Density")

    # Left Card (SFC Chart)
    add_card(slide4, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.5))
    if os.path.exists(img3_sfc):
        slide4.shapes.add_picture(img3_sfc, Inches(1.0), Inches(1.6), width=Inches(5.4))

    # Right Card (SFC Calculations)
    add_card(slide4, Inches(6.8), Inches(1.4), Inches(5.733), Inches(5.5))
    tb_sfc = slide4.shapes.add_textbox(Inches(7.05), Inches(1.65), Inches(5.25), Inches(5.0))
    tf_sfc = tb_sfc.text_frame
    tf_sfc.word_wrap = True

    sfc_points = [
        ("Year 2050 EIS Turbofan Baseline (Jet-A):",
         "Following historical efficiency trends (CFM56 ➔ GE90 ➔ Leap-1A):\n• Jet-A Cruise SFC: ~12.0 to 13.5 mg/(N·s)\n• Jet-A Loiter SFC: ~11.0 mg/(N·s)"),
        ("Thermal Energy Equivalence Principle:",
         "Hydrogen releases 2.80× higher energy per kg than kerosene:\n• LHV (Jet-A) = 42.8 MJ/kg\n• LHV (LH2) = 120.0 MJ/kg\n• Energy Ratio: 42.8 / 120.0 = 0.3567"),
        ("Converted Liquid Hydrogen SFC:",
         "• LH2 Cruise SFC = 12.0 × 0.3567 ≈ 4.80 to 4.815 mg/(N·s)\n• LH2 Loiter SFC = 11.0 × 0.3567 ≈ 3.92 mg/(N·s)\n➔ Over 60% lower fuel mass flow rate than conventional Jet-A!")
    ]
    for i, (stitle, sdesc) in enumerate(sfc_points):
        p_t = tf_sfc.paragraphs[0] if i == 0 else tf_sfc.add_paragraph()
        p_t.text = stitle
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD_ACCENT
        p_t.space_before = Pt(10) if i > 0 else Pt(0)

        p_d = tf_sfc.add_paragraph()
        p_d.text = sdesc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: Aerodynamics & Drag Polar
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Aerodynamic Efficiency & Drag Polar Optimization")

    # Top Row: 4 Metric Cards
    aero_metrics = [
        ("ASPECT RATIO (AR)", "9.50", "Transonic Optimum", CYAN_ACCENT),
        ("WETTED RATIO (Swet/Sref)", "2.20", "High Volume Hull", EMERALD_ACCENT),
        ("MAX EFFICIENCY (L/D Max)", "30.8", "Loiter & Hold Phase", GOLD_ACCENT),
        ("CRUISE EFFICIENCY (L/D)", "26.7", "Mach 0.85 Range Max", CYAN_ACCENT)
    ]
    for i, (lbl, val, unt, col) in enumerate(aero_metrics):
        bx = Inches(0.8 + i * 2.98)
        add_kpi_card(slide5, bx, Inches(1.4), Inches(2.8), Inches(1.7), val, lbl, unt, value_color=col)

    # Bottom Left Card (Aerodynamic Principles)
    add_card(slide5, Inches(0.8), Inches(3.3), Inches(5.75), Inches(3.6))
    tb_a1 = slide5.shapes.add_textbox(Inches(1.0), Inches(3.5), Inches(5.35), Inches(3.2))
    tf_a1 = tb_a1.text_frame
    tf_a1.word_wrap = True
    p = tf_a1.paragraphs[0]
    p.text = "Parabolic Drag Polar Formulation:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    p = tf_a1.add_paragraph()
    p.text = "• Zero-Lift Drag (CD0): 0.0150 (smooth composite BWB surface)\n• Oswald Span Factor (e): 0.85 with 70° canted winglets\n• Optimal Lift-to-Drag Ratio:\n   (L/D)_max = 0.5 × sqrt(π × AR × e / CD0)\n• Long-Range Cruise Condition:\n   (L/D)_cruise = 0.866 × (L/D)_max (maximizes V × L/D range factor)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT

    # Bottom Right Card (BWB Aerodynamic Advantages)
    add_card(slide5, Inches(6.75), Inches(3.3), Inches(5.78), Inches(3.6))
    tb_a2 = slide5.shapes.add_textbox(Inches(6.95), Inches(3.5), Inches(5.38), Inches(3.2))
    tf_a2 = tb_a2.text_frame
    tf_a2.word_wrap = True
    p = tf_a2.paragraphs[0]
    p.text = "Blended Wing Body Advantages:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    p = tf_a2.add_paragraph()
    p.text = "• Lifting Fuselage: Centerbody generates ~45% of total aircraft lift, reducing required wing loading.\n• Lower Wetted Area per Passenger: Reduces parasitic drag per seat by ~20% compared to circular tube-and-wing.\n• Spanwise Camber & Winglets: Endplates lower induced drag while remaining strictly within the 80m Code F gate limit."
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: Aircraft Mass Sizing (MTOW)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Aircraft Weight Buildup & Sizing Convergence")

    # Left Card (Mass Buildup Table)
    add_card(slide6, Inches(0.8), Inches(1.4), Inches(6.8), Inches(5.5))
    tb_tbl = slide6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(6.4), Inches(5.1))
    tf_tbl = tb_tbl.text_frame
    tf_tbl.word_wrap = True
    
    p = tf_tbl.paragraphs[0]
    p.text = "Mass Breakdown (Converged Sizing Model):"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    table_lines = [
        ("Maximum Take-Off Weight (MTOW)", "235,460 kg (235.5 t)", "100.0%"),
        ("Operating Empty Weight (OEW / We)", "155,600 kg (155.6 t)", "66.0%"),
        ("  • Baseline Airframe & Systems", "120,200 kg (120.2 t)", "51.0%"),
        ("  • Cryogenic LH2 Tanks (6 Tanks)", "35,400 kg (35.4 t)", "15.0%"),
        ("Design Payload (430 Pax + Cargo)", "53,750 kg (53.8 t)", "22.8%"),
        ("Usable Liquid Hydrogen Fuel", "24,850 to 39,330 kg", "~11–17%"),
        ("Flight & Cabin Crew (12 Crew)", "1,260 kg (1.26 t)", "0.5%")
    ]
    for name, val, pct in table_lines:
        p_row = tf_tbl.add_paragraph()
        p_row.text = f"• {name:<36} : {val:>18}  ({pct})"
        p_row.font.name = "Courier New" if "•" in name else FONT_BODY
        p_row.font.size = Pt(10.5)
        p_row.font.bold = "MTOW" in name or "OEW" in name
        p_row.font.color.rgb = GOLD_ACCENT if "MTOW" in name or "OEW" in name else TEXT_LIGHT

    # Right Card (Cryotank Packaging Physics)
    add_card(slide6, Inches(7.8), Inches(1.4), Inches(4.733), Inches(5.5))
    tb_tphys = slide6.shapes.add_textbox(Inches(8.0), Inches(1.6), Inches(4.333), Inches(5.1))
    tf_tp = tb_tphys.text_frame
    tf_tp.word_wrap = True
    
    p = tf_tp.paragraphs[0]
    p.text = "Cryotank Gravimetric Sizing:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    p = tf_tp.add_paragraph()
    p.text = "• Gravimetric Index (Gi = 0.50):\n   Gi = M_fuel / (M_fuel + M_tank)\n   Dry tank structural mass equals fuel mass.\n\n• 6 Cylindrical Vessels:\n   4 Wing Shoulder + 2 Aft Core tanks.\n   Average Dry Mass = 5,900 kg / tank.\n\n• Thermal & Pressure Boundary:\n   - 20.3 K (-253 °C) liquid temperature\n   - 2.0 bar operating pressure\n   - Double-walled Multi-Layer Insulation (MLI) with evacuated vacuum jacket."
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 7: The Concept (Digital Engineering Blueprint)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "The Concept: 80m Blended Wing Body Digital Blueprint")

    # Main Blueprint Stage Card
    add_card(slide7, Inches(0.8), Inches(1.35), Inches(11.733), Inches(5.6))
    if os.path.exists(img4_concept):
        slide7.shapes.add_picture(img4_concept, Inches(1.1), Inches(1.45), width=Inches(11.133))

    # =========================================================================
    # SLIDE 8: 3D CAD Parametric Model (OpenVSP 3.51.3)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "3D Parametric CAD Model & Surface Mesh (OpenVSP 3.51.3)")

    # Main CAD Multi-view Card
    add_card(slide8, Inches(0.8), Inches(1.35), Inches(11.733), Inches(5.6))
    if os.path.exists(img_cad_3d):
        slide8.shapes.add_picture(img_cad_3d, Inches(1.05), Inches(1.45), width=Inches(11.233))

    # =========================================================================
    # SLIDE 9: Key Innovations & Next Steps (DT2 Readiness)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Design Innovations & Future Work (Design Task 2)")

    # 3 Pillar Cards
    pillars = [
        ("1. Unified Passenger Deck",
         "• 430 Pax widebody theater layout (20m × 14m × 2.4m).\n• 4 continuous aisles with rapid emergency evacuation egress.\n• Eliminates isolated rows while preserving generous stand-up headroom.",
         CYAN_ACCENT),
        ("2. Balanced Fuel Packaging",
         "• 6 symmetrical cryotanks placed in wing shoulders and aft core.\n• Minimal CG travel during flight, avoiding trim drag penalties.\n• Total storage volume: 610 m³ liquid hydrogen.",
         EMERALD_ACCENT),
        ("3. Acoustic Shielding & Ops",
         "• Twin top-mounted turbofans shielded by upper aft deck.\n• 80m span strictly respects ICAO Code F airport infrastructure.\n• 3-point heavy landing gear ensures ground clearance.",
         GOLD_ACCENT)
    ]
    for i, (title, desc, col) in enumerate(pillars):
        bx = Inches(0.8 + i * 3.98)
        add_card(slide9, bx, Inches(1.4), Inches(3.78), Inches(3.4))
        tb = slide9.shapes.add_textbox(bx + Inches(0.2), Inches(1.55), Inches(3.38), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_TITLE
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Bottom Card (Next Steps for DT2)
    add_card(slide9, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.9))
    tb_nxt = slide9.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(11.333), Inches(1.6))
    tf_nxt = tb_nxt.text_frame
    tf_nxt.word_wrap = True
    
    p = tf_nxt.paragraphs[0]
    p.text = "Roadmap for Design Task 2 (DT2 Detailed Aerodynamics & Structure):"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf_nxt.add_paragraph()
    p.text = "• 3D High-Fidelity CFD in Siemens STAR-CCM+ to validate transonic cruise polars (M0.85, Re = 45M).\n• Finite Element Structural Optimization for multi-bubble pressurized cabin bulkheads and wing spars.\n• Dynamic Stability & Control evaluation with winglet rudders and elevon sizing."
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 10: Academic References
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Academic & Industry References")

    refs = [
        ("NASA Technical Reports Server (NTRS)",
         "NASA/CR-2012-217578: Aerodynamic Design and Performance Analysis of Advanced Blended-Wing-Body Transports",
         "https://ntrs.nasa.gov/api/citations/20120001452/downloads/20120001452.pdf"),
        ("International Journal of Hydrogen Energy (ScienceDirect)",
         "Cryogenic Hydrogen Fuel Storage, Boil-off Management, and Sizing for Long-Range Civil Transports (2024)",
         "https://www.sciencedirect.com/science/article/pii/S036031992404535X#bib87"),
        ("Aircraft Design: A Conceptual Approach (D.P. Raymer, 6th Ed.)",
         "Statistical empty weight estimation, Breguet jet range sizing algorithms, and CS-25 reserve fuel compliance.",
         "AIAA Education Series (2018)"),
        ("Chalmers University of Technology MMS236 Lecture Series",
         "Lecture 2 (Atmospheric Modeling & Sizing Loops), Lecture 4 (Propulsion Trends & Cryogenic Hydrogen Aviation).",
         "Department of Mechanics and Maritime Sciences (2026)")
    ]
    for i, (title, desc, link) in enumerate(refs):
        by = Inches(1.4 + i * 1.35)
        add_card(slide10, Inches(0.8), by, Inches(11.733), Inches(1.2))
        tb = slide10.shapes.add_textbox(Inches(1.05), by + Inches(0.12), Inches(11.2), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_TITLE
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

        p = tf.add_paragraph()
        p.text = f"Source: {link}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # Save presentation
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[OK] Presentation successfully created: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_presentation()
