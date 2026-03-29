import streamlit as st
from fpdf import FPDF
import os
import random

# --- 1. DESIGN & STYLE ---
st.set_page_config(page_title="EduStudio Ultra 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 20px !important; }
    
    /* PRZYCISK AI */
    .stButton > button { 
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important; 
        color: white !important; font-weight: bold !important; border-radius: 12px !important; 
    }
    
    /* BIAŁY PODGLĄD */
    .canvas-pro { 
        background: white !important; border-radius: 20px; padding: 40px; 
        color: black !important; min-height: 450px; display: flex; 
        flex-direction: column; justify-content: center; align-items: center; 
        border: 2px solid #e2e8f0; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BAZA TREŚCI ---
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

# --- 3. GENERATOR PDF (POPRAWIONY) ---
def create_pdf(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    fn = get_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in name_list:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(2)
        pdf.rect(7, 7, 285 if mode=='dyp' else 196, 198 if mode=='dyp' else 285)
        
        if mode == 'dyp':
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_y(85); pdf.cell(0, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 10, za_co, align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            if styl == "Kontur":
                pdf.set_text_color(255, 255, 255) # Białe wypełnienie
                # Renderowanie konturu poprzez rysowanie tekstu z przesunięciem (bezpieczna metoda)
                txt = name.upper()
                pdf.set_line_width(1)
                pdf.set_draw_color(r, g, b)
                # Używamy prostego renderingu - jeśli set_text_render_mode nie działa
                try:
                    pdf.set_text_render_mode(stroke=True, fill=False)
                except:
                    pdf.set_text_color(r, g, b) # fallback do pełnego jeśli biblioteka stara
            else:
                pdf.set_text_color(r, g, b)
            
            pdf.set_xy(0, 45)
            pdf.cell(210, 200, name.upper(), align='C')
            try:
                pdf.set_text_render_mode(stroke=False, fill=True) # Reset
            except:
                pass
            
    return bytes(pdf.output())

# --- 4. UI ---
st.title("✨ EduStudio Ultra 2026")

nav = st.sidebar.radio("Zadanie:", ["🔠 Wielkie Napisy", "📜 Dyplomy & AI"])

if nav == "🔠 Wielkie Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        txt_input = st.text_input("Hasło dekoracji:", "WITAJ")
        kol = st.color_picker("Wybierz kolor:", "#6366f1")
        styl_l = st.radio("Styl liter:", ["Pełny", "Kontur"])
        if st.button("GENERUJ PDF"):
            name_list = [c for c in txt_input if not c.isspace()]
            out = create_pdf('lit', name_list, kol, "", "", "", styl_l)
            st.download_button("📥 POBIERZ PDF", out, "napis.pdf")
    with c2:
        l = txt_input[0].upper() if txt_input else "?"
        if styl_l == "Kontur":
            st.markdown(f'<div class="canvas-pro"><h1 style="font-size:280px; -webkit-text-stroke: 4px {kol}; color: white; margin:0;">{l}</h1></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="canvas-pro"><h1 style="font-size:280px; color:{kol} !important; margin:0;">{l}</h1></div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Wybierz okazję:", list(KALENDARZ_PRO.keys()))
    if st.button("✨ AI: GENERUJ RYMOWANKĘ"):
        st.session_state.tresc_ai = KALENDARZ_PRO[okazja]
        st.balloons()
    
    c1, c2 = st.columns(2)
    with c1:
        imiona = st.text_area("Lista dzieci:", "Ania Nowak\nKuba Kowalski")
        final_tresc = st.text_area("Treść wyróżnienia:", value=st.session_state.get('tresc_ai', 'za wzorową postawę'))
    with c2:
        miejsc = st.text_input("Data:", "Warszawa, 2026")
        kol_d = st.color_picker("Kolor dyplomu:", "#f59e0b")
        if st.button("GENERUJ DYPLOMY"):
            name_list = [i.strip() for i in imiona.split('\n') if i.strip()]
            out_d = create_pdf('dyp', name_list, kol_d, final_tresc, miejsc, okazja[2:], "")
            st.download_button("📥 POBIERZ PACZKĘ PDF", out_d, "dyplomy.pdf")
            
    st.markdown(f'<div class="canvas-pro" style="border: 10px double {kol_d}"><h2 style="color:{kol_d} !important">{okazja.upper()}</h2><h1 style="color:{kol_d} !important">{imiona.split("\\n")[0]}</h1><p style="color:black !important">za {final_tresc}</p></div>', unsafe_allow_html=True)