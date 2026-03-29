import streamlit as st
import os
import random

# --- 1. PANCERNY IMPORT I SETUP ---
try:
    from fpdf import FPDF
except ImportError:
    st.error("🔄 Inicjalizacja silnika graficznego... Odśwież stronę za 30 sekund.")
    st.stop()

st.set_page_config(page_title="EduStudio v10 Pro", layout="wide", page_icon="🎓")

# Stylizacja "Dark Luxury"
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    [data-testid="stVerticalBlockBorderWrapper"] { 
        background-color: #1e293b; 
        border: 1px solid #334155; 
        border-radius: 20px; 
        padding: 2rem;
    }
    .preview-card {
        background: white;
        border-radius: 15px;
        padding: 40px;
        color: #0f172a;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELIGENTNA BAZA WIEDZY ---
RYMOWANKI = {
    "Pasowanie na Ucznia": "Dziś ślubowanie, wielka sprawa, przed Tobą wiedza i mądra zabawa! Zostań chlubą naszej szkoły.",
    "Dzień Kropki": "Od małej kropki świat się zaczyna, każda Twą pasją jest dziś, chłopcze i dziewczyno!",
    "Dzień Dinozaura": "Odkrywaj świat jak wielki badacz, o prehistorii pięknie opowiadaj!",
    "Dzień Ziemi": "Dbasz o przyrodę, wodę i drzewa, za to Ci dzisiaj podziękować trzeba!",
    "Dzień Misia": "Przyjaciel dzieci, miś pluszowy, do przytulania zawsze gotowy!",
    "Własna treść": "Wpisz poniżej swoje własne wyróżnienie..."
}

# --- 3. PRO SILNIK GENEROWANIA ---
def create_pro_pdf(mode, data):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    
    # Obsługa kolorów
    c = data['color']
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    
    for item in data['items']:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        
        if mode == 'dyp':
            # DYPLOM DESIGN
            pdf.set_line_width(2); pdf.rect(10, 10, 277, 190)
            pdf.set_line_width(0.5); pdf.rect(12, 12, 273, 186)
            
            pdf.set_text_color(r, g, b); pdf.set_font("Helvetica", "B", 45)
            pdf.set_y(35); pdf.cell(297, 20, data['okazja'].upper(), align='C', ln=1)
            
            pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", "", 20)
            pdf.cell(297, 10, "otrzymuje", align='C', ln=1)
            
            pdf.set_text_color(r, g, b); pdf.set_font("Helvetica", "B", 55)
            pdf.set_y(80); pdf.cell(297, 30, item.upper(), align='C', ln=1)
            
            pdf.set_y(120); pdf.set_text_color(40, 40, 40); pdf.set_font("Helvetica", "", 22)
            pdf.set_left_margin(30); pdf.set_right_margin(30)
            pdf.multi_cell(237, 12, data['tresc'], align='C')
            
            pdf.set_left_margin(0); pdf.set_y(175); pdf.set_font("Helvetica", "", 14)
            pdf.set_x(25); pdf.cell(100, 10, f"Data: {data['data']}")
            pdf.set_x(172); pdf.cell(100, 10, "Podpis: ..........................", align='R')
        else:
            # NAPIS DESIGN
            pdf.set_line_width(1.5); pdf.rect(8, 8, 194, 281)
            pdf.set_font("Helvetica", "B", 550)
            if data['styl'] == "Kontur":
                pdf.set_text_color(255, 255, 255)
                pdf._out("1 Tr"); pdf.set_line_width(1.5)
                pdf.set_y(50); pdf.cell(210, 210, item.upper(), align='C')
                pdf._out("0 Tr")
            else:
                pdf.set_text_color(r, g, b)
                pdf.set_y(50); pdf.cell(210, 210, item.upper(), align='C')
                
    return bytes(pdf.output())

# --- 4. INTERFEJS ---
st.title("🚀 EduStudio v10 Pro")

if 'rym' not in st.session_state: st.session_state.rym = RYMOWANKI["Pasowanie na Ucznia"]

tab1, tab2 = st.tabs(["🔠 Napisy Ścienne", "📜 Generator Dyplomów"])

with tab1:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        n_txt = st.text_input("Treść napisu:", "WITAJ")
        n_col = st.color_picker("Kolor liter:", "#6366f1", key="c_lit")
        n_stl = st.radio("Styl:", ["Pełny", "Kontur"], key="s_lit")
        if st.button("GENERUJ PAKIET NAPISÓW"):
            pdf_bytes = create_pro_pdf('lit', {'items': [c for c in n_txt if not c.isspace()], 'color': n_col, 'styl': n_stl})
            st.download_button("📥 Pobierz PDF", pdf_bytes, "napisy.pdf")
    with c2:
        char = n_txt[0].upper() if n_txt else "?"
        stroke = f"-webkit-text-stroke: 6px {n_col}; color: white;" if n_stl == "Kontur" else f"color: {n_col};"
        st.markdown(f'<div class="preview-card"><h1 style="font-size:380px; {stroke}">{char}</h1></div>', unsafe_allow_html=True)

with tab2:
    okz = st.selectbox("Okazja:", list(RYMOWANKI.keys()))
    if st.button("✨ GENERUJ RYMOWANKĘ AI"):
        st.session_state.rym = RYMOWANKI[okz]
    
    ca, cb = st.columns(2)
    with ca:
        u_list = st.text_area("Lista uczniów:", "Jan Kowalski\nAnna Nowak")
        d_rym = st.text_area("Treść wyróżnienia:", value=st.session_state.rym)
    with cb:
        d_dat = st.text_input("Miejscowość i data:", "Leżajsk, 2026")
        d_col = st.color_picker("Kolor dyplomu:", "#f59e0b", key="c_dyp")
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            u_items = [i.strip() for i in u_list.split('\n') if i.strip()]
            pdf_dyp = create_pro_pdf('dyp', {'items': u_items, 'color': d_col, 'okazja': okz, 'tresc': d_rym, 'data': d_dat})
            st.download_button("📥 Pobierz paczkę", pdf_dyp, "dyplomy.pdf")
            
    p_im = u_list.split('\n')[0] if u_list else "Uczeń"
    st.markdown(f"""
        <div class="preview-card" style="border: 12px double {d_col}">
            <h2 style="color:{d_col}">{okz.upper()}</h2>
            <p style="color:#666">otrzymuje</p>
            <h1 style="color:{d_col}; margin:20px 0;">{p_im}</h1>
            <p style="color:black; text-align:center; padding:0 30px;">{d_rym}</p>
        </div>
    """, unsafe_allow_html=True)