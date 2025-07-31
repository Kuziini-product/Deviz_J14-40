import streamlit as st
from ai_generator import genereaza_deviz_AI
from deviz_exporter import export_excel, export_pdf
from drive_uploader import init_drive, upload_to_drive
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path

load_dotenv()
st.set_page_config(page_title="Kuziini | Generator Devize", layout="wide")

if Path("Kuziini_logo_negru.png").exists():
    st.image("Kuziini_logo_negru.png", width=250)

st.title("Kuziini | Configurator AI Devize Mobilier")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

nr_oferte = len(list(output_dir.glob("OF-*.json")))
st.markdown(f"📊 Devize generate: **{nr_oferte}**")

col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client", value=st.session_state.get("nume_client", ""), key="nume_client")
with col2:
    telefon_client = st.text_input("Telefon client", value=st.session_state.get("telefon_client", ""), key="telefon_client")

col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime", min_value=0, value=st.session_state.get("inaltime", 0), key="inaltime")
with col2:
    latime = st.number_input("Lățime", min_value=0, value=st.session_state.get("latime", 0), key="latime")
with col3:
    adancime = st.number_input("Adâncime", min_value=0, value=st.session_state.get("adancime", 0), key="adancime")

tipuri = [
    "Corp bază bucătărie", "Corp suspendat bucătărie",
    "Corp colțar bază", "Corp colțar suspendat",
    "Dulap dressing", "Comodă", "Poliță simplă",
    "Ansamblu bucătărie", "Ansamblu dressing"
]
tip_mobilier = st.selectbox("Tip mobilier:", tipuri, index=tipuri.index(st.session_state.get("tip_mobilier", tipuri[0])))

prompt = st.text_area("Descriere pentru AI", value=st.session_state.get("prompt", ""), key="prompt")
foloseste_gpt = st.checkbox("Folosește GPT pentru rescriere prompt", value=True)

if st.button("Generează ofertă"):
    with st.spinner("🧠 Se generează devizul..."):
        nr_nou = nr_oferte + 1
        cod = f"OF-2025-{nr_nou:04d}_{nume_client.replace(' ', '')}"
        prompt_final = prompt
        if foloseste_gpt:
            prompt_final = f"Generează un deviz pentru un {tip_mobilier} cu dimensiunile {inaltime} x {latime} x {adancime} mm. {prompt}"

        rezultat = genereaza_deviz_AI(prompt_final)

        meta = {
            "cod_oferta": cod,
            "client": nume_client,
            "telefon": telefon_client,
            "dimensiuni": [inaltime, latime, adancime],
            "tip": tip_mobilier,
            "prompt": prompt,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "valoare_total": 1000.00
        }

        output_json = output_dir / f"{cod}.json"
        with open(output_json, "w") as f:
            json.dump(meta, f, indent=2)

        st.success("✅ Deviz generat")
        st.markdown(f"**Număr ofertă:** `{cod}`")
        st.text_area("Rezultat AI:", rezultat, height=300)

        deviz = [{
            "Produs": tip_mobilier,
            "Cod": "AI-001",
            "UM": "buc",
            "Cantitate": 1,
            "Pret": 1000.00
        }]
        export_pdf(deviz, str(output_json.with_suffix("")))
        export_excel(deviz, str(output_json.with_suffix("")))

        drive = init_drive()
        client_folder = nume_client.strip().replace(" ", "_")
        for f in [output_json, output_json.with_suffix(".pdf"), output_json.with_suffix(".xlsx")]:
            if f.exists():
                upload_to_drive(drive, str(f), client_folder)

        st.session_state.update({
            "nume_client": nume_client,
            "telefon_client": telefon_client,
            "inaltime": inaltime,
            "latime": latime,
            "adancime": adancime,
            "tip_mobilier": tip_mobilier,
            "prompt": prompt
        })

# Istoric oferte
st.subheader("📂 Istoric oferte generate")
oferta_files = sorted(output_dir.glob("OF-*.json"), reverse=True)
oferta_options = [f.stem for f in oferta_files]
select_oferta = st.selectbox("Selectează o ofertă:", oferta_options)

if select_oferta:
    path = output_dir / f"{select_oferta}.json"
    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)
        st.markdown(f"### 🔎 Ofertă: `{data.get('cod_oferta', select_oferta)}`")
        st.markdown(f"- 👤 Client: **{data.get('client', 'necunoscut')}**")
        dim = data.get('dimensiuni', [])
        if len(dim) == 3:
            st.markdown(f"- 📏 Dimensiuni: **{dim[0]} x {dim[1]} x {dim[2]} mm**")
        st.markdown(f"- 🧱 Tip corp: **{data.get('tip', 'N/A')}**")
        st.markdown(f"- 💰 Valoare totală: **{data.get('valoare_total', 0)} lei**")

        col1, col2 = st.columns(2)
        with col1:
            pdf_file = output_dir / f"{select_oferta}.pdf"
            if pdf_file.exists():
                with open(pdf_file, "rb") as f:
                    st.download_button("📄 Descarcă PDF", f, file_name=pdf_file.name)
        with col2:
            excel_file = output_dir / f"{select_oferta}.xlsx"
            if excel_file.exists():
                with open(excel_file, "rb") as f:
                    st.download_button("📊 Descarcă Excel", f, file_name=excel_file.name)

        if st.button("🔁 Regenerare această ofertă"):
            dims = data.get("dimensiuni", [0, 0, 0])
            st.session_state.update({
                "nume_client": data.get("client", ""),
                "telefon_client": data.get("telefon", ""),
                "inaltime": dims[0],
                "latime": dims[1],
                "adancime": dims[2],
                "tip_mobilier": data.get("tip", ""),
                "prompt": data.get("prompt", "")
            })
            st.experimental_rerun()