#!/usr/bin/env python3
"""
=============================================================================
Pure Black & White Minimalist Presentation: EXAELIA 80m BWB (MMS236 DT1)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Group 13: Johan Persson, Sai Srinivasa Manideep Jakka, Tobias Hilltorp, William Gustavsson

Design Language: Pure Black & White Swiss Architecture Style
- 100% authentic original graphs and figures (zero artificial plots)
- High-contrast stark black typography on clean white canvas
- Seamless integration: Original white-background graphs blend 100% invisibly
- Minimalist data cards with large punchy numbers
=============================================================================
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Pure Black & White Monochrome Palette
# -----------------------------------------------------------------------------
BG_COLOR     = RGBColor(255, 255, 255)    # #FFFFFF Pure Stark White
CARD_BG      = RGBColor(248, 250, 252)    # #F8FAFC Subtle Off-White Surface
BORDER_COLOR = RGBColor(226, 232, 240)    # #E2E8F0 Clean Hairline Border
TEXT_BLACK   = RGBColor(15, 23, 42)       # #0F172A Deep Jet Black
TEXT_DARK    = RGBColor(51, 65, 85)       # #334155 Slate 700
TEXT_MUTED   = RGBColor(100, 116, 139)    # #64748B Slate 500
TEXT_LIGHT   = RGBColor(148, 163, 184)    # #94A3B8 Slate 400

FONT_HEADING = "Helvetica Neue"
FONT_BODY    = "Arial"

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text=None):
    if category_text:
        tb_cat = slide.shapes.add_textbox(Inches(0.9), Inches(0.48), Inches(11.5), Inches(0.25))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_BODY
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEXT_MUTED

    tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(0.75), Inches(11.5), Inches(0.55))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_BLACK

def add_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = BORDER_COLOR
    shape.line.width = Pt(0.75)
    return shape

def build_presentation(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    blank_layout = prs.slide_layouts[6]

    # Exact original assets from user's downloaded presentation
    assets_dir = "/Users/jakkasaisrinivasamanideep/Documents/MMS236/04_Presentation_Assets/user_extracted"
    img_sketch  = os.path.join(assets_dir, "slide_2_Content Placeholder 4.jpg")
    img_mission = os.path.join(assets_dir, "slide_3_Content Placeholder 8.jpg")
    img_sfc     = os.path.join(assets_dir, "slide_4_Picture 6.png")
    img_concept = os.path.join(assets_dir, "slide_7_Picture 7.png")

    # =========================================================================
    # SLIDE 1: Title Slide (Swiss Minimalist Black & White)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # University & Course Header
    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(0.35))
    tf1 = tb1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "CHALMERS UNIVERSITY OF TECHNOLOGY  •  MMS236 AIRCRAFT DESIGN"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MUTED

    # Title
    tb_title = slide1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(1.1))
    tf_title = tb_title.text_frame
    p_t = tf_title.paragraphs[0]
    p_t.text = "Aircraft design, DT1"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(48)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_BLACK

    # Subtitle
    tb_sub = slide1.shapes.add_textbox(Inches(1.2), Inches(3.45), Inches(11.0), Inches(0.45))
    tf_sub = tb_sub.text_frame
    p_s = tf_sub.paragraphs[0]
    p_s.text = "EXAELIA — 80m Liquid Hydrogen Blended Wing Body Transport"
    p_s.font.name = FONT_HEADING
    p_s.font.size = Pt(18)
    p_s.font.color.rgb = TEXT_DARK

    # Authors & Group
    tb_auth = slide1.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(11.0), Inches(1.0))
    tf_auth = tb_auth.text_frame
    p_a1 = tf_auth.paragraphs[0]
    p_a1.text = "Johan Persson, Sai Srinivasa Manideep Jakka, Tobias Hilltorp, William Gustavsson"
    p_a1.font.name = FONT_BODY
    p_a1.font.size = Pt(14)
    p_a1.font.bold = True
    p_a1.font.color.rgb = TEXT_BLACK

    p_a2 = tf_auth.add_paragraph()
    p_a2.text = "Group 13"
    p_a2.font.name = FONT_BODY
    p_a2.font.size = Pt(13)
    p_a2.font.bold = True
    p_a2.font.color.rgb = TEXT_MUTED
    p_a2.space_before = Pt(4)

    # Key Specs Strip (Clean Minimalist Card)
    add_card(slide1, Inches(1.2), Inches(5.85), Inches(10.933), Inches(0.85))
    tb_stats = slide1.shapes.add_textbox(Inches(1.4), Inches(6.0), Inches(10.533), Inches(0.55))
    tf_stats = tb_stats.text_frame
    p_st = tf_stats.paragraphs[0]
    p_st.alignment = PP_ALIGN.CENTER
    p_st.text = "430 Passengers   |   12,500 km Range   |   Mach 0.85 at FL350   |   80.0 m Wingspan (ICAO Code F)"
    p_st.font.name = FONT_BODY
    p_st.font.size = Pt(12.5)
    p_st.font.bold = True
    p_st.font.color.rgb = TEXT_BLACK

    # =========================================================================
    # SLIDE 2: Blended wing body (Original Hand Sketch)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Blended wing body", "Concept Origin")

    # Center Hero Sketch (Original File)
    add_card(slide2, Inches(4.5), Inches(1.4), Inches(4.333), Inches(5.3))
    if os.path.exists(img_sketch):
        slide2.shapes.add_picture(img_sketch, Inches(4.86), Inches(1.5), height=Inches(5.1))

    # Caption Tag
    tb_cap2 = slide2.shapes.add_textbox(Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.35))
    tf_cap2 = tb_cap2.text_frame
    p_c2 = tf_cap2.paragraphs[0]
    p_c2.alignment = PP_ALIGN.CENTER
    p_c2.text = "Initial hand-drawn configuration sketch  •  80 m wingspan blended wing body planform"
    p_c2.font.name = FONT_BODY
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: Sizing mission (Original Authentic Course Graph)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Sizing mission", "Mission Profile")

    # The exact original mission profile graphic, centered seamlessly on white
    if os.path.exists(img_mission):
        slide3.shapes.add_picture(img_mission, Inches(3.54), Inches(1.45), height=Inches(4.9))

    # Minimal Caption
    tb_cap3 = slide3.shapes.add_textbox(Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.35))
    tf_cap3 = tb_cap3.text_frame
    p_c3 = tf_cap3.paragraphs[0]
    p_c3.alignment = PP_ALIGN.CENTER
    p_c3.text = "Design Range: 12,500 km at FL350 (M0.85)  •  200 nm Diversion  •  30 min Loiter + 3% Contingency"
    p_c3.font.name = FONT_BODY
    p_c3.font.size = Pt(11)
    p_c3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Engine performance (Original SFC Chart + User Bullets)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Engine performance", "Propulsion Modeling")

    # Left: The exact original SFC chart, full resolution, uncompressed
    if os.path.exists(img_sfc):
        slide4.shapes.add_picture(img_sfc, Inches(0.9), Inches(1.6), width=Inches(6.8))

    # Right: User's exact bullets as clean minimalist cards
    # Card 1: Trend line
    add_card(slide4, Inches(8.0), Inches(1.6), Inches(4.433), Inches(2.35))
    tb4_1 = slide4.shapes.add_textbox(Inches(8.3), Inches(1.85), Inches(3.8), Inches(1.85))
    tf4_1 = tb4_1.text_frame
    p = tf4_1.paragraphs[0]
    p.text = "FOLLOWING TREND LINE"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p = tf4_1.add_paragraph()
    p.text = "2050 SFC ~ 12.4 mg/Ns"
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_BLACK
    p.space_before = Pt(4)

    p = tf4_1.add_paragraph()
    p.text = "Baseline turbofan historical efficiency extrapolation"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(4)

    # Card 2: Hydrogen fuel conversion
    add_card(slide4, Inches(8.0), Inches(4.15), Inches(4.433), Inches(2.35))
    tb4_2 = slide4.shapes.add_textbox(Inches(8.3), Inches(4.4), Inches(3.8), Inches(1.85))
    tf4_2 = tb4_2.text_frame
    p = tf4_2.paragraphs[0]
    p.text = "HYDROGEN FUEL CONVERSION"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p = tf4_2.add_paragraph()
    p.text = "SFC ~ 5.0 mg/Ns"
    p.font.name = FONT_HEADING
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_BLACK
    p.space_before = Pt(4)

    p = tf4_2.add_paragraph()
    p.text = "Adjusted for liquid hydrogen (120 MJ/kg vs 42.8 MJ/kg)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: Aerodynamics (User's Updated Numbers)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Aerodynamics", "Aerodynamic Efficiency")

    # 4 Large Clean Data Tiles
    aero_items = [
        ("ASPECT RATIO", "5.0", "Full planform geometric ratio (b² / S_ref)"),
        ("SWET / SREF", "2.4", "High volumetric packaging efficiency"),
        ("L/D MAX", "24.5", "Maximum loiter & holding efficiency"),
        ("L/D CRUISE", "21.2", "Optimal Mach 0.85 long-range condition")
    ]
    for idx, (lbl, val, note) in enumerate(aero_items):
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
        p_val.font.size = Pt(42)
        p_val.font.bold = True
        p_val.font.color.rgb = TEXT_BLACK
        p_val.space_before = Pt(2)

        p_nt = tf.add_paragraph()
        p_nt.text = note
        p_nt.font.name = FONT_BODY
        p_nt.font.size = Pt(11.5)
        p_nt.font.color.rgb = TEXT_DARK
        p_nt.space_before = Pt(3)

    # Note at bottom for L/D Loiter = 24.5
    tb_loiter = slide5.shapes.add_textbox(Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.35))
    tf_loiter = tb_loiter.text_frame
    p_loiter = tf_loiter.paragraphs[0]
    p_loiter.alignment = PP_ALIGN.CENTER
    p_loiter.text = "Holding & Loiter Aerodynamic Efficiency: (L/D) Loiter = 24.5 (Jet Engine Loiter Maximum)"
    p_loiter.font.name = FONT_BODY
    p_loiter.font.size = Pt(11)
    p_loiter.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: MTOW (User's Updated Numbers)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "MTOW", "Mass Sizing")

    mtow_cards = [
        ("ASSUMPTION", "Aircraft design book", "Raymer statistical empty weight buildup method", "Raymer Methodology"),
        ("EMPTY WEIGHT FRACTION", "0.56", "We / W0 = 155,600 / 275,460 kg", "MTOW = 275,460 kg (~275.5 t)"),
        ("TANK MASS", "35,400 kg", "6 tanks × 5,900 kg", "Gravimetric index Gi = 0.50")
    ]
    for idx, (lbl, val, formula, note) in enumerate(mtow_cards):
        bx = Inches(0.9 + idx * 3.9)
        by = Inches(1.5)
        
        add_card(slide6, bx, by, Inches(3.733), Inches(5.0))
        
        tb = slide6.shapes.add_textbox(bx + Inches(0.35), by + Inches(0.4), Inches(3.0), Inches(4.2))
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
        p_val.font.size = Pt(26 if len(val) > 10 else 38)
        p_val.font.bold = True
        p_val.font.color.rgb = TEXT_BLACK
        p_val.space_before = Pt(8)

        p_form = tf.add_paragraph()
        p_form.text = formula
        p_form.font.name = FONT_HEADING
        p_form.font.size = Pt(13.5)
        p_form.font.bold = True
        p_form.font.color.rgb = TEXT_DARK
        p_form.space_before = Pt(6)

        p_note = tf.add_paragraph()
        p_note.text = note
        p_note.font.name = FONT_BODY
        p_note.font.size = Pt(11)
        p_note.font.color.rgb = TEXT_LIGHT
        p_note.space_before = Pt(26)

    # =========================================================================
    # SLIDE 7: The concept (AI enhanced sketch)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "The concept", "Configuration")

    # Subtitle badge: (AI enhanced sketch)
    tb_sub7 = slide7.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(11.5), Inches(0.35))
    tf_sub7 = tb_sub7.text_frame
    p_sub7 = tf_sub7.paragraphs[0]
    p_sub7.text = "(AI ENHANCED SKETCH)"
    p_sub7.font.name = FONT_BODY
    p_sub7.font.size = Pt(11)
    p_sub7.font.bold = True
    p_sub7.font.color.rgb = TEXT_MUTED

    # Exact Original Concept AI Enhanced Sketch
    if os.path.exists(img_concept):
        slide7.shapes.add_picture(img_concept, Inches(3.41), Inches(1.65), height=Inches(4.9))

    tb_cap7 = slide7.shapes.add_textbox(Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.35))
    tf_cap7 = tb_cap7.text_frame
    p_c7 = tf_cap7.paragraphs[0]
    p_c7.alignment = PP_ALIGN.CENTER
    p_c7.text = "EXAELIA 80m Hydrogen BWB  •  430 Pax Single-Deck Theater Cabin  •  610 m³ Cryogenic Storage"
    p_c7.font.name = FONT_BODY
    p_c7.font.size = Pt(11)
    p_c7.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: References (Clean B&W Cards)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "References", "Bibliography")

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
        add_card(slide8, Inches(0.9), by, Inches(11.533), Inches(2.0))
        
        tb = slide8.shapes.add_textbox(Inches(1.3), by + Inches(0.3), Inches(10.7), Inches(1.4))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = source
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_BLACK
        p_title.space_before = Pt(4)

        p_url = tf.add_paragraph()
        p_url.text = url
        p_url.font.name = "Courier New"
        p_url.font.size = Pt(10.5)
        p_url.font.color.rgb = TEXT_MUTED
        p_url.space_before = Pt(4)

    # Save presentation to all targets
    for p in output_paths:
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        prs.save(p)
        print(f"[OK] Saved: {os.path.abspath(p)}")

if __name__ == "__main__":
    targets = [
        "/Users/jakkasaisrinivasamanideep/Documents/MMS236/Aircraft_Design_DT1_EXAELIA_Group13.pptx",
        "/Users/jakkasaisrinivasamanideep/Downloads/Aircraft Design DT1 (1).pptx",
        "/Users/jakkasaisrinivasamanideep/Downloads/Aircraft Design DT1.pptx",
        "/Users/jakkasaisrinivasamanideep/Desktop/Aircraft_Design_DT1_EXAELIA_Group13.pptx"
    ]
    build_presentation(targets)
