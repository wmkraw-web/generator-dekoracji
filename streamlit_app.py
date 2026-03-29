import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="MagicColor Studio PRO", layout="wide")

# FORSOWANIE WYGLĄDU - Usuwanie czarnych pól i naprawa kolorów
st.markdown("""
    <style>
    /* Usuwanie tła z kontenerów Streamlit */
    .stApp { background-color: #0f172a !important; }
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stExpander"] { background: rgba(255,255,255,0.05) !important; border: none !important; }
    
    /* Nowoczesna karta edytora */
    .editor-pane {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Stylizacja przycisków */
    div.stButton > button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 3.5em !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }

    /* Płótno podglądu */
    .preview-canvas {
        background: white !important;
        border-radius: 20px;
        padding: 40px;
        color: #1e293b;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

MOTYWY = {
    "🌟 Pasowanie": {"t": "DYPLOM PASOWANIA", "s": "NA UCZNIA KLASY PIERWSZEJ", "c": "#1e40af"},
    "🎓 Koniec Roku": {"t": "ŚWIADECTWO ZNAKOMITOŚCI", "s": "ZA WYBITNE OSIĄGNIĘCIA", "c": "#b45309"},
    "❤️ Dzień Rodziców": {"t": "PODZIĘKOWANIE", "s": "DLA KOCHANYCH RODZICÓW", "c": "#be185d"},
    "🧸 Przedszkolak": {"t": "DYPLOM SUPER ZUCHA", "s": "DLA DZIELNEGO PRZEDSZKOLAKA", "c": "#047857"}
}

def setup_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_modern_frame(pdf, r, g, b):
    # Nowoczesna rama geometryczna
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(1)
    # Cienkie linie pomocnicze
    pdf.line(15, 15, 282, 15)
    pdf.line(15, 182, 282, 182)
    # Grube narożniki dekoracyjne
    pdf.set_line_width(3)
    # GL
    pdf.line(10, 10, 40, 10); pdf.line(10, 10, 10, 40)
    # GP
    pdf.line(257, 10, 287, 10); pdf.line(287, 10, 287, 40)
    # DL
    pdf.line(10, 160, 10, 190); pdf.line(10, 190, 40, 190)
    # DP
    pdf.line(287, 160, 287, 190); pdf.line(257, 190, 287, 190)

def create_premium_pdf(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = setup_font(pdf)
    r, g, b = int(data['col'][1:3], 16), int(data['col'][3:5], 16), int(data['col'][5:7], 16)

    for name in data['items']:
        pdf.add_page()
        if mode == "dyplomy":
            draw_modern_frame(pdf, r, g, b)
            # Tytuł
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, data['title'], align='C', ln=1)
            # Podtytuł
            pdf.set_font(fn, size=16)
            pdf.cell(0, 10, data['sub'], align='C', ln=1)
            # Imię
            pdf.set_y(80)
            pdf.set_font(fn, size=60)
            pdf.cell(0, 30, name.upper(), align='C', ln=1)
            # Za co
            pdf.set_y(120); pdf.set_text_color(40, 40, 40)
            pdf.set_font(fn, size=22)
            pdf.multi_cell(0, 12, f"za {data['za_co']}", align='C')
            # Data/Podpis
            pdf.set_y(175); pdf.set_font(fn, size=12)
            pdf.set_x(30); pdf.cell(100, 10, f"Data: {data['date']}", align='L')
            pdf.set_x(170); pdf.cell(100, 10, "Podpis wychowawcy: .....................", align='L')
        else:
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, name.upper(), align='C')
            
    return bytes(pdf.output())

# --- INTERFEJS ---
st.title("✨ MagicColor Studio PRO")

sidebar = st.sidebar.radio("NARZĘDZIE", ["Napisy A4", "Dyplomy"])

if sidebar == "Napisy A4":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="editor-pane">', unsafe_allow_html=True)
        txt = st.text_input("Hasło:", "WITAJ")
        kol = st.color_picker("Kolor:", "#6366f1")
        if st.button("GENERUJ PDF"):
            out = create_premium_pdf("litery", {'items': [c for c in txt if not c.isspace()], 'col': kol, 'ori': 'P'})
            st.download_button("POBIERZ PLIK", out, "napisy.pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="preview-canvas"><h1 style="font-size:300px; color:{kol};">{txt[0].upper() if txt else "?"}</h1></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="editor-pane">', unsafe_allow_html=True)
    o1, o2 = st.columns(2)
    with o1:
        wybor = st.selectbox("Wybierz okazję:", list(MOTYWY.keys()))
        t_za_co = st.text_area("Treść (za co):", value=MOTYWY[wybor]["t"].lower())
    with o2:
        t_imiona = st.text_area("Uczniowie (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        t_data = st.text_input("Data:", "Warszawa, 2026")
    st.markdown('</div>', unsafe_allow_html=True)

    b1, p1 = st.columns([1, 2])
    with b1:
        t_kol = st.color_picker("Kolor motywu:", MOTYWY[wybor]["c"])
        if st.button("WYGENERUJ WSZYSTKIE"):
            lista = [i.strip() for i in t_imiona.split('\n') if i.strip()]
            out_d = create_premium_pdf("dyplomy", {'items': lista, 'col': t_kol, 'title': MOTYWY[wybor]["t"], 'sub': MOTYWY[wybor]["s"], 'za_co': t_za_co, 'date': t_data, 'ori': 'L'})
            st.download_button("POBIERZ PACZKĘ PDF", out_d, "dyplomy.pdf")
    with p1:
        st.markdown(f"""
            <div class="preview-canvas" style="border: 4px solid {t_kol};">
                <h2 style="color:{t_kol}; margin:0;">{MOTYWY[wybor]["t"]}</h2>
                <h1 style="color:{t_kol}; margin:40px 0;">{t_imiona.split('\\n')[0]}</h1>
                <p style="text-align:center;">za {t_za_co}</p>
            </div>
        """, unsafe_allow_html=True)