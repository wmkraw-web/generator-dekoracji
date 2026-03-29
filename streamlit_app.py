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

KALENDARZ_PRO = {
    "Pasowanie na Ucznia": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej",
    "Dzień Kropki": "odkrywanie talentów, wielką kreatywność i odwagę",
    "Dzień Dinozaura": "zdobycie wiedzy o prehistorycznym świecie",
    "Dzień Ziemi": "postawę proekologiczną i dbanie o naszą planetę"
}

# --- GENERATOR PDF (FINAL GEOMETRY) ---
def create_pdf_v86(mode, items, col, za_co, data, tytul, styl):
    # Wymuszamy brak marginesów automatycznych, żeby ramka była idealna
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    
    fn = "Helvetica"
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        
        if mode == 'dyp':
            # DYPLOM POZIOMY (A4: 297x210mm)
            # Ramka zewnętrzna (równe odstępy 10mm od krawędzi)
            pdf.set_line_width(2)
            pdf.rect(10, 10, 277, 190) 
            # Ramka wewnętrzna (cienka)
            pdf.set_line_width(0.5)
            pdf.rect(13, 13, 271, 184)
            
            # Tytuł
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, 'B', size=48)
            pdf.set_y(35)
            pdf.cell(297, 20, tytul.upper(), align='C', ln=1)
            
            # Napis "dla"
            pdf.set_text_color(80, 80, 80)
            pdf.set_font(fn, size=20)
            pdf.set_y(60)
            pdf.cell(297, 15, "dla", align='C', ln=1)
            
            # Imię (GIGANT)
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, 'B', size=55)
            pdf.set_y(85)
            pdf.cell(297, 30, name.upper(), align='C', ln=1)
            
            # Treść
            pdf.set_y(125)
            pdf.set_text_color(50, 50, 50)
            pdf.set_font(fn, size=22)
            pdf.set_left_margin(30) # Margines dla tekstu wieloliniowego
            pdf.set_right_margin(30)
            pdf.multi_cell(237, 12, f"za {za_co}", align='C')
            
            # Reset marginesów dla stopki
            pdf.set_left_margin(0)
            pdf.set_y(175)
            pdf.set_font(fn, size=14)
            pdf.set_text_color(r, g, b)
            # Data po lewej, Podpis po prawej (wyliczone pozycje)
            pdf.set_x(25)
            pdf.cell(100, 10, f"Data: {data}", align='L')
            pdf.set_x(172)
            pdf.cell(100, 10, "Podpis: ..........................", align='R')
            
        else:
            # NAPIS PIONOWY (A4: 210x297mm)
            pdf.set_line_width(1.5)
            pdf.rect(7, 7, 196, 283) # Ramka napisu
            
            pdf.set_font(fn, 'B', size=550)
            txt = name.upper()
            
            if styl == "Kontur":
                pdf.set_text_color(255, 255, 255)
                pdf.set_draw_color(r, g, b)
                pdf.set_line_width(1.5)
                pdf._out("1 Tr") # Tryb konturu
                pdf.set_y(50)
                pdf.cell(210, 210, txt, align='C')
                pdf._out("0 Tr") # Powrót do wypełnienia
            else:
                pdf.set_text_color(r, g, b)
                pdf.set_y(50)
                pdf.cell(210, 210, txt, align='C')
            
    return bytes(pdf.output())

# --- UI ---
st.title("🚀 EduStudio Ultra v8.6")

if 'liter_txt' not in st.session_state: st.session_state['liter_txt'] = "WITAJ"
if 'dyp_imiona' not in st.session_state: st.session_state['dyp_imiona'] = "JAN KOWALSKI"

nav = st.sidebar.radio("Zadanie:", ["🔠 Napisy", "📜 Dyplomy & AI"])

if nav == "🔠 Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.session_state['liter_txt'] = st.text_input("Hasło:", value=st.session_state['liter_txt'])
        kol_l = st.color_picker("Kolor:", "#6366f1")
        styl_l = st.radio("Styl:", ["Pełny", "Kontur"])
        if st.button("GENERUJ NAPIS"):
            name_list = [c for c in st.session_state['liter_txt'] if not c.isspace()]
            out_n = create_pdf_v86('lit', name_list, kol_l, "", "", "", styl_l)
            st.download_button("📥 POBIERZ PDF", out_n, "napisy.pdf")
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
        st.session_state['dyp_imiona'] = st.text_area("Uczniowie:", value=st.session_state['dyp_imiona'])
        final_tresc = st.text_area("Za co:", value=st.session_state.get('tresc_ai_final', 'za wzorową postawę'))
    with colB:
        miejsc = st.text_input("Data i miasto:", "Leżajsk, 2026")
        kol_d = st.color_picker("Kolor:", "#f59e0b")
        if st.button("GENERUJ DYPLOMY"):
            u_list = [i.strip() for i in st.session_state['dyp_imiona'].split('\n') if i.strip()]
            out_d = create_pdf_v86('dyp', u_list, kol_d, final_tresc, miejsc, okazja, "")
            st.download_button("📥 POBIERZ PDF", out_d, "dyplomy.pdf")
            
    p_imie = st.session_state['dyp_imiona'].split('\n')[0] if st.session_state['dyp_imiona'] else "Uczeń"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 10px double {kol_d}">
            <h2 style="color:{kol_d}; margin:0;">{okazja.upper()}</h2>
            <p style="color:#666; margin:0;">dla</p>
            <h1 style="color:{kol_d}; margin:15px 0;">{p_imie}</h1>
            <p style="color:black; font-size:18px; text-align:center;">za {final_tresc}</p>
        </div>
    """, unsafe_allow_html=True)