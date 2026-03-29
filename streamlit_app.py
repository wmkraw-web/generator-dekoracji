import streamlit as st
from fpdf import FPDF
import os

# --- STYLE ---
st.set_page_config(page_title="EduStudio Ultra 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; padding: 25px !important; border-radius: 20px !important; }
    .canvas-pro { 
        background: white !important; border-radius: 20px; padding: 50px; 
        min-height: 500px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 3px solid #e2e8f0; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- REJESTR OKAZJI ---
KALENDARZ_PRO = {
    "Pasowanie na Ucznia": "Dziś pasowanie, wielkie wydarzenie, przed Tobą nauka i marzeń spełnienie!",
    "Dzień Kropki": "Od małej kropki talent się zaczyna, każda kropka to Twoja wielka mina!",
    "Dzień Dinozaura": "Dinozaury wielkie były, przez wieki w ziemi kości skryły.",
    "Dzień Ziemi": "Ziemia to dom nasz jedyny, dbajmy o nią dla wspólnej rodziny."
}

# --- GENERATOR PDF (VECTOR MODE) ---
def create_pdf_vector(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    # Używamy Helvetica (standardowa), by uniknąć problemów z ładowaniem fontów
    fn = "Helvetica"
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        
        if mode == 'dyp':
            pdf.set_line_width(2); pdf.rect(7, 7, 285, 198)
            pdf.set_text_color(r, g, b); pdf.set_font(fn, 'B', size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, 'B', size=55); pdf.set_y(85); pdf.cell(0, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 10, za_co, align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            pdf.set_line_width(1.5); pdf.rect(7, 7, 196, 285)
            txt = name.upper()
            
            # Parametry napisu
            pdf.set_font(fn, 'B', size=500)
            pdf.set_y(50)
            
            if styl == "Kontur":
                # METODA WEKTOROWA (Najbezpieczniejsza na świecie)
                pdf.set_line_width(1.5)
                # Ustawiamy przezroczyste wypełnienie i kolorowy obrys
                # Składnia: 'D' oznacza tylko obrys (Draw)
                pdf.set_text_color(r, g, b) # fallback
                try:
                    # Rysujemy tekst jako kontur (render mode 1 to standard PDF)
                    with pdf.local_context(text_render_mode=1, draw_color=(r, g, b), line_width=1):
                        pdf.cell(190, 210, txt, align='C')
                except:
                    # Jeśli local_context nie zadziała (stara wersja), rysujemy cell
                    pdf.cell(190, 210, txt, align='C')
            else:
                pdf.set_text_color(r, g, b)
                pdf.cell(190, 210, txt, align='C')
            
    return bytes(pdf.output())

# --- UI ---
st.title("🚀 EduStudio Ultra v8.3")

if 'liter_txt' not in st.session_state: st.session_state['liter_txt'] = "WITAJ"
if 'dyp_imiona' not in st.session_state: st.session_state['dyp_imiona'] = "Jan Kowalski"

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
                out_l = create_pdf_vector('lit', name_list, kol_l, "", "", "", styl_l)
                st.download_button(f"📥 POBIERZ PDF", out_l, "napisy.pdf")
    with c2:
        pierwsza = st.session_state['liter_txt'][0].upper() if st.session_state['liter_txt'] else "?"
        stroke = f"-webkit-text-stroke: 6px {kol_l}; color: white;" if styl_l == "Kontur" else f"color: {kol_l};"
        st.markdown(f'<div class="canvas-pro"><h1 style="font-size:350px; {stroke} margin:0; font-family: Arial;">{pierwsza}</h1></div>', unsafe_allow_html=True)

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
            out_d = create_pdf_vector('dyp', name_list_d, kol_d, final_tresc, miejsc, okazja, "")
            st.download_button("📥 POBIERZ PDF", out_d, "dyplomy.pdf")
            
    p_imie = st.session_state['dyp_imiona'].split('\n')[0] if st.session_state['dyp_imiona'] else "Uczeń"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 10px double {kol_d}">
            <h2 style="color:{kol_d}; font-family: Arial;">{okazja.upper()}</h2>
            <h1 style="color:{kol_d}; margin:30px 0; font-family: Arial;">{p_imie}</h1>
            <p style="color:black; font-family: Arial;">za {final_tresc}</p>
        </div>
    """, unsafe_allow_html=True)