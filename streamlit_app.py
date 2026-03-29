import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="Nauczycielskie Narzędzia PRO", layout="wide", page_icon="🍎")

def setup_font(pdf):
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

# --- GENERATOR LITER A4 ---
def gen_napis(tekst, kolor_hex, styl):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)
    font_name = setup_font(pdf)
    
    # Konwersja hex na RGB
    r = int(kolor_hex.lstrip('#')[:2], 16)
    g = int(kolor_hex.lstrip('#')[2:4], 16)
    b = int(kolor_hex.lstrip('#')[4:6], 16)

    for char in tekst.upper():
        if char.isspace(): continue
        pdf.add_page()
        if styl == "Tylko kontury (szary)":
            pdf.set_text_color(220, 220, 220)
        else:
            pdf.set_text_color(r, g, b)
        
        pdf.set_font(font_name, size=600 if font_name == "Roboto" else 500)
        pdf.set_xy(0, 50)
        pdf.cell(210, 200, char, align='C')
    return bytes(pdf.output())

# --- GENERATOR DYPLOMÓW (WERSJA Z LISTĄ) ---
def gen_dyplomy_seryjne(lista_imion, za_co, data, kolor_ramki):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    font_name = setup_font(pdf)
    
    r = int(kolor_ramki.lstrip('#')[:2], 16)
    g = int(kolor_ramki.lstrip('#')[2:4], 16)
    b = int(kolor_ramki.lstrip('#')[4:6], 16)

    imiona = [i.strip() for i in lista_imion.split('\n') if i.strip()]

    for imie in imiona:
        pdf.add_page()
        # Ramka
        pdf.set_line_width(2)
        pdf.set_draw_color(r, g, b)
        pdf.rect(10, 10, 277, 190)
        
        # Tekst
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, size=50)
        pdf.set_y(40)
        pdf.cell(0, 20, "DYPLOM", align='C', ln=1)
        
        pdf.set_font(font_name, size=20)
        pdf.cell(0, 15, "dla", align='C', ln=1)
        
        pdf.set_font(font_name, size=40)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 30, imie, align='C', ln=1)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, size=22)
        pdf.set_y(120)
        pdf.multi_cell(0, 12, f"za {za_co}", align='C')
        
        pdf.set_y(170)
        pdf.set_font(font_name, size=12)
        pdf.set_x(20)
        pdf.cell(0, 10, f"Data: {data}", align='L')
        pdf.set_x(200)
        pdf.cell(0, 10, "Podpis: ........................", align='L')
    
    return bytes(pdf.output())

# --- INTERFEJS GŁÓWNY ---
st.title("🍎 Centrum Nauczyciela PRO")
tab1, tab2, tab3 = st.tabs(["🔠 Wielkie Litery A4", "🏆 Generator Dyplomów", "✉️ Podziękowania"])

with tab1:
    st.subheader("Dekoracje na gazetki")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        txt = st.text_input("Wpisz hasło:", "WITAJ", key="t1")
    with c2:
        kol = st.color_picker("Kolor liter:", "#003366")
    with c3:
        staly = st.selectbox("Styl:", ["Pełny kolor", "Tylko kontury (szary)"])
    
    if st.button("Generuj Napis"):
        out = gen_napis(txt, kol, staly)
        st.download_button("Pobierz Napis (PDF)", out, "napis.pdf", "application/pdf")

with tab2:
    st.subheader("Seryjne generowanie dyplomów")
    colA, colB = st.columns([1, 1])
    with colA:
        tryb = st.radio("Tryb wpisywania:", ["Jeden uczeń", "Lista uczniów (wielu naraz)"])
        if tryb == "Jeden uczeń":
            lista_imion = st.text_input("Imię i nazwisko:")
        else:
            lista_imion = st.text_area("Wklej listę (jedno imię pod drugim):", "Jan Kowalski\nAnna Nowak")
    
    with colB:
        d_za_co = st.text_area("Treść (za co):", "wzorową postawę i aktywny udział w zajęciach")
        d_data = st.text_input("Data i miejscowość:", "Kraków, 2026")
        d_kolor = st.color_picker("Kolor ramki i imienia:", "#C41E3A")

    if st.button("Generuj wszystkie dyplomy"):
        if lista_imion:
            with st.spinner("Trwa generowanie plików..."):
                pdf_dyplomy = gen_dyplomy_seryjne(lista_imion, d_za_co, d_data, d_kolor)
                st.success("Gotowe! Wygenerowano dyplomy.")
                st.download_button(
                    label="POBIERZ WSZYSTKIE DYPLOMY (JEDEN PDF)",
                    data=pdf_dyplomy,
                    file_name="dyplomy_zbiorcze.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Lista uczniów jest pusta!")

with tab3:
    st.write("Moduł w przygotowaniu...")