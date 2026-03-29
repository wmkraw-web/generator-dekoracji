import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="MagicColor Studio PRO", layout="wide", page_icon="✨")

# Nowoczesny i czysty wygląd bez czarnych pól
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stApp { background-color: #0f172a; }
    
    /* Naprawa czarnych pól i kontenerów */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .canvas {
        background: white !important;
        border-radius: 15px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        padding: 40px;
        color: #1e293b;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid #e2e8f0;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

MOTYWY = {
    "🌟 Pasowanie": {"t": "DYPLOM PASOWANIA", "c": "#1e40af", "sub": "NA UCZNIA KLASY PIERWSZEJ", "icon": "🎓"},
    "🎓 Koniec Roku": {"t": "DYPLOM UZNANIA", "c": "#b45309", "sub": "ZA WYBITNE OSIĄGNIĘCIA", "icon": "🏆"},
    "🌸 Dzień Rodziców": {"t": "PODZIĘKOWANIE", "c": "#be185d", "sub": "DLA KOCHANYCH RODZICÓW", "icon": "❤️"},
    "🧸 Przedszkolak": {"t": "DYPLOM SUPER ZUCHA", "c": "#047857", "sub": "DLA DZIELNEGO PRZEDSZKOLAKA", "icon": "🎈"}
}

def setup_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_decorations(pdf, r, g, b):
    # Ozdobne narożniki
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(1.5)
    # GÓRA LEWO
    pdf.line(5, 5, 25, 5); pdf.line(5, 5, 5, 25)
    # GÓRA PRAWO
    pdf.line(272, 5, 292, 5); pdf.line(292, 5, 292, 25)
    # DÓŁ LEWO
    pdf.line(5, 185, 5, 205); pdf.line(5, 205, 25, 205)
    # DÓŁ PRAWO
    pdf.line(292, 185, 292, 205); pdf.line(272, 205, 292, 205)

def create_ultra_pdf(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = setup_font(pdf)
    r, g, b = int(data['col'][1:3], 16), int(data['col'][3:5], 16), int(data['col'][5:7], 16)

    for name in data['items']:
        pdf.add_page()
        draw_decorations(pdf, r, g, b)
        
        if mode == "litery":
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45)
            pdf.cell(210, 200, name.upper(), align='C')
        else:
            # NAGŁÓWEK
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=45)
            pdf.set_y(30)
            pdf.cell(0, 20, data['title'], align='C', ln=1)
            
            # PODTYTUŁ
            pdf.set_font(fn, size=18)
            pdf.cell(0, 10, data['sub'], align='C', ln=1)
            
            # IMIĘ
            pdf.set_y(85)
            pdf.set_font(fn, size=55)
            pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, name.upper(), align='C', ln=1)
            
            # TREŚĆ
            pdf.set_y(125)
            pdf.set_text_color(60, 60, 60)
            pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 12, f"za {data['za_co']}", align='C')
            
            # STOPKA
            pdf.set_y(180)
            pdf.set_font(fn, size=12)
            pdf.set_x(30)
            pdf.cell(100, 10, f"Data: {data['date']}", align='L')
            pdf.set_x(180)
            pdf.cell(100, 10, "Podpis: ............................", align='L')
            
    return bytes(pdf.output())

# --- UI ---
st.title("✨ MagicColor Studio PRO")
menu = st.sidebar.radio("NARZĘDZIE:", ["🔠 Napisy", "📜 Dyplomy"])

if menu == "🔠 Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        txt = st.text_input("Tekst napisu:", "WITAJ")
        kol = st.color_picker("Kolor:", "#6366f1")
        if st.button("GENERUJ PDF"):
            out = create_ultra_pdf("litery", {'items': [c for c in txt if not c.isspace()], 'col': kol, 'ori': 'P'})
            st.download_button("POBIERZ PLIK", out, "napisy.pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="canvas"><h1 style="font-size:300px; color:{kol};">{txt[0].upper() if txt else "?"}</h1></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c_o, c_i = st.columns(2)
    with c_o:
        wybor = st.selectbox("Styl okazji:", list(MOTYWY.keys()))
        t_za_co = st.text_area("Za co:", MOTYWY[wybor]["t"].lower())
    with c_i:
        t_imiona = st.text_area("Uczniowie:", "Jan Kowalski\nAnna Nowak")
        t_data = st.text_input("Data:", "Warszawa, 2026")
    st.markdown('</div>', unsafe_allow_html=True)

    c_b, c_p = st.columns([1, 2])
    with c_b:
        t_kol = st.color_picker("Kolor motywu:", MOTYWY[wybor]["c"])
        if st.button("GENERUJ DYPLOMY"):
            lista = [i.strip() for i in t_imiona.split('\n') if i.strip()]
            out_d = create_ultra_pdf("dyplomy", {'items': lista, 'col': t_kol, 'title': MOTYWY[wybor]["t"], 'sub': MOTYWY[wybor]["sub"], 'za_co': t_za_co, 'date': t_data, 'ori': 'L'})
            st.download_button("POBIERZ PACZKĘ", out_d, "dyplomy.pdf")
            
    with c_p:
        st.markdown(f"""
            <div class="canvas" style="border: 2px solid {t_kol};">
                <h3 style="color:{t_kol}; margin:0;">{MOTYWY[wybor]["t"]}</h3>
                <small>{MOTYWY[wybor]["sub"]}</small>
                <h1 style="color:{t_kol}; margin:40px 0;">{t_imiona.split('\\n')[0]}</h1>
                <p style="text-align:center; padding:0 20px;">za {t_za_co}</p>
            </div>
        """, unsafe_allow_html=True)