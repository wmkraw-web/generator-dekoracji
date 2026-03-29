import streamlit as st
from fpdf import FPDF
import os

# --- 1. USTAWIENIA I BRUTALNY DESIGN ---
st.set_page_config(page_title="EduStudio PRO 2026", layout="wide")

# Wymuszamy kontrast, żeby nie było "białego na białym"
st.markdown("""
    <style>
    .stApp { background-color: #111 !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #222 !important; border: 1px solid #444 !important; padding: 20px !important; }
    label, p, h1, h2, h3 { color: white !important; }
    
    /* PRZYCISK GENERUJ */
    div.stButton > button { 
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%) !important; 
        color: black !important; font-weight: bold !important; border: none !important; width: 100% !important;
    }
    
    /* BIAŁY PODGLĄD - MUSI BYĆ WYRAŹNY */
    .preview-box { 
        background-color: white !important; padding: 40px; border-radius: 15px; 
        text-align: center; color: black !important; min-height: 400px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .preview-box h1, .preview-box h2, .preview-box p { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KALENDARZ ŚWIĄT ---
KALENDARZ = {
    "Pasowanie": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej",
    "Dzień Kropki": "odkrywanie talentów, wielką kreatywność i odwagę",
    "Dzień Dinozaura": "zdobycie wiedzy o prehistorycznym świecie",
    "Dzień Misia": "przyjaźń z pluszakami i udział w misiowych zabawach",
    "Dzień Ziemi": "postawę proekologiczną i dbanie o naszą planetę",
    "Dzień Przedszkolaka": "radosne reprezentowanie grupy i bycie super kolegą"
}

def get_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

# --- 3. GENERATOR PDF ---
def create_pdf(mode, items, col, za_co, data, tytul):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    fn = get_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for imie in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        # Nowoczesna, gruba rama
        pdf.set_line_width(2); pdf.rect(7, 7, 285 if mode=='dyp' else 196, 198 if mode=='dyp' else 285)
        
        if mode == 'dyp':
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_y(85); pdf.cell(0, 30, imie.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(40, 40, 40); pdf.set_font(fn, size=22)
            pdf.multi_cell(0, 12, f"za {za_co}", align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=500); pdf.set_xy(0, 50)
            pdf.cell(210, 200, imie.upper(), align='C')
    return bytes(pdf.output())

# --- 4. INTERFEJS ---
st.title("✨ EduStudio 2026 - FINAL")

tryb = st.sidebar.radio("MENU:", ["LITERY A4", "DYPLOMY"])

if tryb == "LITERY A4":
    c1, c2 = st.columns(2)
    with c1:
        litery_input = st.text_input("Wpisz tekst:", "WITAJ")
        litery_kolor = st.color_picker("Wybierz kolor:", "#00aaff")
        if st.button("GENERUJ PDF"):
            out = create_pdf('lit', [c for c in litery_input if not c.isspace()], litery_kolor, "", "", "")
            st.download_button("POBIERZ PLIK", out, "napisy.pdf")
    with c2:
        pierwsza = litery_input[0].upper() if litery_input else "?"
        st.markdown(f'<div class="preview-box"><h1 style="font-size:250px; color:{litery_kolor};">{pierwsza}</h1></div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Okazja z kalendarza:", list(KALENDARZ.keys()))
    c1, c2 = st.columns(2)
    with c1:
        imiona = st.text_area("Lista (jedno pod drugim):", "Jan Kowalski\nAnna Nowak")
        tresc = st.text_area("Za co:", value=KALENDARZ[okazja])
    with c2:
        miejscowa = st.text_input("Data:", "Kraków, 2026")
        kolor_d = st.color_picker("Kolor dyplomu:", "#ffaa00")
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            lista = [i.strip() for i in imiona.split('\n') if i.strip()]
            out_d = create_pdf('dyp', lista, kolor_d, tresc, miejscowa, okazja)
            st.download_button("POBIERZ DYPLOMY", out_d, "dyplomy.pdf")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="preview-box" style="border: 10px solid {kolor_d}"><h2 style="color:{kolor_d}">{okazja.upper()}</h2><h1>{imiona.split("\\n")[0]}</h1><p>za {tresc}</p></div>', unsafe_allow_html=True)