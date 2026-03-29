import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Generator Dekoracji PRO", page_icon="🎨", layout="wide")

def generate_full_wypas(text, style, color_choice):
    # Orientacja pionowa, jednostka mm, format A4
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    
    # Obsługa czcionki z polskimi znakami
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        pdf.set_font("Roboto", "", 210) # Gigantyczna czcionka
    else:
        pdf.set_font("Helvetica", "B", 170)

    for char in text.upper():
        if char.isspace():
            continue
            
        pdf.add_page()
        
        # Ustawienie kolorów i trybu rysowania
        r, g, b = 0, 0, 0 # Domyślnie czarny
        if color_choice == "Niebieski Królewski": r, g, b = 0, 51, 102
        if color_choice == "Pastelowy Róż": r, g, b = 255, 182, 193
        if color_choice == "Zieleń Szkolna": r, g, b = 34, 139, 34

        pdf.set_text_color(r, g, b)

        # Tryb "Kontury" lub "Pełne"
        if style == "Tylko kontury (do kolorowania)":
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(1)
            pdf.set_render_mode("outline") # Uwaga: fpdf2 wspiera to w specyficzny sposób
            # Jeśli Twoja wersja fpdf2 gryzie się z render_mode, użyjemy jasnego szarego
        
        # Centrowanie litery - Cell(szerokość, wysokość, tekst, ramka, nowa linia, wyrównanie)
        # 210mm to szerokość A4, 297mm to wysokość. 
        # Ustawiamy y na 15, żeby litera nie "uciekła" na dole
        pdf.set_y(40)
        pdf.cell(0, 210, char, border=0, ln=1, align='C')
        
    return bytes(pdf.output())

# --- INTERFEJS ---
st.title("🎨 Profesjonalny Generator Napisów")
st.markdown("Stwórz napisy na gazetki, które zachwycą każdego!")

with st.expander("🛠️ USTAWIENIA NAPISU", expanded=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        napis = st.text_input("Wpisz swoje hasło:", placeholder="Np. PASOWANIE")
    with col2:
        styl = st.selectbox("Styl litery:", ["Pełny kolor", "Tylko kontury (do kolorowania)"])
    with col3:
        kolor = st.selectbox("Kolor:", ["Czarny", "Niebieski Królewski", "Zieleń Szkolna", "Pastelowy Róż"])

if napis:
    try:
        pdf_bytes = generate_full_wypas(napis, styl, kolor)
        
        st.success(f"✅ Projekt gotowy! Liczba stron: {len(napis.replace(' ',''))}")
        
        # Wyświetlamy wielki przycisk pobierania
        st.download_button(
            label="🔥 POBIERZ PDF W JAKOŚCI PRO",
            data=pdf_bytes,
            file_name=f"dekoracja_{napis.lower()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        st.info("💡 Wskazówka: Drukuj bez marginesów (skala 100%), aby litery były jak największe!")
        
    except Exception as e:
        st.error(f"Coś poszło nie tak przy generowaniu: {e}")

st.divider()
st.caption("MagicColor Generator v2.0 | Profesjonalne pomoce dydaktyczne")