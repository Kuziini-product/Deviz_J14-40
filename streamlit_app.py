
import streamlit as st
from ai_generator import genereaza_deviz_AI
from deviz_exporter import export_excel, export_pdf
from drive_uploader import init_drive, upload_to_drive
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Kuziini | Generator Devize", layout="wide")

if Path("Kuziini_logo_negru.png").exists():
    st.image("Kuziini_logo_negru.png", width=250)

st.title("Kuziini | Configurator AI Devize Mobilier")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

df_accesorii = pd.read_csv("Accesorii_clean.csv")

nr_oferte = len(list(output_dir.glob("OF-*.json")))
st.markdown(f"📊 Devize generate: **{nr_oferte}**")

col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client", key="nume_client")
with col2:
    telefon_client = st.text_input("Telefon client", key="telefon_client")

col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime", min_value=0, key="inaltime")
with col2:
    latime = st.number_input("Lățime", min_value=0, key="latime")
with col3:
    adancime = st.number_input("Adâncime", min_value=0, key="adancime")

tip_mobilier = st.selectbox("Tip mobilier:", [
    "Corp bază bucătărie", "Corp suspendat bucătărie",
    "Corp colțar bază", "Corp colțar suspendat",
    "Dulap dressing", "Comodă", "Poliță simplă",
    "Ansamblu bucătărie", "Ansamblu dressing"
])

prompt = st.text_area("Descriere pentru AI", key="prompt")
foloseste_gpt = st.checkbox("Folosește GPT pentru rescriere prompt", value=True)

if st.button("Generează ofertă"):
    with st.spinner("🧠 Se generează devizul..."):
        nr_nou = nr_oferte + 1
        cod = f"OF-2025-{nr_nou:04d}_{nume_client.replace(' ', '')}"

        prompt_final = prompt
        if foloseste_gpt:
            prompt_final = f"Generează un deviz pentru un {tip_mobilier} cu dimensiunile {inaltime}x{latime}x{adancime} mm. {prompt}"

        rezultat = genereaza_deviz_AI(prompt_final)

        lista_materiale = []
        valoare_total = 0
        for _, row in df_accesorii.iterrows():
            if str(row["Nume"]).lower() in rezultat.lower():
                item = {
                    "Produs": row["Nume"],
                    "Cod": row["Cod"],
                    "UM": row["UM"],
                    "Cantitate": 1,
                    "Pret": row["Pret"]
                }
                lista_materiale.append(item)
                valoare_total += row["Pret"]

        meta = {
            "cod_oferta": cod,
            "client": nume_client,
            "telefon": telefon_client,
            "dimensiuni": [inaltime, latime, adancime],
            "tip": tip_mobilier,
            "prompt": prompt,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "valoare_total": valoare_total
        }

        with open(output_dir / f"{cod}.json", "w") as f:
            json.dump(meta, f, indent=2)

        st.success("✅ Deviz generat")
        st.markdown(f"**Număr ofertă:** `{cod}`")
        st.text_area("Rezultat AI:", rezultat, height=300)

        export_pdf(lista_materiale, str(output_dir / cod))
        export_excel(lista_materiale, str(output_dir / cod))

        service = init_drive()
        for f in [f"{cod}.json", f"{cod}.pdf", f"{cod}.xlsx"]:
            upload_to_drive(service, str(output_dir / f), nume_client)

        st.success("📤 Fișierele au fost urcate în Google Drive!")
