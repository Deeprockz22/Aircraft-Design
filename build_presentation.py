#!/usr/bin/env python3
"""
=============================================================================
Minimalist Presentation Builder: EXAELIA 80m Hydrogen BWB (MMS236 DT1)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Group 13: Johan Persson, Sai Srinivasa Manideep Jakka, Tobias Hilltorp, William Gustavsson

Design Language: Ultra-Clean Minimal Dark Studio
- Generous whitespace, no cluttered text blocks
- Large high-impact numbers and clean typography
- Hero images centered with elegant dark framing
=============================================================================
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette
# -----------------------------------------------------------------------------
BG_COLOR     = RGBColor(10, 13, 20)       # #0A0D14 Deep Carbon Matte
CARD_BG      = RGBColor(17, 22, 34)       # #111622 Minimalist Surface
BORDER_COLOR = RGBColor(30, 41, 59)       # #1E293B Subtle Border
CYAN_ACCENT  = RGBColor(56, 189, 248)     # #38BDF8 Electric Cyan
TEXT_WHITE   = RGBColor(248, 250, 252)    # #F8FAFC Crisp White
TEXT_LIGHT   = RGBColor(203, 213, 225)    # #CBD5E1 Slate 300
TEXT_MUTED   = RGBColor(148, 163, 184)    # #94A3B8 Slate 400
TEXT_SUBTLE  = RGBColor(100, 116, 139)    # #64748B Slate 500

FONT_HEADING = "Helvetica Neue"
FONT_BODY    = "Arial"

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, number_tag, title_text):
    # Category / Number tag
    tb_tag = slide.shapes.add_textbox(Inches(0.9), Inches(0.55), Inches(11.5), Inches(0.25))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = f"MMS236  •  GROUP 13  •  {number_tag}".upper()
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = CYAN_ACCENT

    # Minimalist Title
    tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(0.82), Inches(11.5), Inches(0.5))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

def add_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = BORDER_COLOR
    shape.line.width = Pt(0.75)
    return shape

def build_minimal_presentation(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    blank_layout = prs.slide_layouts[6]

    asset_dir = "/Users/jakkasaisrinivasamanideep/Documents/MMS236/04_Presentation_Assets"
    img1_sketch   = os.path.join(asset_dir, "image1.jpeg")
    img2_mission  = os.path.join(asset_dir, "image2.jpeg")
    img3_sfc      = os.path.join(asset_dir, "image3.png")
    img4_concept  = os.path.join(asset_dir, "image4.jpeg")
    img_cad_3d    = "/Users/jakkasaisrinivasamanideep/Documents/MMS236/03_CAD_OpenVSP_Models/exaelia_bwb_80m_3d_views.png"

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # University & Course Header
    tb = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "CHALMERS UNIVERSITY OF TECHNOLOGY  •  MMS236 AIRCRAFT DESIGN"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    # Main Title
    tb_title = slide1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(1.1))
    tf_title = tb_title.text_frame
    p_t = tf_title.paragraphs[0]
    p_t.text = "Aircraft Design, DT1"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(46)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    # Subtitle
    tb_sub = slide1.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(11.0), Inches(0.45))
    tf_sub = tb_sub.text_frame
    p_s = tf_sub.paragraphs[0]
    p_s.text = "EXAELIA — 80m Liquid Hydrogen Blended Wing Body Transport"
    p_s.font.name = FONT_HEADING
    p_s.font.size = Pt(18)
    p_s.font.color.rgb = TEXT_LIGHT

    # Author Roster & Group
    tb_auth = slide1.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(11.0), Inches(1.0))
    tf_auth = tb_auth.text_frame
    p_a1 = tf_auth.paragraphs[0]
    p_a1.text = "Johan Persson   •   Sai Srinivasa Manideep Jakka   •   Tobias Hilltorp   •   William Gustavsson"
    p_a1.font.name = FONT_BODY
    p_a1.font.size = Pt(14)
    p_a1.font.bold = True
    p_a1.font.color.rgb = TEXT_WHITE

    p_a2 = tf_auth.add_paragraph()
    p_a2.text = "Group 13"
    p_a2.font.name = FONT_BODY
    p_a2.font.size = Pt(12)
    p_a2.font.color.rgb = TEXT_MUTED
    p_a2.space_before = Pt(4)

    # Key Specs Strip at bottom
    add_card(slide1, Inches(1.2), Inches(5.8), Inches(10.933), Inches(0.85))
    tb_stats = slide1.shapes.add_textbox(Inches(1.4), Inches(5.95), Inches(10.533), Inches(0.55))
    tf_stats = tb_stats.text_frame
    p_st = tf_stats.paragraphs[0]
    p_st.alignment = PP_ALIGN.CENTER
    p_st.text = "430 Passengers   |   12,500 km Range   |   Mach 0.85 at FL350   |   80.0 m Span (ICAO Code F)"
    p_st.font.name = FONT_BODY
    p_st.font.size = Pt(13)
    p_st.font.bold = True
    p_st.font.color.rgb = CYAN_ACCENT

    # =========================================================================
    # SLIDE 2: First Sketch
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Concept Origin", "First sketch")

    # Centered Sketch Card (height = 4.8 in, aspect ratio 0.707 -> width = 3.40 in)
    add_card(slide2, Inches(4.7), Inches(1.5), Inches(3.933), Inches(5.0))
    if os.path.exists(img1_sketch):
        slide2.shapes.add_picture(img1_sketch, Inches(4.9), Inches(1.6), height=Inches(4.8))

    # Caption Tag
    tb_cap2 = slide2.shapes.add_textbox(Inches(0.9), Inches(6.75), Inches(11.533), Inches(0.35))
    tf_cap2 = tb_cap2.text_frame
    p_c2 = tf_cap2.paragraphs[0]
    p_c2.alignment = PP_ALIGN.CENTER
    p_c2.text = "Initial hand-drawn configuration sketch  •  80 m wingspan blended wing body planform"
    p_c2.font.name = FONT_BODY
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: Sizing Mission
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Mission Profile", "Sizing mission")

    # Centered Mission Diagram Card (height = 4.7 in, aspect ratio 1.278 -> width = 6.0 in)
    add_card(slide3, Inches(3.3), Inches(1.5), Inches(6.733), Inches(5.0))
    if os.path.exists(img2_mission):
        slide3.shapes.add_picture(img2_mission, Inches(3.66), Inches(1.65), height=Inches(4.7))

    # Caption Tag
    tb_cap3 = slide3.shapes.add_textbox(Inches(0.9), Inches(6.75), Inches(11.533), Inches(0.35))
    tf_cap3 = tb_cap3.text_frame
    p_c3 = tf_cap3.paragraphs[0]
    p_c3.alignment = PP_ALIGN.CENTER
    p_c3.text = "Design Range: 12,500 km at FL350 (M0.85)  •  200 nm Diversion  •  30 min Loiter + 3% Contingency"
    p_c3.font.name = FONT_BODY
    p_c3.font.size = Pt(11)
    p_c3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Engine Performance
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Propulsion Modeling", "Engine performance")

    # Left: Clean Chart Card
    add_card(slide4, Inches(0.9), Inches(1.5), Inches(6.6), Inches(5.0))
    if os.path.exists(img3_sfc):
        slide4.shapes.add_picture(img3_sfc, Inches(1.15), Inches(1.75), width=Inches(6.1))

    # Right: 2 Minimal Data Cards
    # Card 1: 2050 Trend
    add_card(slide4, Inches(7.8), Inches(1.5), Inches(4.633), Inches(2.35))
    tb4_1 = slide4.shapes.add_textbox(Inches(8.1), Inches(1.7), Inches(4.0), Inches(1.9))
    tf4_1 = tb4_1.text_frame
    p = tf4_1.paragraphs[0]
    p.text = "2050 SFC TREND (JET-A)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p = tf4_1.add_paragraph()
    p.text = "12.0 mg/Ns"
    p.font.name = FONT_HEADING
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(3)

    p = tf4_1.add_paragraph()
    p.text = "Baseline historical turbofan efficiency trend"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT
    p.space_before = Pt(3)

    # Card 2: LH2 Equivalent
    add_card(slide4, Inches(7.8), Inches(4.15), Inches(4.633), Inches(2.35))
    tb4_2 = slide4.shapes.add_textbox(Inches(8.1), Inches(4.35), Inches(4.0), Inches(1.9))
    tf4_2 = tb4_2.text_frame
    p = tf4_2.paragraphs[0]
    p.text = "LH2 EQUIVALENT SFC"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf4_2.add_paragraph()
    p.text = "4.8 mg/Ns"
    p.font.name = FONT_HEADING
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(3)

    p = tf4_2.add_paragraph()
    p.text = "2.8× higher energy density (120 MJ/kg vs 42.8 MJ/kg)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT
    p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: Aerodynamics
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Aerodynamic Efficiency", "Aerodynamics")

    # 4 Large Clean Data Tiles (2x2 Grid)
    aero_cards = [
        ("ASPECT RATIO", "9.5", "Transonic planform optimum", TEXT_WHITE),
        ("WETTED RATIO (Swet / Sref)", "2.2", "High volumetric packaging efficiency", CYAN_ACCENT),
        ("MAX EFFICIENCY (L/D Max)", "30.8", "Maximum loiter & hold efficiency", TEXT_WHITE),
        ("CRUISE EFFICIENCY (L/D Cruise)", "26.7", "Optimal Mach 0.85 long-range condition", CYAN_ACCENT)
    ]
    for idx, (lbl, val, desc, col) in enumerate(aero_cards):
        row = idx // 2
        col_idx = idx % 2
        bx = Inches(0.9 + col_idx * 5.9)
        by = Inches(1.5 + row * 2.6)
        
        add_card(slide5, bx, by, Inches(5.633), Inches(2.35))
        
        tb = slide5.shapes.add_textbox(bx + Inches(0.4), by + Inches(0.3), Inches(4.8), Inches(1.75))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = lbl
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.name = FONT_HEADING
        p_val.font.size = Pt(38)
        p_val.font.bold = True
        p_val.font.color.rgb = col
        p_val.space_before = Pt(2)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = TEXT_LIGHT
        p_desc.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: MTOW
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Mass Sizing", "MTOW")

    # 3 Large Minimalist Cards (3 Columns)
    mtow_cards = [
        ("MAXIMUM TAKE-OFF WEIGHT", "235,460 kg", "~235.5 tonnes", "Converged mission sizing", TEXT_WHITE),
        ("OPERATING EMPTY WEIGHT", "155,600 kg", "We / W0 = 0.66", "Raymer statistical method", CYAN_ACCENT),
        ("CRYOGENIC LH2 TANKS", "35,400 kg", "6 × 5,900 kg", "Gravimetric index Gi = 0.50", TEXT_WHITE)
    ]
    for idx, (title, val, sub, note, col) in enumerate(mtow_cards):
        bx = Inches(0.9 + idx * 3.9)
        by = Inches(1.5)
        
        add_card(slide6, bx, by, Inches(3.733), Inches(5.0))
        
        tb = slide6.shapes.add_textbox(bx + Inches(0.35), by + Inches(0.4), Inches(3.0), Inches(4.2))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.name = FONT_HEADING
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = col
        p_val.space_before = Pt(8)

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_HEADING
        p_sub.font.size = Pt(15)
        p_sub.font.bold = True
        p_sub.font.color.rgb = CYAN_ACCENT if col == TEXT_WHITE else TEXT_LIGHT
        p_sub.space_before = Pt(4)

        p_note = tf.add_paragraph()
        p_note.text = note
        p_note.font.name = FONT_BODY
        p_note.font.size = Pt(12)
        p_note.font.color.rgb = TEXT_SUBTLE
        p_note.space_before = Pt(28)

    # =========================================================================
    # SLIDE 7: The Concept
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Configuration", "The concept")

    # Centered Concept Stage Card (height = 4.8 in, aspect ratio 1.339 -> width = 6.43 in)
    add_card(slide7, Inches(3.0), Inches(1.5), Inches(7.333), Inches(5.0))
    if os.path.exists(img4_concept):
        slide7.shapes.add_picture(img4_concept, Inches(3.45), Inches(1.6), height=Inches(4.8))

    # Caption Tag
    tb_cap7 = slide7.shapes.add_textbox(Inches(0.9), Inches(6.75), Inches(11.533), Inches(0.35))
    tf_cap7 = tb_cap7.text_frame
    p_c7 = tf_cap7.paragraphs[0]
    p_c7.alignment = PP_ALIGN.CENTER
    p_c7.text = "EXAELIA 80m Hydrogen BWB  •  430 Pax Theater Cabin  •  610 m³ Cryogenic Storage"
    p_c7.font.name = FONT_BODY
    p_c7.font.size = Pt(11)
    p_c7.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: 3D CAD Model (OpenVSP)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Parametric CAD", "3D CAD model")

    # Centered CAD Stage Card (height = 4.8 in, aspect ratio 1.407 -> width = 6.75 in)
    add_card(slide8, Inches(2.9), Inches(1.5), Inches(7.533), Inches(5.0))
    if os.path.exists(img_cad_3d):
        slide8.shapes.add_picture(img_cad_3d, Inches(3.29), Inches(1.6), height=Inches(4.8))

    # Caption Tag
    tb_cap8 = slide8.shapes.add_textbox(Inches(0.9), Inches(6.75), Inches(11.533), Inches(0.35))
    tf_cap8 = tb_cap8.text_frame
    p_c8 = tf_cap8.paragraphs[0]
    p_c8.alignment = PP_ALIGN.CENTER
    p_c8.text = "OpenVSP 3.51.3 Parametric Multi-View Render  •  Top, Isometric, Front & Side Views"
    p_c8.font.name = FONT_BODY
    p_c8.font.size = Pt(11)
    p_c8.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 9: References
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Bibliography", "References")

    refs = [
        ("NASA Technical Reports Server (NTRS)",
         "Aerodynamic Design and Performance Analysis of Advanced Blended-Wing-Body Transports",
         "https://ntrs.nasa.gov/api/citations/20120001452/downloads/20120001452.pdf"),
        ("International Journal of Hydrogen Energy (ScienceDirect)",
         "Civil Liquid Hydrogen Aircraft Design, Sizing and Cryogenic Storage Integration",
         "https://www.sciencedirect.com/science/article/pii/S036031992404535X#bib87")
    ]
    for idx, (source, title, url) in enumerate(refs):
        by = Inches(1.8 + idx * 2.3)
        add_card(slide9, Inches(0.9), by, Inches(11.533), Inches(2.0))
        
        tb = slide9.shapes.add_textbox(Inches(1.3), by + Inches(0.3), Inches(10.7), Inches(1.4))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = source
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_before = Pt(4)

        p_url = tf.add_paragraph()
        p_url.text = url
        p_url.font.name = "Courier New"
        p_url.font.size = Pt(10.5)
        p_url.font.color.rgb = TEXT_MUTED
        p_url.space_before = Pt(4)

    # Save to all target locations
    for p in output_paths:
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        prs.save(p)
        print(f"[OK] Saved: {os.path.abspath(p)}")

if __name__ == "__main__":
    targets = [
        "/Users/jakkasaisrinivasamanideep/Documents/MMS236/Aircraft_Design_DT1_EXAELIA_Group13.pptx",
        "/Users/jakkasaisrinivasamanideep/Downloads/Aircraft Design DT1.pptx",
        "/Users/jakkasaisrinivasamanideep/Desktop/Aircraft_Design_DT1_EXAELIA_Group13.pptx"
    ]
    build_minimal_presentation(targets)
