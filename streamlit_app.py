import streamlit as st
from fpdf import FPDF
import os

# --- STYLE ---
st.set_page_config(page_title="EduStudio PRO 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { border: none !important; background: none !important; }
    .stButton>button { background-color: #000; color: #fff; border-radius: 5px; height: 3em; width: 100%; }
    .stDownloadButton>button { background-color: #16a34a !important; color: #fff !important; border-radius: 5px; width: 100%; }
    .preview-card { border: 1px solid #eee; padding: 40px; background: #fff; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- KALENDARZ OKAZJI ---
OKAZJE = {
    "✨ Pasowanie na Ucznia": "uroczyste ślubowanie i wstąpienie do grona uczniów",
    "🔴 Dzień Kropki (15.09)": "odkrywanie talentów, kreatywność i odwagę w tworzeniu",
    "🦖 Dzień Dinozaura (26.02)": "zdobycie ogromnej wiedzy o prehistorycznym świecie",
    "🍎 Dzień Nauczyciela": "trud włożony w edukację i serce oddane uczniom",
    "🦕 Super Przedszkolak": "dzielne stawianie kroków w świecie przedszkolnym",
    "🧸 Dzień Misia (25.11)": "przyjaźń z pluszakami i udział w misiowych zabawach",
    "🌍 Dzień Ziemi": "dbanie o naszą planetę i postawę proekologiczną"
}

def load_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_cool_frame(pdf, r, g, b):
    pdf.set_draw_color(r, g, b)
    # Podwójna ramka (Styl Premium)
    pdf.set_line_width(1.5)
    pdf.rect(8, 8, 281, 194)
    pdf.set_line_width(0.3)
    pdf.rect(10, 10, 277, 190)
    # Narożniki ozdobne
    pdf.set_line_width(2)
    pdf.line(5, 5, 20, 5); pdf.line(5, 5, 5, 20) # GL
    pdf.line(277, 5, 292, 5); pdf.line(292, 5, 292, 20) # GP

def gen_pdf(mode, items, col, za_co, data, title):
    pdf = FPDF(orientation='L' if mode=='dyplom' else 'P', unit='mm', format='A4')
    fn = load_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        if mode == 'dyplom':
            draw_cool_frame(pdf, r, g, b)
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50)
            pdf.set_y(30); pdf.cell(0, 20, title.upper(), align='C', ln=1)
            
            pdf.set_font(fn, size=15); pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 10, "dla", align='C', ln=1)
            
            pdf.set_font(fn, size=55); pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, name.upper(), align='C', ln=1)
            
            # Linia ozdobna pod imieniem
            pdf.set_draw_color(r, g, b); pdf.set_line_width(0.5)
            pdf.line(100, 110, 197, 110)
            
            pdf.set_y(125); pdf.set_text_color(50, 50, 50)
            pdf.set_font(fn, size=22)
            pdf.multi_cell(0, 12, f"za {za_co}", align='C')
            
            pdf.set_y(175); pdf.set_font(fn, size=12)
            pdf.set_x(25); pdf.cell(0, 10, f"Miejscowość i data: {data}")
            pdf.set_x(180); pdf.cell(0, 10, "Podpis wychowawcy: ........................")
        else:
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=550 if fn=="Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, name.upper(), align='C')
    return bytes(pdf.output())

# --- UI ---
st.title("🍎 EduStudio PRO: Kreator 2026")

tab1, tab2 = st.tabs(["🔠 Wielkie Litery", "🏆 Dyplomy z Kalendarza"])

with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        txt = st.text_input("Hasło napisu:", "WITAJ")
        color_n = st.color_picker("Kolor liter:", "#1e3a8a")
        if st.button("GENERUJ NAPIS PDF"):
            out_n = gen_pdf('litery', [c for c in txt if not c.isspace()], color_n, "", "", "")
            st.download_button("POBIERZ NAPIS", out_n, "napis.pdf")
    with c2:
        st.markdown(f"<div class='preview-card'><h1 style='font-size:200px; color:{color_n};'>{txt[0].upper() if txt else '?'}</h1></div>", unsafe_allow_html=True)

with tab2:
    sel_okazja = st.selectbox("Wybierz okazję z kalendarza:", list(OKAZJE.keys()))
    colA, colB = st.columns(2)
    with colA:
        imiona = st.text_area("Lista uczniów:", "Jan Kowalski\nAnna Nowak")
        za_co = st.text_area("Za co:", value=OKAZJE[sel_okazja])
    with colB:
        miejscowa = st.text_input("Data i miasto:", "Leżajsk, 2026")
        kolor_d = st.color_picker("Kolor przewodni:", "#b45309")
    
    if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
        lista = [i.strip() for i in imiona.split('\n') if i.strip()]
        out_d = gen_pdf('dyplom', lista, kolor_d, za_co, miejscowa, sel_okazja[2:])
        st.download_button("POBIERZ PACZKĘ PDF", out_d, "dyplomy.pdf")
    
    # Podgląd dyplomu (Nowoczesny)
    st.markdown(f"""
        <div style="border: 10px double {kolor_d}; padding: 40px; margin-top: 20px; text-align: center; color: #333;">
            <h2 style="color:{kolor_d};">{sel_okazja[2:].upper()}</h2>
            <p>dla</p>
            <h1 style="color:{kolor_d};">{imiona.split('\\n')[0]}</h1>
            <hr style="width: 50%; border: 1px solid {kolor_d};">
            <p>za {za_co}</p>
        </div>
    """, unsafe_allow_html=True)