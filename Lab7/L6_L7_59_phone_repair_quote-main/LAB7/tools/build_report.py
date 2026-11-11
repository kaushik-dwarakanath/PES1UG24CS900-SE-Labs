"""Build the consolidated Lab 7 submission from real evidence and final sources."""
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "PES1UG24CS900_Kaushik_Krishna_Dwarakanath_LAB7.pdf"
# Use the installed Unicode body and monospace fonts.

for family, name in [("DejaVu Sans", "Body"), ("DejaVu Sans Mono", "Code")]:
    path = subprocess.check_output(
        ["fc-match", "-f", "%{file}", family], text=True,
    ).strip()
    pdfmetrics.registerFont(TTFont(name, path))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Text", fontName="Times-Roman", fontSize=12, leading=16,
                          spaceAfter=10, alignment=TA_LEFT))
styles["Heading1"].fontName = "Times-Bold"
styles["Heading1"].fontSize = 14
styles["Heading1"].leading = 18
styles["Heading1"].spaceBefore = 10
styles["Heading1"].spaceAfter = 6
styles.add(ParagraphStyle("Source", fontName="Code", fontSize=8.5, leading=11))
styles.add(ParagraphStyle("Label", fontName="Times-Roman", fontSize=11, leading=14,
                          spaceAfter=6))
story = []


def paragraph(text):
    story.append(Paragraph(text, styles["Text"]))


def title(text):
    story.append(Paragraph(text, styles["Heading1"]))
    story.append(Spacer(1, 6))


title("Lab 7: Fuzzing for Input Validation Bugs")
paragraph("Name: Kaushik Krishna Dwarakanath<br/>"
          "SRN: PES1UG24CS900<br/>Section: 5-B<br/>"
          "Subject: Software Engineering<br/>Date: 11 November 2026")
paragraph("<b>Objective:</b> Use Hypothesis to identify unexpected-input failures in "
          "the three supplied parsers, harden them, and verify both crash resistance "
          "and expected outputs. File names follow the assignment repository README.")
paragraph("<b>Environment:</b> Python 3.15.0, pytest 9.2.0, Hypothesis 6.170.15, "
          "Linux. Dependencies are pinned "
          "in requirements.txt; tests run in a local virtual environment.")
rows = [["Function", "Observed failure / edge case", "Correction"],
        ["mask_imei", "None raises AttributeError; arbitrary characters leak through.",
         "Guard types; accept cleaned ASCII digits; return empty string otherwise."],
        ["parse_parts_order", "Empty/missing/extra separators, None, bytes and invalid quantities raise exceptions.",
         "Validate each entry; skip malformed items; safely convert positive quantities."],
        ["parse_model", "Empty or single-word input raises ValueError; None/bytes crash; tabs split incorrectly.",
         "Guard types; split on whitespace; return a consistent two-string tuple."]]
for function, problem, fix in rows[1:]:
    paragraph(f"<b>{escape(function)}</b><br/>{escape(problem)} {escape(fix)}")
paragraph("<b>Results:</b> Original module: all three fuzz tests fail. Fixed module: "
          "23 tests pass, comprising 3 properties with 500 passing generated examples "
          "each and 20 regression cases. Baseline commit: ffb09ca. Full minimized "
          "failures and final statistics are preserved in evidence/.")

title("Reflections")
paragraph("<b>Reflection 1: What bugs did fuzz testing reveal?</b><br/>"
          "The original functions trusted input types and formats. Hypothesis "
          "automatically reduced failures to None, empty strings and empty bytes. "
          "These expose method calls on unsupported types and tuple unpacking with "
          "too few fields. It also found a non-digit string accepted by the masking "
          "function. Deterministic regressions additionally check invalid numeric "
          "quantities, names containing x, duplicate parts, Unicode and whitespace.")
paragraph("<b>Reflection 2: How does fuzz testing complement ordinary unit tests?</b><br/>"
          "A property describes a general requirement, such as never crashing and "
          "returning a consistent output type. Hypothesis generates varied inputs "
          "and shrinks failures into small counterexamples. The three properties "
          "cover arbitrary Unicode, None, numbers, bytes and containers; the parts "
          "strategy also generates valid orders. Twenty fixed cases check concrete "
          "results. Passing finite samples does not prove correctness for all inputs.")
paragraph("<b>Reflection 3: How were the fixes validated and what are their limits?</b><br/>"
          "The same tests were run before and after the fixes. Type checks prevent "
          "unsupported method calls; structural checks prevent unsafe unpacking; "
          "quantity validation and a narrow ValueError handler protect conversion. "
          "The corrected CLI repeats the malformed input that crashed originally "
          "and reaches the model prompt. All final tests pass. These are parsing "
          "helpers: IMEI checksum validation and a parts catalogue are outside scope.")
paragraph("<b>Contracts:</b> IMEI input loses ASCII spaces/dashes, then must contain "
          "only ASCII digits; invalid input returns an empty string. Up to four "
          "digits remain visible. Parts entries require whitespace before lowercase "
          "x and a positive ASCII integer of at most 4300 digits; invalid entries "
          "are skipped, and the last valid duplicate wins. Model whitespace is "
          "normalized; a brand alone has an empty model, and absent/non-string "
          "input returns two empty strings.")
paragraph("<b>Prompt note:</b> The README requests three reflection answers, but the "
          "supplied PDF and instruction image list no reflection questions. The "
          "three prompts above are supplementary reflections on the stated learning "
          "outcomes, not quotations from the handout.")

screens = [
    ("SS1: Original application", "SS1_original_application.png",
     "Valid inputs run successfully. Repeating with parts input 'screen' raises ValueError before the model prompt."),
    ("SS2: Failing Hypothesis tests", "SS2_failing_fuzz_tests.png",
     "The three fuzz tests fail on the original module. The terminal shows the minimized None model failure, the three-test summary, and a direct IMEI failure. Full details: SS2_buggy_fuzz_full.txt."),
    ("SS3: Corrected application", "SS3_fixed_application.png",
     "Normal inputs retain their results. The same malformed parts input returns an empty order; the single-word model and all three None calls complete safely."),
    ("SS4: Final passing test suite", "SS4_passing_tests.png",
     "The full test file passes: three Hypothesis properties and twenty regression cases. Separate final_fuzz_statistics.txt records 500 passing examples for each property."),
]
story.append(PageBreak())
title("Screenshots")
for heading, filename, caption in screens:
    img = Image(str(ROOT / "evidence" / filename))
    scale = min((A4[0] - 144) / img.imageWidth, 290 / img.imageHeight)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    story.append(KeepTogether([
        Paragraph(heading, styles["Heading1"]), img, Spacer(1, 8),
        Paragraph(escape(caption), styles["Label"]), Spacer(1, 12),
    ]))

for filename in ["phone_repair_quote_parser.py", "test_phone_repair_quote_parser.py"]:
    story.append(PageBreak())
    title(filename)
    story.append(Preformatted(
        (ROOT / filename).read_text(), styles["Source"],
        maxLineLength=87, splitChars=" ", newLineChars="    ",
    ))


doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                        leftMargin=72, rightMargin=72, topMargin=60, bottomMargin=60,
                        title="Lab 7 - Fuzz Testing - PES1UG24CS900",
                        author="Kaushik Krishna Dwarakanath")
doc.build(story)
print(OUTPUT)
