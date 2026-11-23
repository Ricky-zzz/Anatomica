import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_apa_table_borders(table):
    """
    Apply APA table format:
    Top line (single thin), bottom line of header (single thin), bottom line of table (single thin).
    No vertical borders, no interior horizontal borders.
    """
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    # Header bottom border
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>\n'
                f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

def add_page_number_field(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def add_header_page_number(section):
    header = section.header
    header.is_linked_to_previous = False
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run()
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    add_page_number_field(run)

def set_section_page_numbering(section, start_type='arabic', start_num=1):
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn('w:pgNumType'))
    if pgNumType is None:
        pgNumType = OxmlElement('w:pgNumType')
        sectPr.append(pgNumType)
    if start_type == 'roman':
        pgNumType.set(qn('w:fmt'), 'romanLower')
    else:
        pgNumType.set(qn('w:fmt'), 'decimal')
    pgNumType.set(qn('w:start'), str(start_num))

class ThesisDocxBuilder:
    def __init__(self):
        self.doc = Document()
        self.setup_page_properties()

    def setup_page_properties(self):
        # Section 1: Preliminaries (Roman numerals)
        section = self.doc.sections[0]
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        # Margins: 1.5" Left (for binding), 1.0" Top, Right, Bottom
        section.left_margin = Inches(1.5)
        section.right_margin = Inches(1.0)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.different_first_page_header_footer = True

        add_header_page_number(section)
        set_section_page_numbering(section, start_type='roman', start_num=1)

        style_normal = self.doc.styles['Normal']
        font = style_normal.font
        font.name = 'Arial'
        font.size = Pt(12)
        font.color.rgb = RGBColor(0, 0, 0)

    def add_chapter_title(self, chapter_num, title_text):
        p1 = self.doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.line_spacing = 1.5
        p1.paragraph_format.space_before = Pt(24)
        p1.paragraph_format.space_after = Pt(12)
        run1 = p1.add_run(f"CHAPTER {chapter_num}\n\n{title_text.upper()}")
        run1.bold = True
        run1.font.name = 'Arial'
        run1.font.size = Pt(12)

    def add_preliminary_title(self, title_text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(title_text.upper())
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)

    def add_major_heading(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        return p

    def add_subcomponent(self, text):
        """Rule 5: Sub-components should be indented and italicized."""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        return p

    def add_sub_subcomponent(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.75)
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.italic = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        return p

    def add_body_paragraph(self, text, indent=True):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        return p

    def add_numbered_item(self, num_str, title, body_text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        
        run_num = p.add_run(f"{num_str}. ")
        run_num.font.name = 'Arial'
        run_num.font.size = Pt(12)
        
        if title:
            run_title = p.add_run(f"{title} ")
            run_title.bold = True
            run_title.font.name = 'Arial'
            run_title.font.size = Pt(12)
            
        run_body = p.add_run(body_text)
        run_body.font.name = 'Arial'
        run_body.font.size = Pt(12)
        return p

    def add_bullet_item(self, title, body_text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Inches(0.75)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        
        run_bullet = p.add_run("•  ")
        run_bullet.font.name = 'Arial'
        run_bullet.font.size = Pt(12)
        
        if title:
            run_title = p.add_run(f"{title}: ")
            run_title.bold = True
            run_title.font.name = 'Arial'
            run_title.font.size = Pt(12)
            
        run_body = p.add_run(body_text)
        run_body.font.name = 'Arial'
        run_body.font.size = Pt(12)
        return p

    def add_displayed_equation(self, eq_text, eq_num=None):
        """Rule 3: Exception to double spacing - Displayed equations are single line spacing"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        
        run = p.add_run(eq_text)
        run.italic = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        
        if eq_num:
            run_num = p.add_run(f"    ({eq_num})")
            run_num.italic = False
            run_num.font.name = 'Arial'
            run_num.font.size = Pt(12)
        return p

    def add_figure(self, fig_num_str, fig_title):
        """Rule 3: Exception to double spacing - Figures & captions are single spaced"""
        p_box = self.doc.add_paragraph()
        p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_box.paragraph_format.line_spacing = 1.0
        p_box.paragraph_format.space_before = Pt(14)
        p_box.paragraph_format.space_after = Pt(4)
        
        run_box = p_box.add_run(
            f"┌────────────────────────────────────────────────────────┐\n"
            f"│                 [ {fig_num_str}: {fig_title} ]                 │\n"
            f"│                                                        │\n"
            f"│       (Insert Architectural / Workflow Diagram Image)  │\n"
            f"└────────────────────────────────────────────────────────┘"
        )
        run_box.font.name = 'Consolas'
        run_box.font.size = Pt(9.5)
        run_box.font.color.rgb = RGBColor(90, 90, 90)

        p_cap = self.doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.line_spacing = 1.0
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        
        run_cap_lbl = p_cap.add_run(f"{fig_num_str}. ")
        run_cap_lbl.bold = True
        run_cap_lbl.font.name = 'Arial'
        run_cap_lbl.font.size = Pt(11)
        
        run_cap_txt = p_cap.add_run(fig_title)
        run_cap_txt.italic = True
        run_cap_txt.font.name = 'Arial'
        run_cap_txt.font.size = Pt(11)

    def add_table_title(self, table_num_str, table_title):
        """Rule 3 & 4: Table numbers, table titles single spaced, APA format"""
        p_num = self.doc.add_paragraph()
        p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_num.paragraph_format.line_spacing = 1.0
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(2)
        run_num = p_num.add_run(table_num_str)
        run_num.bold = True
        run_num.font.name = 'Arial'
        run_num.font.size = Pt(11)

        p_title = self.doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_title.paragraph_format.line_spacing = 1.0
        p_title.paragraph_format.space_before = Pt(0)
        p_title.paragraph_format.space_after = Pt(6)
        run_title = p_title.add_run(table_title)
        run_title.italic = True
        run_title.font.name = 'Arial'
        run_title.font.size = Pt(11)

    def add_reference_entry(self, ref_text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.space_before = Pt(0)
        
        parts = re.split(r'(\*.*?\*)', ref_text)
        for part in parts:
            if part.startswith('*') and part.endswith('*') and len(part) > 1:
                run = p.add_run(part[1:-1])
                run.italic = True
            else:
                run = p.add_run(part)
            run.font.name = 'Arial'
            run.font.size = Pt(11)
        return p

    def build_title_page(self):
        # Title page is single spaced, centered
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(12)
        
        run_inst = p.add_run("GOLDEN GATE COLLEGES\nCollege of Computer Studies\nBatangas City\n\n\n\n\n")
        run_inst.font.name = 'Arial'
        run_inst.font.size = Pt(12)
        
        run_title = p.add_run(
            "COMPARATIVE EVALUATION OF DIFFUSION-BASED VERSUS PARAMETRIC 3D GENERATION "
            "OF PATIENT FACIAL VISUALIZATIONS FROM CLINICAL SCENARIO DESCRIPTIONS "
            "IN AN EDUCATIONAL HOSPITAL INFORMATION SYSTEM\n\n\n\n\n"
        )
        run_title.bold = True
        run_title.font.name = 'Arial'
        run_title.font.size = Pt(14)
        
        run_sub = p.add_run(
            "A Capstone Project / Thesis Presented to\n"
            "The Faculty of the College of Computer Studies\n"
            "Golden Gate Colleges, Batangas City\n\n\n\n"
            "In Partial Fulfillment of the Requirements for the Degree\n"
            "Bachelor of Science in Computer Science\n\n\n\n\n"
        )
        run_sub.font.name = 'Arial'
        run_sub.font.size = Pt(12)
        
        run_author = p.add_run(
            "NATHANIEL PATRICK L. RAMOS\n"
            "Researcher\n\n\n"
            "November 2026\n"
        )
        run_author.bold = True
        run_author.font.name = 'Arial'
        run_author.font.size = Pt(12)

    def build_approval_sheet(self):
        self.doc.add_page_break()
        self.add_preliminary_title("Approval Sheet")
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.add_run(
            "This capstone project titled \"COMPARATIVE EVALUATION OF DIFFUSION-BASED VERSUS PARAMETRIC 3D "
            "GENERATION OF PATIENT FACIAL VISUALIZATIONS FROM CLINICAL SCENARIO DESCRIPTIONS IN AN EDUCATIONAL "
            "HOSPITAL INFORMATION SYSTEM\", prepared and submitted by NATHANIEL PATRICK L. RAMOS in partial fulfillment "
            "of the requirements for the degree Bachelor of Science in Computer Science, has been examined and recommended "
            "for oral examination and acceptance."
        )

        p_sig = self.doc.add_paragraph()
        p_sig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sig.paragraph_format.line_spacing = 1.15
        p_sig.paragraph_format.space_before = Pt(36)
        p_sig.add_run("______________________________\nAdviser\n\n\n")

        p_panel = self.doc.add_paragraph()
        p_panel.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_panel.paragraph_format.line_spacing = 2.0
        p_panel.paragraph_format.first_line_indent = Inches(0.5)
        p_panel.add_run(
            "Approved by the Committee on Oral Examination with a grade of ________ on November ____, 2026."
        )

        p_sigs = self.doc.add_paragraph()
        p_sigs.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sigs.paragraph_format.line_spacing = 1.15
        p_sigs.paragraph_format.space_before = Pt(36)
        p_sigs.add_run(
            "______________________________             ______________________________\n"
            "Panel Member                                Panel Member\n\n\n\n"
            "______________________________\n"
            "Dean, College of Computer Studies\n"
        )

    def build_acknowledgements(self):
        self.doc.add_page_break()
        self.add_preliminary_title("Acknowledgements")
        self.add_body_paragraph(
            "The researcher wishes to express his profound gratitude and sincere appreciation to the individuals whose "
            "guidance, expertise, and encouragement made the realization of this capstone research possible."
        )
        self.add_body_paragraph(
            "First, to Dr. Evan and the esteemed faculty members of the College of Nursing at Golden Gate Colleges, for their "
            "generous collaboration, clinical insight, and tireless evaluation sessions that defined the pedagogical requirements "
            "and sign catalogs of this study."
        )
        self.add_body_paragraph(
            "To the thesis adviser and panel of examiners, for their critical review, constructive critiques, and intellectual "
            "rigor that shaped the methodological design and experimental boundaries of this research."
        )
        self.add_body_paragraph(
            "To the researcher's family and colleagues, whose continuous moral, financial, and emotional support provided the "
            "resilience needed to bring this academic pursuit to fruition."
        )
        self.add_body_paragraph(
            "Above all, to Almighty God, the ultimate source of wisdom, strength, perseverance, and grace throughout this entire journey."
        )

    def build_abstract(self):
        self.doc.add_page_break()
        self.add_preliminary_title("Abstract")
        self.add_body_paragraph(
            "In simulation-based nursing education, clinical scenarios authored by instructors provide text descriptions of "
            "patient health conditions, yet learners are unable to physically observe the corresponding facial manifestations. "
            "Visual clinical indicators such as jaundice, cyanosis, pallor, and ptosis must be mentally conceptualized, creating "
            "extraneous cognitive load and risking inaccurate clinical recognition. While text-to-image generative models can "
            "synthesize facial representations, unconstrained diffusion models exhibit severe hallucinations, fail on asymmetric "
            "anatomical signs, and show persistent demographic skin-tone biases. Conversely, parametric three-dimensional head models "
            "offer deterministic control over anatomical coordinates and color albedo at the expense of photorealism."
        )
        self.add_body_paragraph(
            "This study investigates and compares two distinct rendering modalities—diffusion-based generative synthesis (Arm A) "
            "and parametric 3D head modeling utilizing FLAME 2023 Open (Arm B)—integrated within Chansey, an educational Hospital "
            "Information System (HIS), under a single constant agentic pipeline. The pipeline couples large language model text "
            "parsing, structured trait schema normalization, automated Vision-Language Model (VLM) verification, and human clinical "
            "approval. Using a pre-registered stimulus dataset of clinical scenario descriptions covering diffuse color signs, "
            "bilateral structural signs, and unilateral asymmetric signs across balanced Fitzpatrick/Monk skin tones, the two modalities "
            "are evaluated on per-trait fidelity, hallucination rates, faculty-rated clinical plausibility, teaching usefulness, "
            "skin-tone concordance, processing latency, and computational cost. This investigation provides empirical evidence on "
            "the comparative trade-offs between stochastic neural diffusion and deterministic parametric geometry for visual medical simulation."
        )
        
        p_kw = self.doc.add_paragraph()
        p_kw.paragraph_format.line_spacing = 2.0
        p_kw.paragraph_format.first_line_indent = Inches(0.5)
        p_kw.paragraph_format.space_before = Pt(12)
        r_kw_lbl = p_kw.add_run("Keywords: ")
        r_kw_lbl.bold = True
        r_kw_lbl.font.name = 'Arial'
        r_kw_lbl.font.size = Pt(12)
        r_kw_txt = p_kw.add_run(
            "Nursing Informatics, Generative AI, Medical Simulation, Diffusion Models, Parametric 3D Head, FLAME, Clinical Signs, Hospital Information Systems"
        )
        r_kw_txt.italic = True
        r_kw_txt.font.name = 'Arial'
        r_kw_txt.font.size = Pt(12)

    def build_toc(self):
        self.doc.add_page_break()
        self.add_preliminary_title("Table of Contents")
        
        toc_items = [
            ("TITLE PAGE", "i"),
            ("APPROVAL SHEET", "ii"),
            ("ACKNOWLEDGEMENTS", "iii"),
            ("ABSTRACT", "iv"),
            ("TABLE OF CONTENTS", "v"),
            ("LIST OF TABLES", "vi"),
            ("LIST OF FIGURES", "vii"),
            ("CHAPTER 1: THE PROBLEM AND ITS BACKGROUND", "1"),
            ("    Introduction", "1"),
            ("    Background of the Study", "1"),
            ("    Statement of the Problem", "4"),
            ("    Objectives of the Study", "5"),
            ("    Significance of the Study", "6"),
            ("    Scope and Limitations", "8"),
            ("    References", "10"),
            ("CHAPTER 2: REVIEW OF RELATED LITERATURE AND STUDIES", "13"),
            ("    Related Literature", "13"),
            ("        Generative AI and Image Synthesis", "13"),
            ("        Visual Failure in AI-Generated Clinical Images", "15"),
            ("        Skin-Tone Bias in AI-Generated Medical Images", "16"),
            ("        Generative AI in Nursing and Medical Education", "18"),
            ("        Parametric 3D Face Models", "19"),
            ("        VLM-Based Evaluation of Generated Images", "21"),
            ("        Ethics and Data Privacy", "22"),
            ("    Related Studies", "23"),
            ("    Gaps in the Literature", "25"),
            ("    Synthesis of the Reviewed Literature and Studies", "27"),
            ("    Theoretical Framework", "28"),
            ("        Simulation Fidelity Theory", "28"),
            ("        Cognitive Load Theory", "29"),
            ("        Multimedia Learning and Picture Superiority", "30"),
            ("        Application in the Study", "31"),
            ("    References", "32"),
            ("CHAPTER 3: METHODOLOGY", "37"),
            ("    Software Development Life Cycle (SDLC) Model", "37"),
            ("        1. Requirements Planning and Quick Design", "38"),
            ("        2. Prototype Cycles (Build, Demonstrate, Refine)", "38"),
            ("        3. Testing Phase", "39"),
            ("        4. Implementation Phase", "40"),
            ("    System Development Tools", "40"),
            ("        Programming Languages and Frameworks", "40"),
            ("        Integrated Development Environment (IDE)", "41"),
            ("        Database Management System", "41"),
            ("    Experimental Stimuli and Evaluation Dataset", "42"),
            ("    Algorithms and Modalities Applied", "43"),
            ("        Arm A: Diffusion-Based Image Generation (Gemini Image API)", "44"),
            ("        Arm B: Parametric 3D Head Generation (FLAME 2023 Open)", "45"),
            ("        Role of the Modalities in the System", "46"),
            ("    Methods of Evaluation", "47"),
            ("        1. Quantitative Trait Fidelity Metrics", "47"),
            ("        2. Skin-Tone Concordance", "48"),
            ("        3. Operational Performance Metrics", "49"),
            ("        4. Faculty Rating (Clinical Plausibility and Teaching Usefulness)", "49"),
            ("        5. Statistical Significance Testing", "51"),
            ("    System Architecture", "52"),
            ("        1. Presentation Layer", "53"),
            ("        2. Application Layer", "53"),
            ("        3. Data Layer", "54"),
            ("    Data Flow Diagram (DFD)", "54"),
            ("        Level 0 Data Flow Diagram (Context DFD)", "54"),
            ("        Level 1 Data Flow Diagram (Generation and Review Pipeline)", "55"),
            ("    Entity-Relationship Diagram (ERD)", "56"),
            ("        Database Table Descriptions", "57"),
            ("    Use Case Diagrams", "58"),
            ("        Faculty Use Case Diagram", "58"),
            ("        Student Use Case Diagram", "59"),
            ("    Sequence Diagram", "60"),
            ("    Machine Learning and Agent Pipeline Diagram", "61"),
            ("    Software Requirements Specification (SRS)", "62"),
            ("        Functional Requirements", "64"),
            ("        Non-Functional Requirements", "65"),
        ]

        for item, page in toc_items:
            p = self.doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.space_before = Pt(0)
            
            run_item = p.add_run(item)
            run_item.font.name = 'Arial'
            run_item.font.size = Pt(11)
            if item.startswith("CHAPTER") or item.isupper():
                run_item.bold = True
            
            # Tab stops or leader dots
            run_dots = p.add_run(f" {'.' * max(2, (68 - len(item)))} ")
            run_dots.font.name = 'Arial'
            run_dots.font.size = Pt(11)
            run_dots.font.color.rgb = RGBColor(140, 140, 140)
            
            run_pg = p.add_run(page)
            run_pg.font.name = 'Arial'
            run_pg.font.size = Pt(11)
            if item.startswith("CHAPTER"):
                run_pg.bold = True

    def build_list_of_tables(self):
        self.doc.add_page_break()
        self.add_preliminary_title("List of Tables")
        
        tables = [
            ("Table 3.1", "Five-Point Likert Scale Interpretation for Clinical Plausibility and Teaching Usefulness", "50"),
            ("Table 3.2", "System Requirements Specification (Hardware, Software, Network, and Environment)", "63"),
        ]

        for num, title, page in tables:
            p = self.doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.space_before = Pt(0)
            
            run_num = p.add_run(f"{num}. ")
            run_num.bold = True
            run_num.font.name = 'Arial'
            run_num.font.size = Pt(11)
            
            run_title = p.add_run(title)
            run_title.font.name = 'Arial'
            run_title.font.size = Pt(11)
            
            run_dots = p.add_run(f" {'.' * max(2, (60 - len(title)))} ")
            run_dots.font.name = 'Arial'
            run_dots.font.size = Pt(11)
            run_dots.font.color.rgb = RGBColor(140, 140, 140)
            
            run_pg = p.add_run(page)
            run_pg.bold = True
            run_pg.font.name = 'Arial'
            run_pg.font.size = Pt(11)

    def build_list_of_figures(self):
        self.doc.add_page_break()
        self.add_preliminary_title("List of Figures")
        
        figures = [
            ("Figure 3.1", "Rapid Application Development (RAD) Model", "38"),
            ("Figure 3.2", "Sample Outputs from the Evaluation Stimulus Set", "43"),
            ("Figure 3.3", "Comparison of Image Synthesis Pipelines", "44"),
            ("Figure 3.4", "Three-Tier System Architecture of the Chansey FaceGen Platform", "52"),
            ("Figure 3.5", "Level 0 Context Data Flow Diagram", "55"),
            ("Figure 3.6", "Level 1 Data Flow Diagram of the FaceGen Pipeline", "56"),
            ("Figure 3.7", "Entity-Relationship Diagram (ERD)", "57"),
            ("Figure 3.8", "Faculty Use Case Diagram", "58"),
            ("Figure 3.9", "Student Use Case Diagram", "59"),
            ("Figure 3.10", "Sequence Diagram for Patient Face Generation and Approval", "60"),
            ("Figure 3.11", "Constant Agentic Generation and Verification Pipeline", "61"),
        ]

        for num, title, page in figures:
            p = self.doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.space_before = Pt(0)
            
            run_num = p.add_run(f"{num}. ")
            run_num.bold = True
            run_num.font.name = 'Arial'
            run_num.font.size = Pt(11)
            
            run_title = p.add_run(title)
            run_title.font.name = 'Arial'
            run_title.font.size = Pt(11)
            
            run_dots = p.add_run(f" {'.' * max(2, (62 - len(title)))} ")
            run_dots.font.name = 'Arial'
            run_dots.font.size = Pt(11)
            run_dots.font.color.rgb = RGBColor(140, 140, 140)
            
            run_pg = p.add_run(page)
            run_pg.bold = True
            run_pg.font.name = 'Arial'
            run_pg.font.size = Pt(11)

    def start_main_section(self):
        """Transition from Roman Preliminaries to Arabic Page Numbering on Chapter 1"""
        section = self.doc.add_section()
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.left_margin = Inches(1.5)
        section.right_margin = Inches(1.0)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.different_first_page_header_footer = False

        add_header_page_number(section)
        set_section_page_numbering(section, start_type='arabic', start_num=1)

    def build_chapter_1(self):
        self.add_chapter_title("1", "The Problem and Its Background")
        
        self.add_major_heading("Introduction")
        self.add_body_paragraph(
            "This chapter gives the background of the study, the statement of the problem, the objectives, the significance, "
            "and the scope and limitations. The central concern is how well a generative AI pipeline can produce a patient face that "
            "shows the clinical signs described in a nursing scenario, and whether a diffusion-generated image or a parametric "
            "three-dimensional head rendering does it more faithfully."
        )

        self.add_major_heading("Background of the Study")
        self.add_body_paragraph(
            "Philippine nursing programs must train students to handle clinical problems safely, and the Commission on Higher "
            "Education requires outcome-based teaching to do it (Commission on Higher Education, 2017). Simulation carries much of "
            "that training because students can practice drug administration and emergency response without putting a real patient "
            "at risk (Bambini, 2016; Jeffries, 2012). This training needs faculty, and nursing schools do not have enough of them. "
            "In one urban area of the Central Philippines, most clinical instructors were part-time and had only a few years of "
            "service (Noblezada et al., 2025), and many experienced nurses keep leaving for jobs abroad (Alibudbud, 2023). The "
            "shortage is not only local. American nursing schools reported a 7.2 percent vacancy rate in full-time faculty posts and "
            "turned away more than 92,000 qualified applicants in a single year because they could not find enough teachers "
            "(American Association of Colleges of Nursing, 2025)."
        )
        self.add_body_paragraph(
            "Faculty also lose many hours writing the scenarios themselves. A complete scenario needs a patient history, changing "
            "vital signs, lab and imaging results, doctor's orders, medication records, and notes for the facilitator, and the "
            "writing process is time intensive (Bambini, 2016). The Healthcare Simulation Standards of Best Practice add more "
            "requirements, such as clear objectives, realistic detail, and a planned debriefing (Watts et al., 2021). Teachers who "
            "tried AI for the writing step said the tools produced a usable draft quickly, but that important details were often "
            "missing and someone still had to check the content before it was safe to use (Harder, 2023; Vaughn & Ford, 2024). Even "
            "when the scenario text is accurate, though, it leaves one thing missing. The student reads about a patient with jaundice, "
            "pallor, or ptosis, but cannot see that patient. Physical signs are visual; text describes them, but a description is not "
            "the same as seeing them, and that gap is what the student has to close through imagination every time."
        )
        self.add_body_paragraph(
            "Generative AI can produce faces from text, but the available evidence says that plain text-to-image models fail at "
            "this task when the signs are clinical. Kumar et al. (2024) tested DALL-E 2 and Midjourney on medical education "
            "illustrations for hypothyroidism and Horner syndrome. For hypothyroidism, whose signs are symmetric and generalized "
            "(facial puffiness, periorbital edema, and coarse features), the models performed relatively well. For Horner syndrome, "
            "which produces unilateral ptosis and anisocoria on one side of the face, both tools consistently failed to render the "
            "asymmetric signs accurately, producing symmetry-biased or anatomically distorted outputs even with repeated prompt "
            "refinements. Fan et al. (2023) generated faces with pathological features for medical education using DALL-E-powered "
            "tools and found that the approach showed potential for bypassing patient consent barriers, but cautioned that images "
            "require expert review before formal curriculum use. Haider et al. (2025) evaluated four text-to-image models "
            "(Midjourney, DALL-E 3, Gemini Ultra, Stable Diffusion) on craniofacial anatomy and found high inter-rater reliability "
            "among expert reviewers (ICC = 0.858), but all tested models produced critical structural flaws, including missing "
            "foramina, incorrect suture lines, and misconfigured neurovascular pathways. A 2025 evaluation of DALL-E 3 for pediatric "
            "ophthalmology educational images similarly found poor accuracy for clinical features, reporting a median pathological "
            "accuracy score of only 1 out of 15 (Jong et al., 2025). The pattern across these studies is consistent: these models "
            "can generate a face that looks like a person, but they cannot reliably render a specific, documented clinical sign on "
            "that face, especially when the sign is asymmetric or requires precise regional anatomy."
        )
        self.add_body_paragraph(
            "The failure is not only about sign accuracy. Skin-tone representation is a documented problem that matters for nursing "
            "education in a country as demographically diverse as the Philippines. Joerg et al. (2025) analyzed 4,000 dermatology "
            "images generated by leading text-to-image models and found that 89.8 percent depicted light skin tones. When blinded "
            "dermatology residents reviewed the same images for clinical accuracy, only 15 percent were correctly identified as "
            "accurately depicting the intended skin condition. O'Malley et al. (2024) showed that injecting an explicit demographic "
            "description into the prompt substantially shifted the skin-tone distribution toward the intended population (P = .04 "
            "for the corrected distribution against expected demographics), but the correction required deliberate engineering and "
            "did not happen by default with standard prompts. Most studies on AI-generated clinical images test one model on one "
            "condition, usually dermatology or ophthalmology, and few look at whether the rendering method itself changes sign "
            "accuracy. No study found in the literature compared two rendering modalities, diffusion-generated photographs versus a "
            "parametric three-dimensional head, for the same clinical signs, using the same pipeline, with nursing faculty as raters, "
            "inside a working school hospital information system. That is the gap this study fills."
        )

        self.add_major_heading("Statement of the Problem")
        self.add_body_paragraph(
            "Nursing scenario descriptions give students the text of a patient's condition, but not a face. Physical signs such as "
            "jaundice, ptosis, facial droop, cyanosis, and pallor are visual; students must imagine them from prose, which introduces "
            "the risk of forming an inaccurate or incomplete mental image before they ever see the real sign in clinic. Generative AI "
            "can produce faces from text, but plain text-to-image models are documented to fail on clinical facial signs, especially "
            "asymmetric ones. Both diffusion-generated photographs and parametric three-dimensional head models can, in principle, "
            "render signs from a structured description, but they work in different ways and have different failure modes. No study "
            "in the literature has run both under the same pipeline with the same evaluation criteria and had clinical educators "
            "judge the results."
        )
        self.add_body_paragraph(
            "This study therefore builds a scenario-to-face generation pipeline integrated into Chansey, an educational hospital "
            "information system, and compares diffusion-generated images against parametric 3D head outputs under a single constant "
            "agentic pipeline. It answers the following specific research questions:"
        )
        self.add_numbered_item("1", "Trait Fidelity:", "What is the per-trait fidelity of diffusion-generated PNG versus parametric 3D generated patient faces, measured as trait recall rate and number of hallucinated extra signs, against a clinician-authored trait checklist?")
        self.add_numbered_item("2", "Clinical Plausibility & Utility:", "What is the clinical plausibility and teaching usefulness of each rendering modality, as rated by Nursing Department faculty?")
        self.add_numbered_item("3", "Statistical Significance:", "Is there a significant difference between the two modalities on trait fidelity, faculty-rated plausibility, and skin-tone fidelity?")
        self.add_numbered_item("4", "Operational Performance:", "What is the latency, token cost, and GPU requirement of each modality under the same pipeline?")
        self.add_numbered_item("5", "Institutional Suitability:", "Which modality is more suitable for patient face visualization in Chansey, and why?")

        self.add_major_heading("Objectives of the Study")
        self.add_body_paragraph(
            "This study develops and evaluates a patient-face generation pipeline embedded in the Faculty Scenario Builder of "
            "Chansey, an educational hospital information system. The pipeline parses a scenario description into a structured trait "
            "schema, renders two versions of the patient face through different modalities, verifies each output, and routes it for "
            "faculty approval. Specifically, this study aims to accomplish the following:"
        )
        self.add_numbered_item("1", "Pipeline Design & Construction:", "Design and build the scenario-to-face generation pipeline as a Python microservice that the Laravel Chansey application calls through an HTTP interface, including a parser, an expander for disease-only inputs, a diffusion renderer, a parametric 3D renderer, and a VLM-based verifier.")
        self.add_numbered_item("2", "Trait Fidelity & Plausibility Evaluation:", "Evaluate the per-trait fidelity of each modality, measuring trait recall rate and the count of hallucinated extra signs against a clinician-authored checklist, and assess faculty-rated clinical plausibility and teaching usefulness (RQ1, RQ2).")
        self.add_numbered_item("3", "Comparative Hypothesis Testing:", "Determine whether a statistically significant difference exists between the two modalities on trait fidelity, clinical plausibility, and skin-tone fidelity (RQ3).")
        self.add_numbered_item("4", "Computational & Resource Profiling:", "Measure the latency, token cost, and GPU requirement of each modality under the same pipeline for realistic classroom deployment assessment (RQ4).")
        self.add_numbered_item("5", "Modality Recommendation:", "Recommend the more suitable modality for patient face visualization in Chansey, supported by the evidence from objectives 2 through 4 (RQ5).")

        self.add_major_heading("Significance of the Study")
        self.add_body_paragraph(
            "This study examines whether a generative pipeline that runs two different rendering modalities can produce a reliable "
            "visual of the patient described in a nursing scenario. The findings provide substantial contributions to the following stakeholders:"
        )
        self.add_body_paragraph(
            "Nursing Department Faculty. It will help Nursing Department faculty by giving them a tested face generation tool inside "
            "the scenario builder they already use. A faculty member can type a patient description or a diagnosis and receive a "
            "rendered patient face for that scenario without sourcing copyrighted textbook images or using real patient photographs. "
            "The tool keeps every generated face under faculty approval before it attaches to a scenario, so clinical control stays with the instructor."
        )
        self.add_body_paragraph(
            "Nursing Students. It will help nursing students by closing the gap between a written scenario and the physical appearance "
            "of the condition it describes. When students see a rendered face showing ptosis, jaundice, or cyanosis next to the scenario "
            "text, they practice matching visual signs to clinical language before they encounter those signs in a real patient. The study "
            "also measures whether either rendering modality represents darker skin tones accurately, because students in the Philippines "
            "need to recognize signs across diverse skin presentations."
        )
        self.add_body_paragraph(
            "Developers and Nursing Informatics Researchers. It will help developers and nursing informatics researchers by providing "
            "measured evidence on two rendering approaches applied to clinical facial signs, an area with few faculty-rated results "
            "inside a working school system. The trait schema, rubric, verifier design, and audit trails the pipeline produces are reusable "
            "for future work, including fine-tuned models once the system has accumulated a corpus of instructor-approved images."
        )
        self.add_body_paragraph(
            "Educational Institutions and Training Programs. It will help schools and training programs by demonstrating a path to patient "
            "face generation that does not require real patient photographs, does not need a GPU on site, and keeps every output under "
            "faculty review before any student sees it. That design supports the outcome-based teaching standards that CHED Memorandum "
            "Order No. 15 requires of nursing programs (Commission on Higher Education, 2017)."
        )
        self.add_body_paragraph(
            "Future Researchers. It will help future researchers by leaving a documented pipeline, a pre-registered test set of scenario "
            "descriptions, an evaluation rubric, and an audit dataset that can be extended to more signs, other body regions, larger rater "
            "pools, or a fine-tuned renderer trained on approved images."
        )

        self.add_major_heading("Scope and Limitations")
        self.add_body_paragraph(
            "This study covers the design, development, and evaluation of a patient-face generation pipeline integrated into the "
            "Faculty Scenario Builder of Chansey, an educational hospital information system. The pipeline generates faces from "
            "faculty-authored scenario descriptions and operates through a Python microservice that Chansey calls over HTTP. Both "
            "rendering modalities use the same agentic pipeline: a large language model parses the input into a structured trait "
            "schema, an expander handles disease-only inputs by proposing visible signs for instructor confirmation, a renderer produces "
            "the output for each modality, and a VLM-based verifier checks each trait against the rendered image before the face "
            "reaches faculty approval."
        )
        self.add_body_paragraph(
            "The study compares two rendering modalities. Arm A is diffusion-based image generation, which runs through a commercial "
            "image API and produces a photograph-style PNG. Arm B is parametric 3D head generation, which uses FLAME 2023 Open (CC-BY-4.0) "
            "to produce a stylized head rendered to a static profile PNG. Both modalities use the same commercial large language model "
            "through an API. The study uses models through APIs and does not train or fine-tune any model; training is future work "
            "contingent on accumulating a corpus of instructor-approved images. The experimental stimuli are a pre-registered set of 24 "
            "to 30 scenario descriptions covering color signs (jaundice, pallor, cyanosis, flushing), structural and asymmetric signs "
            "(ptosis, facial droop, periorbital edema), and secretions (rhinorrhea), across both sexes and the full Monk/Fitzpatrick "
            "skin-tone range. Nursing Department faculty rate the generated faces on a rubric covering trait accuracy, clinical plausibility, "
            "and teaching usefulness. The face scope covers the head only; full-body generation is out of scope."
        )
        self.add_body_paragraph(
            "The study has limits. The test set is small, so results come from one school and may not generalize to other programs or "
            "sign catalogs. All faces are synthetic; no real patient photographs are used at any stage. The raters are Nursing Department "
            "faculty, not licensed physicians, so the study does not claim physician-level diagnostic accuracy. The diffusion arm runs on "
            "a hosted API, and a change in the provider's model version or pricing can affect repeat results over time. The parametric 3D "
            "arm contains a planned go/no-go spike for unilateral blendshapes (ptosis, facial droop); if that spike fails, the arm's "
            "sign set reshuffles to color and bilateral structural signs, and the study continues with the remaining signs on both arms. "
            "The study does not cover autonomous publishing; generated faces stay as unapproved previews until faculty approve them and "
            "attach them to a scenario."
        )

        self.add_major_heading("References")
        ch1_refs = [
            "Alibudbud, R. (2023). Addressing the burnout and shortage of nurses in the Philippines. *SAGE Open Nursing*, *9*, 23779608231195737. https://doi.org/10.1177/23779608231195737",
            "American Association of Colleges of Nursing. (2025). *Nursing faculty shortage fact sheet*. https://www.aacnnursing.org/news-data/fact-sheets/nursing-faculty-shortage",
            "Bambini, D. (2016). Writing a simulation scenario: A step-by-step guide. *AACN Advanced Critical Care*, *27*(1), 62–70. https://doi.org/10.4037/aacnacc2016986",
            "Commission on Higher Education. (2017). *Policies, standards and guidelines for the Bachelor of Science in Nursing (BSN) program* (CMO No. 15, s. 2017). https://ched.gov.ph/wp-content/uploads/2017/10/CMO-15-s-2017.pdf",
            "Fan, B. E., Chow, M., & Winkler, S. (2023). Artificial intelligence-generated facial images for medical education. *Medical Science Educator*, *34*, 5–7. https://doi.org/10.1007/s40670-023-01942-5",
            "Haider, S. A., Shaikh, M. A., Shahid, H., & Haider, A. (2025). A validity analysis of text-to-image generative artificial intelligence models for craniofacial anatomy illustration. *Journal of Clinical Medicine*, *14*(7), 2136. https://doi.org/10.3390/jcm14072136",
            "Harder, N. (2023). Using ChatGPT in simulation design: What can (or should) it do for you? *Clinical Simulation in Nursing*, *78*, A1–A2. https://doi.org/10.1016/j.ecns.2023.02.011",
            "Jeffries, P. R. (Ed.). (2012). *Simulation in nursing education: From conceptualization to evaluation* (2nd ed.). National League for Nursing.",
            "Joerg, L., Kabakova, M., Wang, J. Y., Austin, E., Cohen, M., Kurtti, A., & Jagdeo, J. (2025). AI-generated dermatologic images show deficient skin tone diversity and poor diagnostic accuracy: An experimental study. *Journal of the European Academy of Dermatology and Venereology*, *39*(12), 2134–2141. https://doi.org/10.1111/jdv.20849",
            "Jong, S., Dihan, Q. A., Khodeiry, M. M., Alzein, A., Scelfo, C., & Elhusseiny, A. M. (2025). Evaluating text-to-image generation in pediatric ophthalmology. *Journal of Pediatric Ophthalmology & Strabismus*. Advance online publication. https://doi.org/10.3928/01913913-20250724-03",
            "Kumar, A., Burr, P., & Young, T. M. (2024). Using AI text-to-image generation to create novel illustrations for medical education: Current limitations as illustrated by hypothyroidism and Horner syndrome. *JMIR Medical Education*, *10*, e52155. https://doi.org/10.2196/52155",
            "Noblezada, J. E., Guanzon, R., Sobrevilla, A. R. J., Patigayon, J. R., Guzon, M. A., Venus, R., Rico, A., & Dumdum, M. M. (2025). Workload of clinical instructors in a highly urbanized city. *Aloysian Interdisciplinary Journal of Social Sciences, Education, and Allied Fields*, *1*(10), 1–17. https://doi.org/10.5281/zenodo.17339785",
            "O'Malley, A. S., Veenhuizen, M. A., & Ahmed, A. (2024). Ensuring appropriate representation in artificial intelligence–generated medical imagery: Protocol for a methodological approach to address skin tone bias. *JMIR AI*, *3*, e58275. https://doi.org/10.2196/58275",
            "Vaughn, J., & Ford, S. H. (2024). Enhancing healthcare education: Leveraging ChatGPT for innovative simulation scenarios. *Clinical Simulation in Nursing*, *89*, 101559. https://doi.org/10.1016/j.ecns.2024.101559",
            "Watts, P. I., McDermott, D. S., Alinier, G., Charnetski, M., Ludlow, J., Horsley, E., Meakim, C., & Nawathe, P. A. (2021). Healthcare Simulation Standards of Best Practice: Simulation design. *Clinical Simulation in Nursing*, *58*, 14–21. https://doi.org/10.1016/j.ecns.2021.08.009"
        ]
        for ref in ch1_refs:
            self.add_reference_entry(ref)

    def build_chapter_2(self):
        self.doc.add_page_break()
        self.add_chapter_title("2", "Review of Related Literature and Studies")
        
        self.add_body_paragraph(
            "This chapter reviews the research behind generative AI for image synthesis, the documented failure of these models "
            "on clinical facial signs, and what the literature says about skin-tone bias and visual fidelity in simulation. It follows "
            "the problem from Chapter 1: students cannot see the patient described in a nursing scenario, and the models that could "
            "generate a face fail on the signs that matter most. The chapter covers generative AI foundations for image synthesis, "
            "visual failure in generated clinical images, the use of AI-generated imagery in nursing and medical education, parametric "
            "three-dimensional face modeling, VLM-based evaluation of generated images, and ethics and data privacy. It then identifies "
            "the gaps, synthesizes the reviewed material, and presents the theoretical framework."
        )

        self.add_major_heading("Related Literature")
        
        self.add_subcomponent("Generative AI and image synthesis")
        self.add_body_paragraph(
            "The class of AI systems relevant to this study does not work with text alone. It generates images from text descriptions "
            "by learning to move data through a noise process and reverse it. Rombach et al. (2022) introduced latent diffusion models, "
            "which compress an image into a lower-dimensional space before applying the diffusion process. Running the denoiser in "
            "latent space made generation practical on consumer hardware and became the basis for Stable Diffusion. The same year, "
            "Ramesh et al. (2022) released DALL-E 2, which conditions a diffusion model on a CLIP image embedding derived from the text "
            "prompt. Saharia et al. (2022) introduced Imagen, which conditions a cascaded diffusion model directly on a large language "
            "model's text embeddings and achieved strong prompt-following on general images. Betker et al. (2023) built DALL-E 3 on top "
            "of a recaptioning step: every training image was redescribed with a detailed caption, and the resulting model followed "
            "long, specific prompts far better than its predecessors."
        )
        self.add_body_paragraph(
            "These models work by learning which image features correlate with which text tokens across billions of examples. That "
            "training objective produces images that are statistically plausible given the prompt, not images that enforce specific "
            "structural constraints. When a prompt describes a condition with a single, globally probable visual pattern, such as a "
            "reddened face or a puffy eye, the model can reproduce it. When the condition requires a precise local change on one side of "
            "the face, or requires two signs to appear together at the right spatial relationship, the model can fail because neither "
            "constraint appears explicitly in the generation process."
        )
        self.add_body_paragraph(
            "For this study, the diffusion arm (Arm A) uses a commercial image API that supports iterative editing: a correction loop "
            "where a verifier identifies missing traits and the model edits the same image to add them. Qwen-Image-Edit (2025) and FLUX.1 "
            "Kontext demonstrate that chained editing corrects errors step by step in ways that single-shot generation cannot, because "
            "each edit starts from a near-correct image rather than from noise. Brooks et al. (2023) formalized this pattern with "
            "InstructPix2Pix, showing that text-conditioned image editing can reliably add or remove attributes without destroying the "
            "rest of the image. The agentic editing loop in this study follows the same principle: generate, check, edit locally, check again."
        )

        self.add_subcomponent("Visual failure in AI-generated clinical images")
        self.add_body_paragraph(
            "The strongest evidence for the problem this study addresses comes from studies that tested modern text-to-image tools on "
            "clinical signs and measured the results."
        )
        self.add_body_paragraph(
            "Kumar et al. (2024) evaluated DALL-E 2 and Midjourney on medical education illustrations for two conditions. Hypothyroidism, "
            "whose signs are symmetric and generalized (facial puffiness, periorbital edema, and coarse features), was handled relatively "
            "well. Horner syndrome, which requires unilateral ptosis and anisocoria on one side of the face, was not. Both models produced "
            "symmetry-biased or anatomically distorted output across all tested generations, even with refined prompts. The paper's central "
            "finding is the asymmetry problem: models trained to produce the most statistically likely facial configuration cannot "
            "reliably break that symmetry for conditions that require it."
        )
        self.add_body_paragraph(
            "Fan et al. (2023) generated AI images of clinical facial pathology for use in medical education and found the approach "
            "promising for privacy-safe image sourcing. They also warned that the images require expert review before formal curriculum "
            "use, because anatomical inaccuracies that are invisible to a non-clinician can be apparent to one."
        )
        self.add_body_paragraph(
            "Haider et al. (2025) evaluated four models (Midjourney v6.0, DALL-E 3, Gemini Ultra 1.0, and Stable Diffusion 2.0) on "
            "craniofacial anatomy illustration. Expert reviewers showed high agreement on which errors were present (overall ICC = "
            "0.858), and every tested model produced critical structural flaws: missing foramina, incorrect suture lines, and "
            "misconfigured neurovascular pathways. The ICC result validates the kind of expert checklist approach this study uses, "
            "because clinicians reliably agree on what is wrong even when the image looks acceptable to a layperson."
        )
        self.add_body_paragraph(
            "Taken together, these three studies establish the failure pattern: diffusion models can produce images that look like faces "
            "and that contain generic clinical features, but they cannot be trusted to render a specific sign accurately without a "
            "verification step and without some mechanism that controls exactly which features appear where."
        )

        self.add_subcomponent("Skin-tone bias in AI-generated medical images")
        self.add_body_paragraph(
            "A parallel failure affects who the generated patients look like. Joerg et al. (2025) analyzed 4,000 dermatology images "
            "generated by four tools: ChatGPT-4o, Midjourney, Stable Diffusion, and Adobe Firefly. Across the first three platforms, 89.8 "
            "percent of images depicted light skin tones. When blinded dermatology residents assessed the same images for clinical "
            "accuracy, only 15 percent were correctly identified as depicting the intended skin condition. Firefly was the exception, "
            "matching U.S. Census skin-tone demographics more closely."
        )
        self.add_body_paragraph(
            "O'Malley et al. (2024) tested DALL-E 3 and Midjourney with standard prompts on psoriasis imagery. Both produced a distribution "
            "significantly skewed toward lighter skin tones (P < .001 against expected population demographics). A custom model with a "
            "structured demographic injection prompt corrected the distribution substantially (P = .04 for the adjusted output against "
            "population expectations). The correction required deliberate prompt engineering and did not occur with standard prompts."
        )
        self.add_body_paragraph(
            "These results matter for this study in two ways. First, they add a measurement axis: skin-tone fidelity is not a secondary "
            "concern but a documented failure mode of diffusion models that affects whether the generated patient represents the actual "
            "diversity of patients a Filipino nursing student will encounter. Second, the parametric 3D arm sidesteps this failure by "
            "construction. Skin tone in the FLAME model is a region parameter, not an emergent property of the generation process, so "
            "it can be set exactly and verified exactly. The diffusion arm requires the explicit demographic injection O'Malley et al. demonstrated."
        )

        self.add_subcomponent("Generative AI in nursing and medical education")
        self.add_body_paragraph(
            "The studies above address whether AI can render a face correctly. A separate body of work addresses whether AI-generated content helps learners."
        )
        self.add_body_paragraph(
            "Harder (2023) reported that ChatGPT can draft simulation scenarios quickly but that every draft still needs expert review. "
            "Vaughn and Ford (2024) put that claim to a test: five AI-written simulation scenarios went to 18 expert reviewers, who found "
            "missing information in every case. Liu et al. (2025) interviewed 13 ICU simulation instructors who used AI for case design; "
            "they reported time savings and help for beginners, but also said the content required checking before use. Reed and Dodson "
            "(2024) found a different but related result: AI-generated patient backstories, reviewed before use, lowered student anxiety "
            "and improved pre-simulation familiarity with the patient."
        )
        self.add_body_paragraph(
            "The common thread is that AI-generated clinical content is useful when it is reviewed and when it reduces some friction in "
            "the teaching workflow. This study takes the same position for images: a generated patient face is not a substitute for "
            "faculty clinical judgment, but it closes the gap between a written description and something a student can see."
        )

        self.add_subcomponent("Parametric 3D face models")
        self.add_body_paragraph(
            "The parametric 3D arm of this study uses FLAME (Faces Learned with an Articulated Model and Expressions), developed by "
            "Li et al. (2017) and updated to FLAME 2023 Open (CC-BY-4.0). FLAME represents a face as a linear combination of shape "
            "basis vectors, expression blendshapes, and pose parameters learned from thousands of registered 3D scans. Given any parameter "
            "vector, the model produces a deterministic mesh. That determinism is the theoretical advantage of the parametric arm: a "
            "color sign is a per-region albedo parameter that cannot drift between renders, and a bilateral structural sign is a "
            "blendshape weight set to a specific value."
        )
        self.add_body_paragraph(
            "Feng et al. (2021) showed with DECA that a FLAME model can be fit to a single photograph with high accuracy, validating "
            "that the FLAME parameter space covers enough of human facial variation to be clinically meaningful. The present study moves "
            "in the opposite direction: it starts from a text-described schema and sets FLAME parameters to express that schema, rather "
            "than fitting the model to an observed face."
        )
        self.add_body_paragraph(
            "Existing text-to-3D work shows both the potential and the limits of this direction. Rowan et al. (2023) proposed Text2Face, "
            "which derives FLAME shape parameters from text via CLIP embeddings and textures the result using DALL-E outputs. Because the "
            "texture is diffusion-generated, color signs in Text2Face are unreliable by the same mechanism described above: the texture "
            "is statistically plausible, not clinically controlled. This study separates the shape and color concerns. Shape and "
            "expression come from FLAME parameters; color signs are per-region material parameters applied to the texture map "
            "deterministically, so no diffusion process is involved in rendering a skin-tone tint or a jaundice region."
        )
        self.add_body_paragraph(
            "Score distillation approaches such as DreamFusion (Poole et al., 2022) and Magic3D (Lin et al., 2023) generate 3D objects "
            "from text by optimizing a mesh until a diffusion model would find it likely. HeadSculpt (Han et al., 2023) applied this to "
            "text-to-head generation. These methods are relevant as prior art but not as a practical path for this study: they require "
            "GPU-intensive optimization per output, the result is still diffusion-scored and cannot guarantee a specific sign is present, "
            "and the code for HeadSculpt was never released publicly. The parametric approach trades photorealism for determinism, and "
            "Dr. Evan explicitly accepted stylized output."
        )

        self.add_subcomponent("VLM-based evaluation of generated images")
        self.add_body_paragraph(
            "The pipeline in this study includes an automated verification step: a vision-language model (VLM) checks each generated face "
            "against a per-trait checklist and reports which signs are present, missing, or fabricated. This step is not self-validating. "
            "Hayes et al. (2025) benchmarked VLM judges on prompt-adherence in text-to-image generation (FineGRAIN) and found that "
            "VLM-human agreement was approximately 67 percent, with models failing on specific attribute categories. The result means that "
            "a VLM score is a useful screen, not a ground truth. This study treats the VLM verifier accordingly: it runs first to catch "
            "obvious failures, but it does not replace the clinician-authored checklist and faculty approval gate. The study also measures "
            "VLM-versus-clinician agreement with Cohen's kappa as part of the experimental data, so the verifier's reliability is a "
            "result of the study, not an assumption going into it."
        )

        self.add_subcomponent("Ethics and data privacy")
        self.add_body_paragraph(
            "Generating synthetic patient faces raises questions that real patient photographs do not, and some that they do."
        )
        self.add_body_paragraph(
            "In the Philippines, the Data Privacy Act of 2012 (Republic Act No. 10173) protects personal data, and health data receives "
            "the highest level of protection. This study avoids the patient-data problem at the source: no real patient photographs are "
            "used at any stage. The inputs are faculty-authored scenario descriptions; the outputs are synthetic faces generated from "
            "those descriptions."
        )
        self.add_body_paragraph(
            "The ethical concern specific to synthetic face generation is identity resemblance. A diffusion model trained on real "
            "photographs can produce outputs that resemble specific real individuals, even without intending to. Tian et al. (2025) "
            "built MeMa, a dataset of 42,307 synthetic faces depicting medical manifestations, and found that vanilla Stable Diffusion "
            "outputs had a 71.8 percent identity-matching rate against the real training photos. They reduced this to 1.27 percent by "
            "adding an identity-disentanglement step. This study mitigates the same risk through its parametric arm, as FLAME meshes have "
            "no memory of real individuals, and through the diffusion arm's use of a commercial API whose provider (Google/Gemini) applies "
            "SynthID watermarking for provenance tracking. Every generated face is labeled AI-generated before it attaches to a scenario, "
            "and a hard faculty approval gate sits between generation and student-facing use."
        )
        self.add_body_paragraph(
            "Licensing is also a practical ethics concern. FLUX.1 Kontext [dev] carries a non-commercial license from Black Forest Labs. "
            "Qwen-Image-Edit (Alibaba, 2025) is released under Apache 2.0. FLAME 2023 Open is CC-BY-4.0. The Gemini image API is a "
            "commercial service. This study uses the Gemini API as the primary diffusion provider, which is the only option available "
            "without a GPU and without incurring a non-commercial license constraint for a school deployment."
        )

        self.add_major_heading("Related Studies")
        self.add_body_paragraph(
            "The studies reviewed above are grouped by the specific empirical claims they support in this research:"
        )
        self.add_body_paragraph(
            "AI-generated images fail on clinical facial signs. Kumar et al. (2024) provide the strongest evidence: hypothyroidism "
            "signs rendered acceptably, Horner syndrome did not, and the failure traced directly to the asymmetric nature of the sign. "
            "Haider et al. (2025) extended this finding to craniofacial anatomy across four models and validated the expert checklist "
            "approach with a high ICC. Fan et al. (2023) confirmed the educational relevance while flagging the expert-review requirement."
        )
        self.add_body_paragraph(
            "Skin-tone bias is measurable and partially correctable. Joerg et al. (2025) quantified the scale of the problem (89.8 "
            "percent light skin, 15 percent diagnostic accuracy) across four current platforms. O'Malley et al. (2024) showed that a "
            "structured demographic prompt can substantially correct the distribution, validating the explicit skin-tone injection used "
            "in the diffusion arm of this study."
        )
        self.add_body_paragraph(
            "Synthetic patient data at scale requires ethics infrastructure this study does not yet have. Tian et al. (2025) showed that "
            "producing a clinical face dataset large enough to train a model required 39,323 real patient photographs and a full hospital "
            "ethics approval process. This directly justifies the study's API-first, no-training approach. The approved images this "
            "study accumulates become the future training corpus, not the current one."
        )
        self.add_body_paragraph(
            "Parametric face models can represent clinical variation deterministically. Li et al. (2017) and Feng et al. (2021) "
            "established that FLAME covers enough human facial variation to be meaningful for reconstruction and generation. Rowan et al. "
            "(2023) showed one path from text to FLAME parameters, but also showed the color limitation when texture is diffusion-generated. "
            "This study extends that work by controlling the color layer separately."
        )
        self.add_body_paragraph(
            "VLM judges are useful but not self-validating. Hayes et al. (2025) provide the only published measurement of VLM-human "
            "agreement on fine-grained image attributes in a prompt-adherence setting. The approximately 67 percent agreement rate sets "
            "the expectation for the verifier and justifies measuring kappa in this study."
        )
        self.add_body_paragraph(
            "AI-generated content aids education when reviewed. Reed and Dodson (2024) found that reviewed AI backstories improved student "
            "preparation. Harder (2023), Vaughn and Ford (2024), and Liu et al. (2025) collectively established that AI content production "
            "in simulation saves time while requiring expert checking. Together these studies position the present work as consistent with "
            "accepted practice: the pipeline produces a draft visual, not a final educational asset."
        )

        self.add_major_heading("Gaps in the Literature")
        self.add_body_paragraph(
            "Three specific gaps remain after reviewing the studies above:"
        )
        self.add_numbered_item("1", "Absence of Modality Comparison:", "No study has compared rendering modalities for clinical facial signs. The literature compares different text-to-image models on the same output type, but nothing compares a diffusion-generated photograph against a parametric 3D render of the same clinical description, under the same pipeline, with the same evaluation criteria. That comparison is the study's central experiment.")
        self.add_numbered_item("2", "Lack of Nursing Faculty Validation in HIS:", "No study has measured the ability of either rendering approach to reproduce clinical facial signs in a nursing simulation context with nursing faculty as raters. The existing evaluations use dermatologists, ophthalmologists, or anatomy educators. A nursing faculty rater asks a different question: is this face useful for teaching clinical assessment?")
        self.add_numbered_item("3", "Omission of Skin-Tone Fidelity in Simulation:", "Skin-tone fidelity has not been measured as an axis in nursing simulation face generation. The bias literature focuses on dermatology and general medical images. No study has asked how well either modality renders a patient face at a specified skin tone for educational use in a country with a diverse patient population.")
        self.add_body_paragraph(
            "These three gaps define the study's contribution: a controlled modality comparison, with nursing faculty raters, that includes "
            "skin-tone fidelity as a measured outcome, inside a working school hospital information system."
        )

        self.add_major_heading("Synthesis of the Reviewed Literature and Studies")
        self.add_body_paragraph(
            "Diffusion models can generate high-quality faces, but they cannot be trusted to render specific clinical signs without "
            "verification. The asymmetry problem (Kumar et al., 2024), the structural-accuracy problem (Haider et al., 2025), and the "
            "skin-tone bias problem (Joerg et al., 2025; O'Malley et al., 2024) all point to the same root: a model trained to produce "
            "statistically likely images has no built-in mechanism to enforce a precise local clinical constraint. The agentic editing "
            "loop addresses the first problem by correcting errors after detection. The parametric 3D arm addresses all three by "
            "construction: sign fidelity and skin tone are parameters, not emergent properties."
        )
        self.add_body_paragraph(
            "The educational evidence (Harder, 2023; Vaughn & Ford, 2024; Liu et al., 2025; Reed & Dodson, 2024) supports the role of "
            "AI-generated content in simulation when it is reviewed, and the ethics literature (Tian et al., 2025; O'Malley et al., 2024) "
            "shows that synthetic faces carry real identity and bias risks that require deliberate mitigation. The VLM evaluation "
            "literature (Hayes et al., 2025) constrains how much the automated verifier can be trusted."
        )
        self.add_body_paragraph(
            "Taken together, the literature supports building an agentic generation pipeline that separates the two rendering approaches, "
            "verifies both, and routes outputs through faculty approval. It also establishes that the comparison has not been run and "
            "that the three outcomes this study measures (per-trait fidelity, faculty-rated plausibility, and skin-tone fidelity) are the right ones."
        )

        self.add_major_heading("Theoretical Framework")
        self.add_body_paragraph(
            "Three complementary theoretical frameworks explain why the pipeline is designed the way it is and define what success means in this investigation:"
        )

        self.add_subcomponent("Simulation fidelity theory")
        self.add_body_paragraph(
            "The NLN Jeffries Simulation Theory (Jeffries, 2012) holds that effective simulations require fidelity: objectives, realism, "
            "and clinical accuracy must align so that students learn the right pattern. Jeffries, Rodgers, and Adamson (2015) clarified "
            "that fidelity is not a single dimension but a set of aligned properties. Watts et al. (2021) operationalized this in the "
            "Healthcare Simulation Standards of Best Practice, which require that designers use various types of fidelity to create the "
            "required perception of realism, calibrated to learner level and objective."
        )
        self.add_body_paragraph(
            "A generated patient face is a fidelity artifact. When it shows the right signs, it raises the physical fidelity of the "
            "scenario without requiring real patient photographs or expensive moulage. When it shows wrong signs, it breaks fidelity as "
            "directly as a hallucinated vital sign does. Jeffries simulation theory is the central framework because it defines what "
            "success means: not photorealism, but sign fidelity and teaching usefulness, which is precisely what this study measures."
        )

        self.add_subcomponent("Cognitive load theory")
        self.add_body_paragraph(
            "Cognitive load theory (Sweller, 1988) distinguishes three types of mental demand: the load from the material itself, the "
            "load from poorly designed tools or presentation, and the load from the work of forming understanding. Good instructional "
            "design eliminates the second type so learners can direct working memory toward the third."
        )
        self.add_body_paragraph(
            "Students who read a scenario without a visual must imagine the patient. When the sign they must imagine is one they have "
            "never seen (such as ptosis, cyanosis, or Cushing facies), that imagination is effortful and likely inaccurate, adding "
            "extraneous load before the clinical reasoning begins. A generated face that shows the correct signs removes that imagining "
            "step. The learning task becomes interpreting a sign that is visible, not constructing one from text, and working memory is "
            "freed for the clinical reasoning the scenario is designed to teach. Cognitive load theory explains why a visual, even a "
            "stylized parametric one, is not a decorative addition to a scenario but a reduction in the cognitive demand placed on a "
            "student before the simulation begins."
        )

        self.add_subcomponent("Multimedia learning and picture superiority")
        self.add_body_paragraph(
            "Mayer's (2001) cognitive theory of multimedia learning holds that people learn more deeply from words and pictures together "
            "than from words alone. The picture superiority effect, documented across decades of memory research, shows that images are "
            "encoded and retrieved more reliably than verbal descriptions of the same information. For physical signs, this means that a "
            "student who has seen a face with jaundice will recognize jaundice in clinic more reliably than a student who has only read a definition."
        )
        self.add_body_paragraph(
            "Applied to this study, the theory predicts that adding a generated patient face to a scenario text is not neutral: it should "
            "improve students' ability to recognize the described signs in real patients, provided the face is clinically accurate. That "
            "prediction is not tested in this study, because testing it would require a separate learning outcomes study, but it motivates "
            "the project. The theoretical claim is that if the generated face is correct, the educational benefit follows from established learning theory."
        )

        self.add_subcomponent("Application in the study")
        self.add_body_paragraph(
            "The three theories map to the three primary metrics. Simulation fidelity theory defines what the face must achieve and sets "
            "the standard for faculty evaluation (trait accuracy and teaching usefulness). Cognitive load theory explains why that "
            "achievement matters for the student (reduced extraneous load at the start of simulation). Multimedia learning theory grounds "
            "the whole project in what is known about how visual information supports clinical learning. Together they establish that the "
            "study is not a technology demonstration but a test of an instructional design decision: whether generated faces meet the "
            "fidelity standard that makes them worth the reduced cognitive burden they create."
        )

        self.add_major_heading("References")
        ch2_refs = [
            "Betker, J., Goh, G., Jing, L., Brooks, T., Wang, J., Li, L., Ouyang, L., Zhuang, J., Lee, J., Guo, Y., Manber, R., Xu, R., Zheng, G., Zhang, W., Ogut, O., Mishkin, P., & Chen, M. (2023). *Improving image generation with better captions* [Technical report]. OpenAI. https://cdn.openai.com/papers/dall-e-3.pdf",
            "Brooks, T., Holynski, A., & Efros, A. A. (2023). InstructPix2Pix: Learning to follow image editing instructions. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2023)*, 18392–18402. https://doi.org/10.48550/arXiv.2211.09800",
            "Commission on Higher Education. (2017). *Policies, standards and guidelines for the Bachelor of Science in Nursing (BSN) program* (CMO No. 15, s. 2017). https://ched.gov.ph/wp-content/uploads/2017/10/CMO-15-s-2017.pdf",
            "Fan, B. E., Chow, M., & Winkler, S. (2023). Artificial intelligence-generated facial images for medical education. *Medical Science Educator*, *34*, 5–7. https://doi.org/10.1007/s40670-023-01942-5",
            "Feng, Y., Feng, H., Black, M. J., & Bolkart, T. (2021). Learning an animatable detailed 3D face model from in-the-wild images. *ACM Transactions on Graphics*, *40*(4), Article 88. https://doi.org/10.1145/3450626.3459936",
            "Haider, S. A., Shaikh, M. A., Shahid, H., & Haider, A. (2025). A validity analysis of text-to-image generative artificial intelligence models for craniofacial anatomy illustration. *Journal of Clinical Medicine*, *14*(7), 2136. https://doi.org/10.3390/jcm14072136",
            "Han, X., Cao, Y., Han, K., Zhu, X., Deng, J., Song, Y.-Z., Xiang, T., & Wong, K.-Y. K. (2023). HeadSculpt: Crafting 3D head avatars with text. In *Advances in Neural Information Processing Systems*, *36*, 37213–37226. https://doi.org/10.48550/arXiv.2306.03038",
            "Harder, N. (2023). Using ChatGPT in simulation design: What can (or should) it do for you? *Clinical Simulation in Nursing*, *78*, A1–A2. https://doi.org/10.1016/j.ecns.2023.02.011",
            "Hayes, K., Goldblum, M., Sehwag, V., Somepalli, G., Panda, A., & Goldstein, T. (2025). FineGRAIN: Evaluating failure modes of text-to-image models with vision language model judges. *Advances in Neural Information Processing Systems*, *38*. https://doi.org/10.48550/arXiv.2512.02161",
            "Jeffries, P. R. (Ed.). (2012). *Simulation in nursing education: From conceptualization to evaluation* (2nd ed.). National League for Nursing.",
            "Jeffries, P. R., Rodgers, B., & Adamson, K. (2015). NLN Jeffries simulation theory: Brief narrative description. *Nursing Education Perspectives*, *36*(5), 292–293. https://doi.org/10.5480/1536-5026-36.5.292",
            "Joerg, L., Kabakova, M., Wang, J. Y., Austin, E., Cohen, M., Kurtti, A., & Jagdeo, J. (2025). AI-generated dermatologic images show deficient skin tone diversity and poor diagnostic accuracy: An experimental study. *Journal of the European Academy of Dermatology and Venereology*, *39*(12), 2134–2141. https://doi.org/10.1111/jdv.20849",
            "Kumar, A., Burr, P., & Young, T. M. (2024). Using AI text-to-image generation to create novel illustrations for medical education: Current limitations as illustrated by hypothyroidism and Horner syndrome. *JMIR Medical Education*, *10*, e52155. https://doi.org/10.2196/52155",
            "Li, T., Bolkart, T., Black, M. J., Li, H., & Romero, J. (2017). Learning a model of facial shape and expression from 4D scans. *ACM Transactions on Graphics*, *36*(6), Article 194. https://doi.org/10.1145/3130800.3130813",
            "Lin, C.-H., Gao, J., Tang, L., Takikawa, T., Zeng, X., Huang, X., Kreis, K., Fidler, S., Liu, M.-Y., & Lin, T.-Y. (2023). Magic3D: High-resolution text-to-3D content creation. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2023)*, 300–309. https://doi.org/10.48550/arXiv.2211.10440",
            "Liu, J., Wang, L., He, X., Xia, Y., Gong, X., Wu, R., Li, S., & Wu, L. (2025). Leveraging generative artificial intelligence to enhance ICU novice simulation instructors' case design: A qualitative study. *Clinical Simulation in Nursing*, Article 101770. https://doi.org/10.1016/j.ecns.2025.101770",
            "Mayer, R. E. (2001). *Multimedia learning*. Cambridge University Press.",
            "O'Malley, A. S., Veenhuizen, M. A., & Ahmed, A. (2024). Ensuring appropriate representation in artificial intelligence–generated medical imagery: Protocol for a methodological approach to address skin tone bias. *JMIR AI*, *3*, e58275. https://doi.org/10.2196/58275",
            "Poole, B., Jain, A., Barron, J. T., & Mildenhall, B. (2022). DreamFusion: Text-to-3D using 2D diffusion. *arXiv preprint arXiv:2209.14988*. https://doi.org/10.48550/arXiv.2209.14988",
            "Ramesh, A., Dhariwal, P., Nichol, A., Chu, C., & Chen, M. (2022). *Hierarchical text-conditional image generation with CLIP latents* [Technical report]. OpenAI. https://doi.org/10.48550/arXiv.2204.06125",
            "Reed, J. M., & Dodson, T. M. (2024). Generative AI backstories for simulation preparation. *Nurse Educator*, *49*(4), 184–188. https://doi.org/10.1097/NNE.0000000000001590",
            "Rombach, R., Blattmann, A., Lorenz, D., Esser, P., & Ommer, B. (2022). High-resolution image synthesis with latent diffusion models. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2022)*, 10684–10695. https://doi.org/10.48550/arXiv.2112.10752",
            "Rowan, W., Huber, P., Pears, N., & Keeling, A. (2023). Text2Face: A multi-modal 3D face model. *arXiv preprint arXiv:2303.02688*. https://doi.org/10.48550/arXiv.2303.02688",
            "Saharia, C., Chan, W., Saxena, S., Li, L., Whang, J., Denton, E., Ghasemipour, S. K. S., Gontijo-Lopes, R., Karagol-Ayan, B., Salimans, T., Ho, J., Fleet, D. J., & Norouzi, M. (2022). Photorealistic text-to-image diffusion models with deep language understanding. *Advances in Neural Information Processing Systems*, *35*, 36479–36494. https://doi.org/10.48550/arXiv.2205.11487",
            "Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, *12*(2), 257–285. https://doi.org/10.1207/s15516709cog1202_4",
            "Tian, Y., Wang, S., & Zhai, G. (2025). Medical manifestation-aware de-identification. In *Proceedings of the AAAI Conference on Artificial Intelligence*, *39*. https://doi.org/10.48550/arXiv.2412.10804",
            "Vaughn, J., & Ford, S. H. (2024). Enhancing healthcare education: Leveraging ChatGPT for innovative simulation scenarios. *Clinical Simulation in Nursing*, *89*, 101559. https://doi.org/10.1016/j.ecns.2024.101559",
            "Watts, P. I., McDermott, D. S., Alinier, G., Charnetski, M., Ludlow, J., Horsley, E., Meakim, C., & Nawathe, P. A. (2021). Healthcare Simulation Standards of Best Practice: Simulation design. *Clinical Simulation in Nursing*, *58*, 14–21. https://doi.org/10.1016/j.ecns.2021.08.009"
        ]
        for ref in ch2_refs:
            self.add_reference_entry(ref)

    def build_chapter_3(self):
        self.doc.add_page_break()
        self.add_chapter_title("3", "Methodology")
        
        self.add_body_paragraph(
            "This study uses a comparative experimental research design combined with developmental software engineering to "
            "evaluate two patient-face rendering modalities: diffusion-generated images (Arm A) and a parametric three-dimensional head "
            "model (Arm B). Both modalities are implemented within the same educational hospital information system, Chansey, under a "
            "single constant agentic pipeline. This setup holds all upstream text parsing, sign expansion, and verification steps constant, "
            "ensuring that differences in trait fidelity, visual plausibility, skin-tone accuracy, and computing cost trace directly to "
            "the rendering modality itself."
        )
        self.add_body_paragraph(
            "The software development process follows the Rapid Application Development (RAD) model. RAD was chosen because it "
            "prioritizes working prototypes, short development cycles, and frequent feedback from the primary clinical stakeholder, "
            "Dr. Evan. In clinical simulation, visual realism is not an abstract aesthetic standard; it must align with what nursing "
            "instructors actually need to teach physical assessment. Short prototyping cycles allow the research team to build candidate "
            "outputs, demonstrate them to nursing faculty, and refine trait parameters, color tints, and severity mappings based on direct "
            "clinical input before running the formal evaluation."
        )
        self.add_body_paragraph(
            "The system development couples a web-based clinical information system built with Laravel with a dedicated Python "
            "microservice that handles language model parsing, API-based diffusion rendering, parametric mesh deformation, and vision-language "
            "model verification."
        )

        self.add_major_heading("Software Development Life Cycle (SDLC) Model")
        self.add_body_paragraph(
            "The project follows the four distinct phases of the Rapid Application Development (RAD) model: Requirements Planning and "
            "Quick Design, Prototype Cycles (Build, Demonstrate, and Refine), Testing, and Implementation."
        )
        self.add_figure("Figure 3.1", "Rapid Application Development (RAD) Model")

        self.add_subcomponent("1. Requirements Planning and Quick Design")
        self.add_body_paragraph(
            "The development began by defining the functional and clinical requirements for patient visualization in Chansey. During this "
            "phase, the researchers identified that nursing faculty authoring scenarios need an automated way to generate patient faces "
            "without sourcing real patient photographs. The data structures for the trait schema and sign catalog were outlined, establishing "
            "the common ground needed between clinical text and rendering parameters."
        )

        self.add_subcomponent("2. Prototype Cycles (Build, Demonstrate, Refine)")
        self.add_body_paragraph(
            "The prototype cycle operated as a repeated sequence of three steps:"
        )
        self.add_bullet_item("Build", "The initial versions of the trait schema, the FastAPI microservice, the diffusion prompt compiler, and the FLAME 3D geometry pipeline were created. Integration hooks were added to Chansey's scenario builder interface.")
        self.add_bullet_item("Demonstrate", "Candidate rendered faces across representative conditions (such as jaundice, ptosis, and cyanosis) were presented to Dr. Evan and nursing faculty. Stakeholders evaluated whether the visual signs matched clinical expectations.")
        self.add_bullet_item("Refine", "Faculty feedback was used to adjust color hex palettes, severity thresholds, and blendshape weights. For instance, color tints for jaundice were adjusted to prevent unnatural yellow hues on darker skin presentations. This cycle repeated until the output reached acceptable clinical plausibility.")

        self.add_subcomponent("3. Testing Phase")
        self.add_body_paragraph(
            "Once the prototype stabilized, the system entered formal testing. This phase encompassed two parts: automated technical "
            "verification of prompt adherence and latency, followed by the formal experimental evaluation where nursing faculty rated 24 "
            "to 30 stimulus scenarios across both modalities."
        )

        self.add_subcomponent("4. Implementation Phase")
        self.add_body_paragraph(
            "The validated pipeline was deployed into the Chansey web platform. In this final phase, the scenario authoring interface "
            "allows instructors to generate, preview, and approve patient faces directly within their everyday workflow."
        )

        self.add_major_heading("System Development Tools")
        self.add_body_paragraph(
            "This section outlines the programming environments, frameworks, libraries, and database management systems used to build the platform."
        )

        self.add_subcomponent("Programming Languages and Frameworks")
        self.add_body_paragraph(
            "The system uses a decoupled client-server architecture:"
        )
        self.add_bullet_item("PHP 8.2+ and Laravel 12", "Serves as the primary web application framework for Chansey HIS. It manages user authentication, role-based access control, clinical ward records, scenario authoring workflows, and database transactions.")
        self.add_bullet_item("Python 3.11+ and FastAPI", "Powers the machine learning and computer vision microservice. FastAPI was chosen for its high asynchronous throughput and native support for Pydantic data validation schemas.")
        self.add_bullet_item("FLAME 2023 Open", "Serves as the three-dimensional parametric head model (CC-BY-4.0). It runs on CPU using standard linear algebra routines in NumPy and PyTorch, avoiding the need for dedicated local graphics hardware.")
        self.add_bullet_item("Gemini API (Google AI Studio)", "Powers the multimodal AI pipeline. Gemini Flash handles structured text parsing and disease expansion, Gemini Image API generates the diffusion PNGs and processes localized inpainting edits, and Gemini Vision operates as the automated VLM verifier.")
        self.add_bullet_item("JavaScript, Tailwind CSS, and Blade", "Handled client-side responsiveness, asynchronous preview loading, and interactive image comparisons in the browser.")

        self.add_subcomponent("Integrated Development Environment (IDE)")
        self.add_body_paragraph(
            "Visual Studio Code served as the primary development environment. It provided workspace management, Git version control, "
            "Python virtual environment isolation, and debugging tools for both PHP and Python services."
        )

        self.add_subcomponent("Database Management System")
        self.add_body_paragraph(
            "The platform utilizes PostgreSQL (with SQLite supported for lightweight automated testing). PostgreSQL manages relational "
            "integrity across patient admissions, scenario templates, trait schemas, and evaluation logs, using foreign keys to guarantee audit traceability."
        )

        self.add_major_heading("Experimental Stimuli and Evaluation Dataset")
        self.add_body_paragraph(
            "To evaluate the two rendering modalities without data leakage or bias toward a single disease, the study uses a "
            "pre-registered evaluation dataset of 24 to 30 clinical scenario descriptions."
        )
        self.add_body_paragraph(
            "The stimuli were structured to test specific clinical sign categories:"
        )
        self.add_numbered_item("1", "Color Signs (Systemic / Diffuse):", "Jaundice (scleral and cutaneous), pallor (conjunctival and facial), cyanosis (perioral), and facial flushing.")
        self.add_numbered_item("2", "Structural Symmetric Signs:", "Periorbital edema, facial puffiness, diaphoresis (sweating), and glassy eyes.")
        self.add_numbered_item("3", "Structural Asymmetric Signs:", "Unilateral ptosis, facial droop (cranial nerve VII palsy), and unilateral anisocoria.")
        self.add_numbered_item("4", "Secretions and Surface Manifestations:", "Rhinorrhea (runny nose) and tearing.")
        self.add_numbered_item("5", "Demographic Variations:", "Balanced distribution across male and female presentations and across all six Monk and Fitzpatrick skin-tone classifications.")
        self.add_numbered_item("6", "Input Types:", "A mix of explicit trait descriptions and disease-only inputs (such as \"acute viral hepatitis\" or \"Bell's palsy\") to evaluate the expander agent.")
        
        self.add_figure("Figure 3.2", "Sample Outputs from the Evaluation Stimulus Set")
        self.add_body_paragraph(
            "Each scenario description in the dataset was converted into a ground-truth checklist by a clinical educator, specifying "
            "the required traits, their anatomical regions, laterality, and severity levels."
        )

        self.add_major_heading("Algorithms and Modalities Applied")
        self.add_body_paragraph(
            "The research compares two fundamentally different image generation paradigms under identical operational conditions."
        )
        self.add_figure("Figure 3.3", "Comparison of Image Synthesis Pipelines")

        self.add_subcomponent("Arm A: Diffusion-Based Image Generation (Gemini Image API)")
        self.add_body_paragraph(
            "Arm A operates through text-to-image latent diffusion. The structured trait schema is compiled into an explicit clinical "
            "prompt that includes demographic markers, laterality constraints, and anatomical descriptions. To mitigate the default light-skin "
            "bias documented by Joerg et al. (2025), explicit Monk/Fitzpatrick descriptors are injected into the prompt based on the method "
            "verified by O'Malley et al. (2024)."
        )
        self.add_body_paragraph(
            "Because one-shot diffusion often omits fine-grained clinical details, Arm A incorporates an agentic correction loop. After "
            "initial generation, the image is passed to the VLM verifier. If a required trait is flagged as missing or an extra sign is "
            "detected, an automated localized inpainting instruction is submitted back to the model, allowing up to two correction cycles "
            "before final output."
        )

        self.add_subcomponent("Arm B: Parametric 3D Head Generation (FLAME 2023 Open)")
        self.add_body_paragraph(
            "Arm B uses an explicit mathematical model of human facial geometry. FLAME expresses facial shape and expression as linear "
            "combinations of basis vectors learned from registered 3D scans:"
        )
        self.add_displayed_equation("M(v, β, θ, ψ) = T̄ + B_s(β) + B_p(θ) + B_e(ψ)", "3.1")
        self.add_body_paragraph("Where:", indent=False)
        self.add_bullet_item("T̄", "is the base template mesh in resting pose.")
        self.add_bullet_item("B_s(β)", "represents shape displacements controlled by identity coefficients β.")
        self.add_bullet_item("B_p(θ)", "represents pose blendshapes controlled by joint rotations θ.")
        self.add_bullet_item("B_e(ψ)", "represents expression blendshapes controlled by expression parameters ψ.")
        self.add_body_paragraph(
            "In this study, color signs are not generated by diffusion texture maps. Instead, per-region albedo and tint parameters are "
            "applied directly to the anatomical UV regions of the mesh (such as sclera, lips, and cheek zones). Structural signs use target "
            "blendshapes: bilateral signs adjust standard expression vectors, while unilateral signs (such as left-sided ptosis) actuate "
            "localized unilateral blendshape weights. The deformed head is rendered offscreen into a standardized PNG profile."
        )

        self.add_subcomponent("Role of the Modalities in the System")
        self.add_body_paragraph(
            "Both renderers function as interchangeable backend modules. When the user initiates face generation, the microservice runs "
            "both arms concurrently or sequentially on the same parsed schema. The resulting previews are presented with their automated "
            "verification logs, allowing faculty to compare both outputs directly before selecting an approved asset."
        )

        self.add_major_heading("Methods of Evaluation")
        self.add_body_paragraph(
            "The evaluation combines automated objective metrics with clinical human ratings to answer all five research questions."
        )

        self.add_subcomponent("1. Quantitative Trait Fidelity Metrics")
        self.add_body_paragraph(
            "Each generated face is evaluated against the ground-truth checklist established for its scenario description. Predictions "
            "are categorized into:"
        )
        self.add_bullet_item("True Positive (TP)", "A required clinical trait is correctly depicted in the appropriate anatomical location and laterality.")
        self.add_bullet_item("False Positive (FP) / Hallucination", "A visual sign appears on the face that was neither requested nor clinically justified.")
        self.add_bullet_item("False Negative (FN)", "A requested clinical trait is completely missing or anatomically incorrect.")
        self.add_bullet_item("True Negative (TN)", "An unrequested sign is correctly absent from the face.")
        self.add_body_paragraph("Based on these classifications, the following standard metrics are computed:")
        self.add_displayed_equation("Accuracy = (TP + TN) / (TP + TN + FP + FN)", "3.2")
        self.add_displayed_equation("Precision = TP / (TP + FP)", "3.3")
        self.add_displayed_equation("Recall = TP / (TP + FN)", "3.4")
        self.add_displayed_equation("F1 Score = 2 × (Precision × Recall) / (Precision + Recall)", "3.5")
        self.add_body_paragraph(
            "Trait recall rate and the count of hallucinated extra signs serve as the primary measures of trait fidelity (RQ1)."
        )

        self.add_subcomponent("2. Skin-Tone Concordance")
        self.add_body_paragraph(
            "Skin-tone fidelity is assessed by comparing the intended Monk skin-tone level (Monk 1 to 10) against the observed skin tone "
            "in the output image. Concordance is evaluated on an exact-match and within-one-level tolerance basis to determine whether "
            "either modality exhibits systematic demographic drift (RQ3)."
        )

        self.add_subcomponent("3. Operational Performance Metrics")
        self.add_body_paragraph("The system logs technical metrics for every generation attempt:")
        self.add_bullet_item("Latency (ms)", "Total round-trip time from the initial request to the delivery of the rendered image.")
        self.add_bullet_item("Token and API Cost", "The count of input, output, and vision tokens consumed per generation attempt, along with the estimated monetary cost in US dollars (RQ4).")
        self.add_bullet_item("Hardware Footprint", "Memory usage and processor load during CPU-based 3D mesh rendering versus cloud API calls.")

        self.add_subcomponent("4. Faculty Rating (Clinical Plausibility and Teaching Usefulness)")
        self.add_body_paragraph(
            "To evaluate clinical plausibility and educational utility (RQ2), generated faces are evaluated by a panel of Nursing "
            "Department faculty, including Dr. Evan. Evaluators review the outputs in a blinded randomized order, rating each image on a "
            "5-point Likert scale across three core criteria:"
        )
        self.add_numbered_item("1", "Clinical Plausibility:", "Does the face present an anatomically believable appearance consistent with human pathology?")
        self.add_numbered_item("2", "Sign Fidelity:", "Are the described symptoms clear, identifiable, and localized correctly?")
        self.add_numbered_item("3", "Teaching Usefulness:", "Would this visual asset help nursing students recognize the condition during simulation?")
        
        self.add_body_paragraph("Responses are interpreted using standard weighted mean intervals as presented in Table 3.1:")

        # Table 3.1
        self.add_table_title("Table 3.1", "Five-Point Likert Scale Interpretation for Clinical Plausibility and Teaching Usefulness")
        tbl1 = self.doc.add_table(rows=6, cols=3)
        tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl1.autofit = False

        headers = ["Scale Value", "Statistical Range", "Qualitative Interpretation"]
        rows_data = [
            ["5", "4.21 – 5.00", "Strongly Agree / Highly Plausible"],
            ["4", "3.41 – 4.20", "Agree / Plausible"],
            ["3", "2.61 – 3.40", "Neutral / Moderately Plausible"],
            ["2", "1.81 – 2.60", "Disagree / Implausible"],
            ["1", "1.00 – 1.80", "Strongly Disagree / Completely Implausible"]
        ]

        col_widths = [Inches(1.5), Inches(2.0), Inches(2.5)]

        # Set headers
        for j, text in enumerate(headers):
            cell = tbl1.cell(0, j)
            cell.width = col_widths[j]
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.line_spacing = 1.0
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            r = p_c.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(10)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

        # Set rows
        for i, row in enumerate(rows_data):
            for j, val in enumerate(row):
                cell = tbl1.cell(i + 1, j)
                cell.width = col_widths[j]
                p_c = cell.paragraphs[0]
                p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if j < 2 else WD_ALIGN_PARAGRAPH.LEFT
                p_c.paragraph_format.line_spacing = 1.0
                p_c.paragraph_format.space_before = Pt(2)
                p_c.paragraph_format.space_after = Pt(2)
                r = p_c.add_run(val)
                r.font.name = 'Arial'
                r.font.size = Pt(10)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

        set_apa_table_borders(tbl1)

        self.add_body_paragraph("The weighted mean is calculated as:")
        self.add_displayed_equation("x̄ = ∑ (f × x) / N", "3.6")
        self.add_body_paragraph("Where:", indent=False)
        self.add_bullet_item("x̄", "= weighted mean")
        self.add_bullet_item("f", "= frequency of responses for a scale category")
        self.add_bullet_item("x", "= Likert scale numerical value (1 to 5)")
        self.add_bullet_item("N", "= total number of faculty evaluations")

        self.add_subcomponent("5. Statistical Significance Testing")
        self.add_body_paragraph(
            "To test whether observed differences between the two modalities are statistically significant (RQ3), the study uses inferential tests:"
        )
        self.add_bullet_item("McNemar’s Test", "Used for paired binary data (presence or absence of each specific trait across matched scenario pairs).")
        self.add_bullet_item("Wilcoxon Signed-Rank Test", "Used for paired non-parametric comparisons of faculty ratings (plausibility, fidelity, usefulness) across matched scenarios.")
        self.add_bullet_item("Paired-Samples t-Test", "Used to compare continuous normal operational variables, specifically latency in milliseconds.")
        self.add_bullet_item("Cohen's Kappa (κ)", "Used to evaluate inter-rater agreement among faculty raters, as well as the agreement between the automated VLM verifier and human clinical scores, testing the validity of the automated judge as established by Hayes et al. (2025).")
        self.add_body_paragraph(
            "The null hypothesis (H0) states that there is no significant difference between diffusion-generated PNGs and parametric 3D "
            "heads in trait fidelity, clinical plausibility, skin-tone fidelity, or processing time. The alternative hypothesis (H1) asserts "
            "that a significant difference exists. All tests use a significance threshold of α = 0.05, with α = 0.01 used to designate "
            "high statistical significance."
        )

        self.add_major_heading("System Architecture")
        self.add_body_paragraph(
            "The patient-face generation module uses a three-tier architecture that integrates seamlessly with the existing Chansey HIS platform."
        )
        self.add_figure("Figure 3.4", "Three-Tier System Architecture of the Chansey FaceGen Platform")

        self.add_subcomponent("1. Presentation Layer")
        self.add_body_paragraph(
            "The presentation layer provides the user interfaces for faculty and students. Built with Blade templates, Tailwind CSS, "
            "and lightweight JavaScript, it includes:"
        )
        self.add_bullet_item("Faculty Scenario Builder", "where instructors enter scenario text, click \"Generate Patient Face\", review generated options, inspect VLM checklist logs, and grant final approval.")
        self.add_bullet_item("Student Ward View", "where the approved patient face appears on the virtual bedside chart alongside real-time vitals, physician orders, and nurse notes.")

        self.add_subcomponent("2. Application Layer")
        self.add_body_paragraph(
            "The application layer coordinates clinical business logic and AI generation:"
        )
        self.add_bullet_item("Laravel Backend", "Receives scenario inputs, enforces authorization policies, dispatches asynchronous HTTP calls to the microservice, and stores approved assets.")
        self.add_bullet_item("FastAPI Microservice (services/facegen)", "Executes the agentic pipeline. It handles text parsing, calls external cloud APIs for diffusion, manages local CPU-based mesh deformation for FLAME, and formats verification reports.")

        self.add_subcomponent("3. Data Layer")
        self.add_body_paragraph(
            "The data layer manages structured records and generated media:"
        )
        self.add_bullet_item("PostgreSQL Database", "Stores scenario definitions, clinical orders, user accounts, structured trait schema JSON blobs, and audit logs.")
        self.add_bullet_item("Asset Storage", "Stores generated PNG images and exported 3D model assets, flagged with AI-generated provenance metadata.")

        self.add_major_heading("Data Flow Diagram (DFD)")
        self.add_body_paragraph(
            "The flow of data through the system is documented across two levels of detail."
        )

        self.add_subcomponent("Level 0 Data Flow Diagram (Context DFD)")
        self.add_figure("Figure 3.5", "Level 0 Context Data Flow Diagram")
        self.add_body_paragraph(
            "Faculty submit scenario descriptions and receive rendered previews paired with verification reports. Once approved, "
            "the platform binds the visual to the scenario admission. Nursing students access the simulation patient chart, observing the "
            "rendered physical signs while conducting simulated clinical care."
        )

        self.add_subcomponent("Level 1 Data Flow Diagram (Generation and Review Pipeline)")
        self.add_figure("Figure 3.6", "Level 1 Data Flow Diagram of the FaceGen Pipeline")
        self.add_body_paragraph(
            "The level 1 pipeline shows the detailed transition from free text input to LLM parsing, disease expansion, renderer branching "
            "between diffusion and FLAME 3D, vision-language model verification checklist generation, and final instructor approval."
        )

        self.add_major_heading("Entity-Relationship Diagram (ERD)")
        self.add_figure("Figure 3.7", "Entity-Relationship Diagram (ERD)")

        self.add_subcomponent("Database Table Descriptions")
        self.add_bullet_item("scenarios", "Core table storing scenario titles, clinical background, and simulation admission details.")
        self.add_bullet_item("trait_schemas", "Stores normalized clinical parameters extracted from the text (demographics, skin tone, and sign arrays with severity and laterality).")
        self.add_bullet_item("scenario_face_assets", "Stores generated output metadata, including the modality type (png or 3d), file path, random seed, latency, token consumption, and approval status.")
        self.add_bullet_item("vlm_audit_logs", "Logs automated verification results, recording which traits were identified as present, missing, or hallucinated.")
        self.add_bullet_item("faculty_evaluations", "Stores blinded faculty Likert scores and qualitative remarks collected during the experimental evaluation.")

        self.add_major_heading("Use Case Diagrams")
        self.add_body_paragraph(
            "The behavioral interactions with the system are divided into instructor and student use cases."
        )

        self.add_subcomponent("Faculty Use Case Diagram")
        self.add_figure("Figure 3.8", "Faculty Use Case Diagram")
        self.add_body_paragraph(
            "The primary use cases include authoring scenario descriptions, triggering generation across either modality, confirming "
            "signs proposed by the expander agent, reviewing the automated VLM audit report, and approving the final face asset."
        )

        self.add_subcomponent("Student Use Case Diagram")
        self.add_figure("Figure 3.9", "Student Use Case Diagram")
        self.add_body_paragraph(
            "Students do not interact with the generation pipeline directly. Instead, they view the approved patient face within the "
            "bedside chart, correlating visual symptoms (such as lip pallor or scleral icterus) with vital signs and physician orders."
        )

        self.add_major_heading("Sequence Diagram")
        self.add_body_paragraph(
            "Figure 3.10 outlines the chronological sequence of operations during face generation and approval."
        )
        self.add_figure("Figure 3.10", "Sequence Diagram for Patient Face Generation and Approval")

        self.add_major_heading("Machine Learning and Agent Pipeline Diagram")
        self.add_body_paragraph(
            "Figure 3.11 illustrates the end-to-end execution pipeline. This pipeline remains constant across both experimental arms, "
            "ensuring that prompt handling, schema normalization, and verification standards do not vary between modalities."
        )
        self.add_figure("Figure 3.11", "Constant Agentic Generation and Verification Pipeline")
        self.add_body_paragraph(
            "The pipeline enforces an instructor-in-the-loop architecture. When given disease-only inputs (such as \"severe dehydration\"), "
            "the expander agent proposes visible signs (sunken eyes, dry lips), but these must be confirmed by the instructor before "
            "rendering occurs. The system never silently invents clinical traits."
        )

        self.add_major_heading("Software Requirements Specification (SRS)")
        self.add_body_paragraph(
            "This section defines the minimum and recommended hardware, software, and functional parameters required to execute the platform."
        )

        # Table 3.2
        self.add_table_title("Table 3.2", "System Requirements Specification (Hardware, Software, Network, and Environment)")
        tbl2 = self.doc.add_table(rows=8, cols=3)
        tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl2.autofit = False

        headers2 = ["Category", "Minimum Requirements", "Recommended Requirements"]
        rows2_data = [
            ["Operating System", "Windows 10 (64-bit), Ubuntu 20.04 LTS", "Windows 11 (64-bit), Ubuntu 22.04 LTS"],
            ["Web Browser", "Google Chrome, Microsoft Edge, Brave (latest 2 versions)", "Google Chrome, Brave (latest updated version)"],
            ["Backend Environment", "PHP 8.2+, Python 3.10+, Composer 2.5+", "PHP 8.3+, Python 3.11+, Composer 2.7+"],
            ["Libraries & Packages", "Laravel 12, FastAPI, Pydantic, NumPy, PyTorch (CPU)", "Laravel 12, FastAPI, PyTorch (CPU), PyRender, Trimesh"],
            ["Database", "SQLite 3.35+", "PostgreSQL 14+"],
            ["Client Hardware", "Intel Core i3 / AMD Ryzen 3, 8 GB RAM", "Intel Core i5 / AMD Ryzen 5, 16 GB RAM"],
            ["Network & Hosting", "Broadband Internet (20 Mbps) for API calls", "Stable Broadband (50 Mbps+)"]
        ]

        col_widths2 = [Inches(1.8), Inches(2.2), Inches(2.5)]

        for j, text in enumerate(headers2):
            cell = tbl2.cell(0, j)
            cell.width = col_widths2[j]
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.line_spacing = 1.0
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            r = p_c.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(10)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

        for i, row in enumerate(rows2_data):
            for j, val in enumerate(row):
                cell = tbl2.cell(i + 1, j)
                cell.width = col_widths2[j]
                p_c = cell.paragraphs[0]
                p_c.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p_c.paragraph_format.line_spacing = 1.0
                p_c.paragraph_format.space_before = Pt(2)
                p_c.paragraph_format.space_after = Pt(2)
                r = p_c.add_run(val)
                r.font.name = 'Arial'
                r.font.size = Pt(10)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

        set_apa_table_borders(tbl2)

        self.add_subcomponent("Functional Requirements")
        self.add_numbered_item("1", "Clinical Text Parsing:", "The system shall parse free-text scenario descriptions into a structured trait schema containing sex, age group, skin tone, and an array of clinical signs with anatomical region, laterality, and severity.")
        self.add_numbered_item("2", "Diagnosis Expansion with Confirmation:", "When an instructor inputs a diagnosis without physical traits, the system shall propose typical visible signs and require instructor confirmation before rendering.")
        self.add_numbered_item("3", "Dual Modality Rendering:", "The system shall support rendering patient faces via both diffusion-based PNG synthesis (Arm A) and parametric 3D mesh projection (Arm B).")
        self.add_numbered_item("4", "Agentic Editing Loop:", "For the diffusion arm, the system shall automatically trigger localized inpainting edits (up to two cycles) if the automated verifier detects missing requested traits.")
        self.add_numbered_item("5", "Deterministic Parametric Mapping:", "For the 3D arm, the system shall map color signs to standardized anatomical UV albedo regions and map structural signs to calibrated FLAME blendshape weights without relying on random seeds.")
        self.add_numbered_item("6", "Automated VLM Verification:", "The system shall evaluate rendered images against a structured trait checklist using a vision-language model and output a structured report of present, missing, and hallucinated features.")
        self.add_numbered_item("7", "Instructor Approval Gate:", "The system shall keep all generated faces in an unapproved preview state until explicitly accepted by faculty.")
        self.add_numbered_item("8", "Clinical Simulation Integration:", "Upon approval, the system shall bind the image asset to the patient admission record in Chansey, making it visible on the virtual bedside chart during student simulations.")

        self.add_subcomponent("Non-Functional Requirements")
        self.add_numbered_item("1", "Performance and Latency:", "API-based diffusion generation and CPU-based 3D rendering shall complete within 15 seconds per generation cycle to remain practical for real-time classroom scenario authoring.")
        self.add_numbered_item("2", "Reliability and Determinism:", "The 3D parametric arm shall yield identical mesh geometry and color parameters when executed repeatedly on the same trait schema.")
        self.add_numbered_item("3", "Data Privacy and Protection:", "The system shall use synthetic generative modeling exclusively and shall not ingest, store, or process real patient photographs, complying with Republic Act No. 10173 (Philippine Data Privacy Act of 2012).")
        self.add_numbered_item("4", "Usability:", "The interface shall provide side-by-side visual comparisons, trait confirmation checkboxes, and clear status badges indicating whether an asset is approved or pending review.")
        self.add_numbered_item("5", "Availability:", "The local microservice and web application shall remain operational without requiring local GPU acceleration, relying on standard cloud API endpoints for neural rendering.")
        self.add_numbered_item("6", "Scalability:", "The database and file storage architecture shall support expanding sign catalogs and growing libraries of approved simulation scenarios across multiple academic terms.")
        self.add_numbered_item("7", "Compatibility:", "Generated image assets shall render seamlessly across modern web browsers without requiring client-side graphics extensions or specialized hardware.")
        self.add_numbered_item("8", "Maintainability:", "The codebase shall maintain modular separation between the Laravel clinical information system and the FastAPI generative microservice, ensuring that AI provider updates do not affect core hospital information workflows.")

    def save(self, filepath):
        self.doc.save(filepath)
        print(f"Document successfully created and saved to: {filepath}")

def main():
    builder = ThesisDocxBuilder()
    
    print("Building Preliminary Pages (Roman Numerals)...")
    builder.build_title_page()
    builder.build_approval_sheet()
    builder.build_acknowledgements()
    builder.build_abstract()
    builder.build_toc()
    builder.build_list_of_tables()
    builder.build_list_of_figures()
    
    print("Transitioning to Main Body (Arabic Numerals)...")
    builder.start_main_section()
    
    print("Building Chapter 1: The Problem and Its Background...")
    builder.build_chapter_1()
    
    print("Building Chapter 2: Review of Related Literature and Studies...")
    builder.build_chapter_2()
    
    print("Building Chapter 3: Methodology...")
    builder.build_chapter_3()
    
    output_path = os.path.join(r"c:\laragon\www\chansey\thesis", "Thesis_Chapters_1_to_3.docx")
    builder.save(output_path)

if __name__ == "__main__":
    main()
