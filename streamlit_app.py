import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="MagicColor Educator PRO", layout="wide", page_icon="🎨")

# Stylizacja UI
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #FF4B4B !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

OKAZJE = {
    "🌟 Pasowanie": {"tekst": "uroczyste ślubowanie i wstąpienie do grona uczniów", "kolor": "#003366", "symbol": "🎓"},
    "❤️ Dzień Rodziców": {"tekst": "ogromne serce, miłość i codzienne wsparcie", "kolor": "#E6007E", "symbol": "🌸"},
    "🏆 Koniec Roku": {"tekst": "bardzo dobre wyniki w nauce oraz wzorowe zachowanie", "kolor": "#D4AF37", "symbol": "🎖️"},
    "🎈 Przedszkolak": {"tekst": "dzielne stawianie pierwszych kroków w przedszkolu", "kolor": "#FF8C00", "symbol": "🧸"}
}

def setup_font(pdf):
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

# --- LOGIKA GENEROWANIA PDF ---
def generate_pdf_final(mode, data_dict):
    pdf = FPDF(orientation=data_dict['ori'], unit='mm', format='A4')
    font_name = setup_font(pdf)
    
    for item in data_dict['items']:
        pdf.add_page()
        r, g, b = int(data_dict['kolor'].lstrip('#')[:2], 16), int(data_dict['kolor'].lstrip('#')[2:4], 16), int(data_dict['kolor'].lstrip('#')[4:6], 16)
        
        if mode == "litery":
            pdf.set_text_color(r, g, b)
            pdf.set_font(font_name, size=550)
            pdf.set_xy(0, 50)
            pdf.cell(210, 200, item.upper(), align='C')
        else:
            # Ramka dyplomu
            pdf.set_line_width(2)
            pdf.set_draw_color(r, g, b)
            pdf.rect(10, 10, 277, 190)
            pdf.set_text_color(r, g, b)
            pdf.set_font(font_name, size=60)
            pdf.set_y(40)
            pdf.cell(0, 20, "DYPLOM", align='C', ln=1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font(font_name, size=20)
            pdf.cell(0, 15, "dla", align='C', ln=1)
            pdf.set_font(font_name, size=45)
            pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, item, align='C', ln=1)
            pdf.set_text_color(40, 40, 40)
            pdf.set_font(font_name, size=22)
            pdf.set_y(125)
            pdf.multi_cell(0, 12, f"za {data_dict['za_co']}", align='C')
            pdf.set_y(175)
            pdf.set_font(font_name, size=12)
            pdf.set_x(25)
            pdf.cell(100, 10, f"Data: {data_dict['data']}", align='L')
            pdf.cell(150, 10, "Podpis: ........................", align='R')
            
    return bytes(pdf.output())

# --- INTERFEJS ---
st.title("🚀 MagicColor Educator PRO")

t1, t2 = st.tabs(["🔠 Litery A4", "📜 Dyplomy Seryjne"])

with t1:
    c1, c2 = st.columns([1, 1])
    with c1:
        txt = st.text_input("Napis:", "WITAJ")
        kol = st.color_picker("Kolor:", "#FF4B4B", key="k1")
        if st.button("Generuj Napis PDF"):
            pdf_b = generate_pdf_final("litery", {'items': [c for c in txt if not c.isspace()], 'kolor': kol, 'ori': 'P'})
            st.download_button("Pobierz Napis", pdf_b, "napis.pdf")
    with c2:
        char = txt[0] if txt else "?"
        st.markdown(f"<div style='border:5px solid {kol}; height:300px; display:flex; align-items:center; justify-content:center; border-radius:20px;'><h1 style='font-size:150px; color:{kol};'>{char.upper()}</h1></div>", unsafe_allow_html=True)

with t2:
    okazja_sel = st.selectbox("Wybierz okazję:", list(OKAZJE.keys()))
    col_cfg, col_pre = st.columns([1, 1])
    
    with col_cfg:
        imiona_raw = st.text_area("Lista uczniów (imie pod imieniem):", "Jan Kowalski\nAnna Nowak")
        tekst_d = st.text_area("Treść:", value=OKAZJE[okazja_sel]["tekst"])
        dat_d = st.text_input("Data i miasto:", "Kraków, 2026")
        kol_d = st.color_picker("Kolor motywu:", OKAZJE[okazja_sel]["kolor"], key="k2")
        
        if st.button("Generuj wszystkie dyplomy"):
            lista = [i.strip() for i in imiona_raw.split('\n') if i.strip()]
            pdf_d = generate_pdf_final("dyplomy", {'items': lista, 'kolor': kol_d, 'za_co': tekst_d, 'data': dat_d, 'ori': 'L'})
            st.download_button("Pobierz Paczkę Dyplomów", pdf_d, "dyplomy.pdf")

    with col_pre:
        pierwsze_imie = imiona_raw.split('\n')[0] if imiona_raw else "Imię Nazwisko"
        st.markdown(f"""
            <div style='border:10px double {kol_d}; padding:20px; background:white; text-align:center; border-radius:15px; color:black;'>
                <h2 style='color:{kol_d};'>DYPLOM</h2>
                <p>dla</p>
                <h1 style='color:{kol_d};'>{pierwsze_imie}</h1>
                <p>za {tekst_d}</p>
                <div style='margin-top:30px; display:flex; justify-content:space-between; font-size:12px;'>
                    <span>{dat_d}</span><span>Podpis: ...........</span>
                </div>
            </div>
        """, unsafe_allow_html=True)