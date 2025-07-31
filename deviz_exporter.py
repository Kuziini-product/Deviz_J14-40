from fpdf import FPDF
import pandas as pd

def export_pdf(deviz, nume_fisier):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for item in deviz:
        for k, v in item.items():
            pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    pdf.output(nume_fisier + ".pdf")

def export_excel(deviz, nume_fisier):
    df = pd.DataFrame(deviz)
    df.to_excel(nume_fisier + ".xlsx", index=False)