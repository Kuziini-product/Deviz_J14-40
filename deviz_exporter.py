import pandas as pd
from fpdf import FPDF

def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    return (
        text.replace("ă", "a").replace("â", "a").replace("î", "i")
            .replace("ș", "s").replace("ț", "t")
            .replace("Ă", "A").replace("Â", "A").replace("Î", "I")
            .replace("Ș", "S").replace("Ț", "T")
            .replace("•", "-")
    )

def export_excel(deviz_data, nume_fisier):
    df = pd.DataFrame(deviz_data)
    df.to_excel(nume_fisier + ".xlsx", index=False)

def export_pdf(deviz_data, nume_fisier):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, clean_text("Deviz oferta Kuziini"), ln=True, align="C")
    pdf.ln(10)

    headers = ["Produs", "Cod", "UM", "Cantitate", "Preț (lei)"]
    col_widths = [60, 30, 25, 25, 30]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, clean_text(header), border=1)
    pdf.ln()

    total = 0
    for row in deviz_data:
        pdf.cell(col_widths[0], 10, clean_text(row.get("Produs", "")), border=1)
        pdf.cell(col_widths[1], 10, clean_text(row.get("Cod", "")), border=1)
        pdf.cell(col_widths[2], 10, clean_text(row.get("UM", "")), border=1)
        pdf.cell(col_widths[3], 10, str(row.get("Cantitate", "")), border=1)
        pret = row.get("Pret", 0)
        pdf.cell(col_widths[4], 10, f"{pret:.2f}", border=1)
        pdf.ln()
        total += row.get("Cantitate", 0) * pret

    pdf.ln(5)
    pdf.cell(200, 10, clean_text(f"Total general: {total:.2f} lei"), ln=True, align="R")
    pdf.output(nume_fisier + ".pdf")
