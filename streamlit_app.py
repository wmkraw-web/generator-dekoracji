import streamlit as st
from fpdf import FPDF
import os
import random

# --- DESIGN & CONFIG ---
st.set_page_config(page_title="EduStudio Ultra AI 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 20px !important; }
    
    /* PRZYCISK AI */
    .ai-btn { background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important; border: none !important; color: white !important; font-weight: bold !important; border-radius: 12px !important; margin-bottom: 10px; }
    
    /* PŁÓTNO PODGLĄDU */
    .canvas-pro { background: white !important; border-radius: 20px; padding: 40px; color: black !important; min-height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 2px solid #e2e8f0; position: relative; }
    .canvas-pro h1, .canvas-pro h2, .canvas-pro p { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INTELIGENTNA BAZA TREŚCI (Symulacja AI) ---
KALENDARZ_PRO = {
    "✨ Pasowanie na Ucznia": "Dziś pasowanie, wielkie wydarzenie, przed Tobą nauka i marzeń spełnienie!",
    "🔴 Dzień Kropki": "Od małej kropki talent się zaczyna, każda kropka to Twoja wielka mina!",
    "🦖 Dzień Dinozaura": "Dinozaury wielkie były, przez wieki w ziemi kości skryły. Tyś odkrywcą jest wspaniałym!",
    "🧸 Dzień Misia": "Misiu mały, misiu duży, niech Ci zawsze w podróży służy. Przyjacielem jesteś misia!",
    "🌍 Dzień Ziemi": "Ziemia to dom nasz jedyny, dbajmy o nią dla wspólnej rodziny. Mały ekologu - brawo!",
    "🎈 Dzień Przedszkolaka": "Przedszkolak dzielny, wesoły i miły, niech Cię nigdy nie opuszczą siły!"
}

def get_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_decor(pdf, col, mode):
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(2)
    pdf.rect(7, 7, 285 if mode=='L' else 196, 198 if mode=='L' else 285)
    # Kropki w tle (styl 2026)
    pdf.set_fill_color(r, g, b)
    for _ in range(20):
        pdf.circle(random.randint(10, 280), random.randint(10, 190), 0.5, 'F')

def create_pdf(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    fn = get_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        draw_decor(pdf, col, 'L' if mode=='dyp' else 'P')
        
        if mode == 'dyp':
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_y(85); pdf.cell(0, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 10, za_co, align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            if styl == "Kontur":
                pdf.set_draw_color(r, g, b); pdf.set_text_mode('OUTLINE')
            else:
                pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, name.upper(), align='C')
            pdf.set_text_mode('FILL')
            
    return bytes(pdf.output())

# --- UI ---
st.title("✨ EduStudio Ultra AI 2026")
st.sidebar.markdown("### 🍎 Panel Nauczyciela")
nav = st.sidebar.radio("Zadanie:", ["🔠 Wielkie Napisy", "📜 Dyplomy & AI"])

if nav == "🔠 Wielkie Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        txt = st.text_input("Hasło dekoracji:", "WITAJ")
        kol = st.color_picker("Wybierz kolor:", "#6366f1")
        styl_l = st.radio("Styl liter:", ["Pełny", "Kontur"])
        if st.button("GENERUJ PDF"):
            out = create_pdf('lit', [c for c in txt if not c.isspace()], kol, "", "", "", styl_l)
            st.download_button("📥 POBIERZ", out, "napis.pdf")
    with c2:
        l = txt[0].upper() if txt else "?"
        color_val = "transparent" if styl_l == "Kontur" else kol
        border_val = f"3px solid {kol}" if styl_l == "Kontur" else "none"
        st.markdown(f'<div class="canvas-pro"><h1 style="font-size:300px; color:{kol}; -webkit-text-stroke: {border_val}; color: {color_val};">{l}</h1></div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Wybierz okazję:", list(KALENDARZ_PRO.keys()))
    if st.button("✨ AI: GENERUJ RYMOWANKĘ"):
        st.session_state.tresc = KALENDARZ_PRO[okazja]
        st.balloons()
    
    c1, c2 = st.columns(2)
    with c1:
        imiona = st.text_area("Lista dzieci:", "Ania Nowak\nKuba Kowalski")
        tresc = st.text_area("Treść wyróżnienia:", value=st.session_state.get('tresc', 'za wzorową postawę'))
    with c2:
        miejsc = st.text_input("Data:", "Warszawa, 2026")
        kol_d = st.color_picker("Kolor dyplomu:", "#f59e0b")
        if st.button("GENERUJ DYPLOMY"):
            out_d = create_pdf('dyp', [i.strip() for i in imiona.split('\n') if i.strip()], kol_d, tresc, miejsc, okazja[2:], "")
            st.download_button("📥 POBIERZ PACZKĘ", out_d, "dyplomy.pdf")
            
    st.markdown(f'<div class="canvas-pro" style="border: 10px double {kol_d}"><h2 style="color:{kol_d}">{okazja.upper()}</h2><h1>{imiona.split("\\n")[0]}</h1><p>za {tresc}</p></div>', unsafe_allow_html=True)