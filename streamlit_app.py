import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="Nauczycielskie Narzędzia PRO", layout="wide", page_icon="🍎")

# Funkcja ładowania czcionki (bezpieczna)
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

# --- GENERATOR DYPLOMÓW ---
def gen_dyplom(imie, za_co, data, kolor_ramki):
    pdf = FPDF(orientation='L', unit='mm', format='A4') # Dyplom poziomo
    pdf.add_page()
    font_name = setup_font(pdf)
    
    # Ramka
    pdf.set_line_width(2)
    pdf.set_draw_color(int(kolor_ramki.lstrip('#')[:2], 16), 
                       int(kolor_ramki.lstrip('#')[2:4], 16), 
                       int(kolor_ramki.lstrip('#')[4:6], 16))
    pdf.rect(10, 10, 277, 190) # Ozdobna obwódka
    
    # Tekst dyplomu
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_name, size=50)
    pdf.set_y(40)
    pdf.cell(0, 20, "DYPLOM", align='C', ln=1)
    
    pdf.set_font(font_name, size=20)
    pdf.cell(0, 20, "dla", align='C', ln=1)
    
    pdf.set_font(font_name, size=40)
    pdf.set_text_color(int(kolor_ramki.lstrip('#')[:2], 16), 0, 0)
    pdf.cell(0, 30, imie, align='C', ln=1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_name, size=20)
    pdf.multi_cell(0, 15, f"za {za_co}", align='C')
    
    pdf.set_y(170)
    pdf.set_font(font_name, size=12)
    pdf.cell(0, 10, f"Data: {data}", align='L')
    pdf.cell(0, 10, "Podpis wychowawcy: ........................", align='R')
    
    return bytes(pdf.output())

# --- INTERFEJS GŁÓWNY ---
st.title("🍎 Centrum Nauczyciela PRO")
tab1, tab2, tab3 = st.tabs(["🔠 Wielkie Litery A4", "🏆 Generator Dyplomów", "✉️ Podziękowania"])

# --- TAB 1: NAPISY ---
with tab1:
    st.subheader("Generator dekoracji na gazetki")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        txt = st.text_input("Wpisz hasło:", "WITAJ", key="t1")
    with c2:
        kol = st.color_picker("Wybierz kolor:", "#003366")
    with c3:
        staly = st.selectbox("Styl:", ["Pełny kolor", "Tylko kontury (szary)"])
    
    if st.button("Generuj Napis"):
        out = gen_napis(txt, kol, staly)
        st.download_button("📥 Pobierz Napis (PDF)", out, f"napis_{txt}.pdf", "application/pdf")

# --- TAB 2: DYPLOMY ---
with tab2:
    st.subheader("Szybki dyplom")
    colA, colB = st.columns(2)
    with colA:
        d_imie = st.text_input("Imię i Nazwisko ucznia:")
        d_za_co = st.text_area("Za co (treść):", "wzorową postawę i wybitne osiągnięcia w nauce")
    with colB:
        d_data = st.text_input("Data i miejscowość:", "Kraków, 2026")
        d_kolor = st.color_picker("Kolor akcentów:", "#FFD700") # Złoty
    
    if st.button("Generuj Dyplom"):
        if d_imie:
            out_d = gen_dyplom(d_imie, d_za_co, d_data, d_kolor)
            st.success(f"Dyplom dla {d_imie} gotowy!")
            st.download_button("📥 Pobierz Dyplom (PDF)", out_d, "dyplom.pdf", "application/pdf")
        else:
            st.warning("Wpisz imię dziecka!")

# --- TAB 3: PODZIĘKOWANIA ---
with tab3:
    st.info("Ta funkcja będzie dostępna wkrótce. Tutaj dodamy zaproszenia na uroczystości!")

st.divider()
st.caption("Aplikacja stworzona dla wsparcia pracy kreatywnego nauczyciela.")