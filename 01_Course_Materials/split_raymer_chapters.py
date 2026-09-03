#!/usr/bin/env python3
"""
=============================================================================
Raymer Textbook Chapter Splitter
=============================================================================
Splits 'Aircraft Design: A Conceptual Approach' (Daniel P. Raymer)
into individual chapter PDFs with clean, descriptive filenames.
=============================================================================
"""

import os
import pypdf

def split_raymer_chapters(
    input_pdf="/Users/jakkasaisrinivasamanideep/Documents/MMS236/01_Course_Materials/Aircraft Design A Conceptual Approach - Daniel P Raymer.pdf",
    output_dir="/Users/jakkasaisrinivasamanideep/Documents/MMS236/01_Course_Materials/Raymer_Textbook_Chapters"
):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Reading {input_pdf}...")
    reader = pypdf.PdfReader(input_pdf)
    total_pages = len(reader.pages)
    print(f"Total pages in textbook: {total_pages}")

    # Offset between printed book pages and PDF pages is +14 (PDF index = printed_page + 13)
    # Define chapter list: (filename, start_printed_page, end_printed_page)
    chapters = [
        ("00_Frontmatter_and_Table_of_Contents.pdf", 1, 14, "Frontmatter & Table of Contents"), # PDF 1-14
        ("Chapter_01_Design_A_Separate_Discipline.pdf", 1, 2, "Chapter 1: Design—A Separate Discipline"),
        ("Chapter_02_Overview_of_Design_Process.pdf", 3, 10, "Chapter 2: Overview of the Design Process"),
        ("Chapter_03_Sizing_from_Conceptual_Sketch.pdf", 11, 32, "Chapter 3: Sizing from a Conceptual Sketch"),
        ("Chapter_04_Airfoil_and_Geometry_Selection.pdf", 33, 76, "Chapter 4: Airfoil and Geometry Selection"),
        ("Chapter_05_Thrust_to_Weight_and_Wing_Loading.pdf", 77, 100, "Chapter 5: Thrust-to-Weight Ratio and Wing Loading"),
        ("Chapter_06_Initial_Sizing.pdf", 101, 116, "Chapter 6: Initial Sizing"),
        ("Chapter_07_Configuration_Layout_and_Loft.pdf", 117, 154, "Chapter 7: Configuration Layout and Loft"),
        ("Chapter_08_Special_Considerations_in_Layout.pdf", 155, 180, "Chapter 8: Special Considerations in Configuration Layout"),
        ("Chapter_09_Crew_Passengers_and_Payload.pdf", 181, 192, "Chapter 9: Crew Station, Passengers, and Payload"),
        ("Chapter_10_Propulsion_and_Fuel_System_Integration.pdf", 193, 228, "Chapter 10: Propulsion and Fuel System Integration"),
        ("Chapter_11_Landing_Gear_and_Subsystems.pdf", 229, 256, "Chapter 11: Landing Gear and Subsystems"),
        ("Chapter_12_Aerodynamics.pdf", 257, 312, "Chapter 12: Aerodynamics"),
        ("Chapter_13_Propulsion.pdf", 313, 332, "Chapter 13: Propulsion"),
        ("Chapter_14_Structures_and_Loads.pdf", 333, 394, "Chapter 14: Structures and Loads"),
        ("Chapter_15_Weights.pdf", 395, 410, "Chapter 15: Weights"),
        ("Chapter_16_Stability_Control_and_Handling_Qualities.pdf", 411, 454, "Chapter 16: Stability, Control, and Handling Qualities"),
        ("Chapter_17_Performance_and_Flight_Mechanics.pdf", 455, 500, "Chapter 17: Performance and Flight Mechanics"),
        ("Chapter_18_Cost_Analysis.pdf", 501, 518, "Chapter 18: Cost Analysis"),
        ("Chapter_19_Sizing_and_Trade_Studies.pdf", 519, 536, "Chapter 19: Sizing and Trade Studies"),
        ("Chapter_20_VTOL_Aircraft_Design.pdf", 537, 558, "Chapter 20: VTOL Aircraft Design"),
        ("Chapter_21_Conceptual_Design_Examples.pdf", 559, 657, "Chapter 21: Conceptual Design Examples"),
        ("Appendices_and_Index.pdf", 658, 746, "Appendices (Atmosphere, Airfoils, Engines) & Index")
    ]

    offset = 14 # Printed page 1 corresponds to PDF page 15 (index 14)

    for idx, (filename, start_p, end_p, title) in enumerate(chapters):
        writer = pypdf.PdfWriter()
        
        if idx == 0:
            pdf_start = 0
            pdf_end = 14
        else:
            pdf_start = start_p + offset - 1
            pdf_end = min(end_p + offset, total_pages)

        for p in range(pdf_start, pdf_end):
            writer.add_page(reader.pages[p])

        out_path = os.path.join(output_dir, filename)
        with open(out_path, "wb") as f_out:
            writer.write(f_out)

        num_p = pdf_end - pdf_start
        print(f"[{idx+1}/{len(chapters)}] Extracted '{title}' -> {filename} ({num_p} pages, PDF p.{pdf_start+1}-{pdf_end})")

    print(f"\n[OK] All {len(chapters)} chapters successfully saved to: {output_dir}")

if __name__ == "__main__":
    split_raymer_chapters()
