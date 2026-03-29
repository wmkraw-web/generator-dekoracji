import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Generator Dekoracji PRO", layout="wide")

def generate_full_wypas(text, style, color_choice):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)
    
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        font_name = "Roboto"
    else:
        font_name = "Helvetica"

    for char in text.upper():
        if char.isspace(): continue
        pdf.add_page()
        
        # Kolory RGB
        colors = {
            "Czarny": (0, 0, 0),
            "Niebieski Królewski": (0, 51, 102),
            "Zieleń Szkolna": (34, 139, 34),
            "Pastelowy Róż": (255, 182, 193)
        }
        r, g, b = colors.get(color_choice, (0, 0, 0))
        
        # Ustawienie renderowania
        if style == "Tylko kontury (do kolorowania)":
            pdf.set_text_color(255, 255, 255)
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(1)
            pdf.set_render_mode("fill_and_stroke")
        else:
            pdf.set_text_color(r, g, b)
            pdf.set_render_mode("fill")

        # Rozmiar 600 jest bezpieczniejszy dla A4
        pdf.set_font(font_name, "B" if font_name=="Helvetica" else "", 600)
        
        # --- KLUCZOWA POPRAWKA: POZYCJONOWANIE ---
        # Ustawiamy kursor niżej (np. 60mm od góry), żeby litera nie wystawała poza stronę
        pdf.set_xy(0, 50) 
        pdf.cell(210, 200, char, border=0, align='C')
        
    return bytes(pdf.output())
# --- INTERFEJS ---
st.title("🎨 Profesjonalny Generator Napisów")

with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        napis = st.text_input("Wpisz hasło:", value="WITAJ")
    with col2:
        styl = st.selectbox("Styl litery:", ["Pełny kolor", "Tylko kontury (do kolorowania)"])
    with col3:
        kolor = st.selectbox("Kolor:", ["Czarny", "Niebieski Królewski", "Zieleń Szkolna", "Pastelowy Róż"])

if napis:
    try:
        pdf_bytes = generate_full_wypas(napis, styl, kolor)
        st.success(f"✅ Wygenerowano {len(napis.replace(' ',''))} stron(y) w formacie PRO.")
        
        st.download_button(
            label="📥 POBIERZ PDF (WIELKIE LITERY)",
            data=pdf_bytes,
            file_name=f"napis_{napis.lower()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Błąd: {e}")