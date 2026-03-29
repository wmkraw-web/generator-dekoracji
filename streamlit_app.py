import streamlit as st
from fpdf import FPDF
import os

# --- 1. DESIGN & CONFIG ---
st.set_page_config(page_title="EduStudio Ultra 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; padding: 25px !important; border-radius: 20px !important; }
    .canvas-pro { 
        background: white !important; border-radius: 20px; padding: 50px; 
        min-height: 500px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 3px solid #e2e8f0; 
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BAZA TREŚCI ---
KALENDARZ_PRO = {
    "Pasowanie na Ucznia": "Dziś pasowanie, wielkie wydarzenie, przed Tobą nauka i marzeń spełnienie!",
    "Dzień Kropki": "Od małej kropki talent się zaczyna, każda kropka to Twoja wielka mina!",
    "Dzień Dinozaura": "Dinozaury wielkie były, przez wieki w ziemi kości skryły.",
    "Dzień Ziemi": "Ziemia to dom nasz jedyny, dbajmy o nią dla wspólnej rodziny."
}

# --- 3. GENERATOR PDF (METODA PANCERNEGO KONTURU) ---
def create_pdf_final(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    fn = "Helvetica" # Używamy standardowej dla max stabilności
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(2)
        
        if mode == 'dyp':
            pdf.rect(7, 7, 285, 198)
            pdf.set_text_color(r, g, b); pdf.set_font(fn, 'B', size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, 'B', size=55); pdf.set_y(85); pdf.cell(0, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 10, za_co, align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            pdf.rect(7, 7, 196, 285)
            pdf.set_font(fn, 'B', size=500)
            txt = name.upper()
            
            if styl == "Kontur":
                # RĘCZNE RYSOWANIE KONTURU (offset method)
                pdf.set_text_color(r, g, b)
                off = 0.5 # Grubość "obramowania"
                # Rysujemy 4 razy przesunięty tekst w kolorze
                pdf.text(35-off, 240, txt)
                pdf.text(35+off, 240, txt)
                pdf.text(35, 240-off, txt)
                pdf.text(35, 240+off, txt)
                # Na koniec biały środek
                pdf.set_text_color(255, 255, 255)
                pdf.text(35, 240, txt)
            else:
                pdf.set_text_color(r, g, b)
                pdf.text(35, 240, txt)
            
    return bytes(pdf.output())

# --- 4. UI ---
st.title("✨ EduStudio Ultra v8.1")

if 'liter_txt' not in st.session_state: st.session_state['liter_txt'] = "WITAJ"
if 'dyp_imiona' not in st.session_state: st.session_state['dyp_imiona'] = "Ania Nowak"

nav = st.sidebar.radio("Zadanie:", ["🔠 Napisy", "📜 Dyplomy & AI"])

if nav == "🔠 Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.session_state['liter_txt'] = st.text_input("Hasło:", value=st.session_state['liter_txt'])
        kol_l = st.color_picker("Kolor:", "#6366f1")
        styl_l = st.radio("Styl:", ["Pełny", "Kontur"])
        
        name_list = [c for c in st.session_state['liter_txt'] if not c.isspace()]
        if st.button("GENERUJ PDF"):
            if name_list:
                out_l = create_pdf_final('lit', name_list, kol_l, "", "", "", styl_l)
                st.download_button(f"📥 POBIERZ PDF", out_l, "napisy.pdf")
    with c2:
        pierwsza = st.session_state['liter_txt'][0].upper() if st.session_state['liter_txt'] else "?"
        if styl_l == "Kontur":
            html = f'<h1 style="font-size:350px; -webkit-text-stroke: 6px {kol_l}; color: white;">{pierwsza}</h1>'
        else:
            html = f'<h1 style="font-size:350px; color:{kol_l};">{pierwsza}</h1>'
        st.markdown(f'<div class="canvas-pro">{html}</div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Okazja:", list(KALENDARZ_PRO.keys()))
    if st.button("✨ AI: GENERUJ RYMOWANKĘ"):
        st.session_state.tresc_ai_final = KALENDARZ_PRO[okazja]
    
    colA, colB = st.columns(2)
    with colA:
        st.session_state['dyp_imiona'] = st.text_area("Lista dzieci:", value=st.session_state['dyp_imiona'])
        final_tresc = st.text_area("Za co:", value=st.session_state.get('tresc_ai_final', 'za wzorową postawę'))
    with colB:
        miejsc = st.text_input("Data:", "Leżajsk, 2026")
        kol_d = st.color_picker("Kolor:", "#f59e0b")
        name_list_d = [i.strip() for i in st.session_state['dyp_imiona'].split('\n') if i.strip()]
        if st.button("GENERUJ DYPLOMY"):
            out_d = create_pdf_final('dyp', name_list_d, kol_d, final_tresc, miejsc, okazja, "")
            st.download_button("📥 POBIERZ PDF", out_d, "dyplomy.pdf")
            
    p_imie = st.session_state['dyp_imiona'].split('\n')[0] if st.session_state['dyp_imiona'] else "Uczeń"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 10px double {kol_d}">
            <h2 style="color:{kol_d}">{okazja.upper()}</h2>
            <h1 style="color:{kol_d}; margin:30px 0;">{p_imie}</h1>
            <p style="color:black">za {final_tresc}</p>
        </div>
    """, unsafe_allow_html=True)