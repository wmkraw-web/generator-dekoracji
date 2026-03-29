import streamlit as st
import os
import random

# --- INTELIGENTNY IMPORT FPDF ---
try:
    from fpdf import FPDF
except ImportError:
    st.error("Błąd: Biblioteka FPDF nie została znaleziona. Upewnij się, że w pliku requirements.txt jest wpis: fpdf2")
    st.stop()

# --- KONFIGURACJA ---
st.set_page_config(page_title="EduStudio Master 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; padding: 30px !important; border-radius: 25px !important; }
    .canvas-pro { background: white !important; border-radius: 20px; padding: 40px; min-height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 4px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- BAZA ---
RYMOWANKI = {
    "Pasowanie na Ucznia": "Dzielny uczniu, ślubuj szczerze, w Twoją mądrość mocno wierzę!",
    "Dzień Kropki": "Mała kropka, wielka sprawa, to jest twórcza dziś zabawa!",
    "Dzień Dinozaura": "T-Rex, diplodok i inne gady, dają nam dzisiaj ważne rady!",
    "Dzień Ziemi": "Małe ręce, wielkie chęci, niech ekologia Cię zakręci!"
}

# --- GENERATOR PDF ---
def generate_pdf(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        if mode == 'dyp':
            pdf.set_line_width(2); pdf.rect(10, 10, 277, 190)
            pdf.set_text_color(r, g, b); pdf.set_font("Helvetica", 'B', size=45)
            pdf.set_y(40); pdf.cell(297, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font("Helvetica", 'B', size=55); pdf.set_y(85); pdf.cell(297, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font("Helvetica", size=20)
            pdf.multi_cell(297, 12, f"za {za_co}", align='C')
            pdf.set_y(175); pdf.set_font("Helvetica", size=12); pdf.set_x(30); pdf.cell(100, 10, f"Data: {data}")
        else:
            pdf.set_line_width(1.5); pdf.rect(8, 8, 194, 281)
            pdf.set_font("Helvetica", 'B', size=500)
            if styl == "Kontur":
                pdf.set_text_color(255, 255, 255); pdf.set_draw_color(r, g, b)
                pdf._out("1 Tr")
                pdf.set_y(50); pdf.cell(210, 210, name.upper(), align='C')
                pdf._out("0 Tr")
            else:
                pdf.set_text_color(r, g, b)
                pdf.set_y(50); pdf.cell(210, 210, name.upper(), align='C')
    return bytes(pdf.output())

# --- UI ---
if 'ai_text' not in st.session_state: st.session_state.ai_text = "Za wzorową postawę i uśmiech każdego dnia!"

st.title("🎓 EduStudio v9.3")
nav = st.sidebar.radio("Menu", ["Napisy", "Dyplomy"])

if nav == "Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        txt = st.text_input("Hasło:", "WITAJ")
        kol = st.color_picker("Kolor:", "#6366f1", key="k_nap")
        stl = st.radio("Styl:", ["Pełny", "Kontur"])
        if st.button("Generuj PDF"):
            out = generate_pdf('lit', [c for c in txt if not c.isspace()], kol, "", "", "", stl)
            st.download_button("Pobierz PDF", out, "napisy.pdf")
    with c2:
        char = txt[0].upper() if txt else "?"
        strk = f"-webkit-text-stroke: 4px {kol}; color: white;" if stl == "Kontur" else f"color: {kol};"
        st.markdown(f'<div class="canvas-pro"><h1 style="font-size:300px; {strk}">{char}</h1></div>', unsafe_allow_html=True)

else:
    okz = st.selectbox("Wybierz okazję:", list(RYMOWANKI.keys()))
    if st.button("✨ Generuj treść AI"):
        st.session_state.ai_text = RYMOWANKI[okz]
    
    colA, colB = st.columns(2)
    with colA:
        imiona = st.text_area("Lista dzieci:", "Jan Kowalski")
        tresc = st.text_area("Tekst dyplomu:", value=st.session_state.ai_text)
    with colB:
        dat = st.text_input("Data:", "Leżajsk, 2026")
        k_d = st.color_picker("Kolor:", "#f59e0b", key="k_dyp")
        if st.button("Generuj Dyplomy"):
            u_l = [i.strip() for i in imiona.split('\n') if i.strip()]
            out_d = generate_pdf('dyp', u_l, k_d, tresc, dat, okz, "")
            st.download_button("Pobierz dyplomy", out_d, "dyplomy.pdf")
            
    p_imie = imiona.split('\n')[0] if imiona else "Uczeń"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 10px double {k_d}">
            <h2 style="color:{k_d}">{okz.upper()}</h2>
            <h1 style="color:{k_d}; margin:20px 0;">{p_imie}</h1>
            <p style="color:black; text-align:center; padding:0 20px;">za {tresc}</p>
        </div>
    """, unsafe_allow_html=True)