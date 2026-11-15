from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape
from datetime import datetime

def generate_pdf_report(report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("MAFDES_Title", parent=styles["Title"], alignment=TA_CENTER,
                           textColor=colors.HexColor("#163A5F"), fontSize=23, spaceAfter=8)
    subtitle = ParagraphStyle("MAFDES_Subtitle", parent=styles["Normal"], alignment=TA_CENTER,
                              textColor=colors.HexColor("#39718F"), fontSize=10, spaceAfter=18)
    story = [
        Paragraph("MAFDES", title),
        Paragraph("Military Aircraft Fault Diagnosis Expert System", subtitle),
        Paragraph("EDUCATIONAL SIMULATION REPORT", styles["Heading2"]),
        Paragraph("Generated: " + escape(str(report.get("time", datetime.now().strftime("%d-%m-%Y %H:%M:%S")))), styles["Normal"]),
        Spacer(1, 12),
        Paragraph("1. Simulation Overview", styles["Heading2"]),
        Paragraph("<b>Subsystem:</b> " + escape(str(report.get("system", "Not specified"))), styles["Normal"]),
        Paragraph("<b>Selected observations:</b> " + escape(", ".join(report.get("symptoms", []))), styles["Normal"]),
        Spacer(1, 14),
        Paragraph("2. Diagnostic Findings", styles["Heading2"])
    ]
    data = [["Finding", "Illustrative confidence", "Activated conditions"]]
    for item in report.get("results", []):
        data.append([
            Paragraph(escape(str(item.get("Fault", ""))), styles["Normal"]),
            f'{item.get("Confidence", 0)}%',
            Paragraph(escape(", ".join(item.get("Rule", []))), styles["Normal"])
        ])
    table = Table(data, colWidths=[170, 105, 205], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#163A5F")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), .5, colors.HexColor("#AAB8C6")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#EEF4F8")]),
        ("PADDING", (0,0), (-1,-1), 8)
    ]))
    story.extend([table, Spacer(1, 14), Paragraph("3. Rule Explanations", styles["Heading2"])])
    for item in report.get("results", []):
        story.append(Paragraph("<b>" + escape(str(item.get("Fault", ""))) + ":</b> " +
                               escape(str(item.get("Explanation", ""))), styles["Normal"]))
        story.append(Spacer(1, 7))
    story.extend([Spacer(1, 14), Paragraph(
        "<b>Disclaimer:</b> This report contains fictional educational simulation results only. "
        "It is not approved for real aircraft inspection, maintenance, flight-safety or operational decisions.",
        styles["Normal"])])
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
