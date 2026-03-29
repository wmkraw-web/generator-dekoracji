import streamlit as st
from fpdf import FPDF
import os# --- NO

# --- KONFIGURACJA I DESIGN ---
st.set_page_config(page_title="MagicColor Educator PRO", layout="wide", page_icon="🎨")

# SŁOWNIK OKAZJI (zostawiamy bez zmian)
OKAZJE = {
    "🌟 Pasowanie": {"tekst": "uroczyste ślubowanie i wstąpienie do grona uczniów", "kolor": "#003366"},
    "❤️ Dzień Rodziców": {"tekst": "ogromne serce, miłość i codzienne wsparcie", "kolor": "#E6007E"},
    "🏆 Koniec Roku": {"tekst": "bardzo dobre wyniki w nauce oraz wzorowe zachowanie", "kolor": "#D4AF37"},
    "🎈 Przedszkolak": {"tekst": "dzielne stawianie pierwszych kroków w przedszkolu", "kolor": "#FF8C00"}
}

# --- NOWOCZESNY DESIGN (WERSJA POPRAWIONA) ---
st.markdown("""
    <style>
    /* Naprawa kolorów zakładek */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f8f9fa; 
        border-radius: 12px 12px 0 0; 
        padding: 12px 25px;
        border: 1px solid #e0e0e0;
        color: #333 !important; /* Ciemny tekst na nieaktywnej zakładce */
    }
    .stTabs [aria-selected="true"] { 
        background-color: #FF4B4B !important; 
        color: white !important; 
        border: 1px solid #FF4B4B !important;
    }

    /* Przyciski - Napis w środku będzie teraz wyraźniejszy */
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 800 !important; /* Grubszy tekst */
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        border: 2px solid #FF4B4B !important;
        background-color: white !important;
        color: #FF4B4B !important;
    }

    /* Efekt po najechaniu - przycisk robi się pełny */
    div.stButton > button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    
    /* Przycisk pobierania - zielony i wyraźny */
    div.stDownloadButton > button {
        border: 2px solid #28a745 !important;
        color: #28a745 !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #28a745 !important;
        color: white !important;
    }

    /* Naprawa białych tekstów w ciemnym motywie Streamlit */
    h1, h2, h3, p, span { color: #f0f2f6 !important; }
    .stMarkdown div p { color: #f0f2f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKCJE POMOCNICZE ---
def setup_font(pdf):
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

def generate_pdf_final(mode, data_dict):
    pdf = FPDF(orientation=data_dict['ori'], unit='mm', format='A4')
    font_name = setup_font(pdf)
    for item in data_dict['items']:
        pdf.add_page()
        r, g, b = int(data_dict['kolor'].lstrip('#')[:2], 16), int(data_dict['kolor'].lstrip('#')[2:4], 16), int(data_dict['kolor'].lstrip('#')[4:6], 16)
        if mode == "litery":
            pdf.set_text_color(r, g, b)
            pdf.set_font(font_name, size=550 if font_name == "Roboto" else 500)
            pdf.set_xy(0, 50)
            pdf.cell(210, 200, item.upper(), align='C')
        else:
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
        st.subheader("Ustawienia napisu")
        txt = st.text_input("Hasło:", "WITAJ")
        kol = st.color_picker("Kolor dekoracji:", "#FF4B4B")
        if st.button("GENERUJ PROJEKT"):
            pdf_b = generate_pdf_final("litery", {'items': [c for c in txt if not c.isspace()], 'kolor': kol, 'ori': 'P'})
            st.download_button("POBIERZ NAPIS (PDF)", pdf_b, "napis.pdf")
    with c2:
        char = txt[0] if txt else "?"
        st.markdown(f"<div style='border:5px solid {kol}; height:350px; display:flex; align-items:center; justify-content:center; border-radius:25px; background:white; box-shadow: 0 10px 20px rgba(0,0,0,0.05);'><h1 style='font-size:180px; color:{kol}; margin:0;'>{char.upper()}</h1></div>", unsafe_allow_html=True)

with t2:
    col_cfg, col_pre = st.columns([1, 1])
    with col_cfg:
        st.subheader("Parametry dyplomów")
        okazja_sel = st.selectbox("Motyw okazji:", list(OKAZJE.keys()))
        imiona_raw = st.text_area("Lista uczniów (imię pod imieniem):", "Jan Kowalski\nAnna Nowak")
        tekst_d = st.text_area("Treść wyróżnienia:", value=OKAZJE[okazja_sel]["tekst"])
        dat_d = st.text_input("Data:", "29 marca 2026")
        kol_d = st.color_picker("Kolor motywu:", OKAZJE[okazja_sel]["kolor"])
        
        if st.button("PRZYGOTUJ DYPLOMY"):
            lista = [i.strip() for i in imiona_raw.split('\n') if i.strip()]
            pdf_d = generate_pdf_final("dyplomy", {'items': lista, 'kolor': kol_d, 'za_co': tekst_d, 'data': dat_d, 'ori': 'L'})
            st.download_button("POBIERZ PACZKĘ DYPLOMÓW", pdf_d, "dyplomy.pdf")

    with col_pre:
        st.subheader("Podgląd pierwszej strony")
        pierwsze_imie = imiona_raw.split('\n')[0] if imiona_raw else "Imię Nazwisko"
        st.markdown(f"""
            <div style='border:8px double {kol_d}; padding:30px; background:white; text-align:center; border-radius:15px; color:#333; box-shadow: 0 10px 25px rgba(0,0,0,0.1);'>
                <h2 style='color:{kol_d}; margin-top:0;'>DYPLOM</h2>
                <p style='font-size:14px;'>dla</p>
                <h1 style='color:{kol_d}; margin:10px 0;'>{pierwsze_imie}</h1>
                <p style='font-size:18px;'>za {tekst_d}</p>
                <div style='margin-top:40px; display:flex; justify-content:space-between; font-size:12px; font-style:italic;'>
                    <span>{dat_d}</span><span>Podpis: ........................</span>
                </div>
            </div>
        """, unsafe_allow_html=True)