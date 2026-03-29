import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA PREMIUM ---
st.set_page_config(page_title="MagicColor Studio v4.0", layout="wide", page_icon="✨")

# Nowoczesny Design (Glassmorphism & Modern UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* Główny kontener */
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    
    /* Karty edytora */
    .editor-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border_radius: 24px;
        padding: 30px;
        margin-bottom: 20px;
    }
    
    /* Przyciski w stylu Modern Apple/SaaS */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4) !important;
        filter: brightness(1.1);
    }

    /* Wygląd podglądu (Canvas) */
    .canvas-container {
        background: white !important;
        border-radius: 16px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        padding: 40px;
        color: #1e293b;
        position: relative;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Ukrycie nudnych elementów Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BAZA MOTYWÓW ---
MOTYWY = {
    "🌟 Pasowanie": {"t": "ŚLUBOWANIE", "c": "#6366f1", "desc": "uroczyste wstąpienie do grona uczniów"},
    "🎓 Koniec Roku": {"t": "GRATULACJE", "c": "#f59e0b", "desc": "wybitne osiągnięcia i wzorowe zachowanie"},
    "🌸 Dzień Rodziców": {"t": "PODZIĘKOWANIE", "c": "#ec4899", "desc": "ogromne serce i codzienne wsparcie"},
    "🧸 Przedszkolak": {"t": "DYPLOM", "c": "#10b981", "desc": "dzielne kroki w świecie przedszkola"}
}

def setup_font(pdf):
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

def create_pdf_final(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = setup_font(pdf)
    for name in data['items']:
        pdf.add_page()
        r, g, b = int(data['col'].lstrip('#')[:2], 16), int(data['col'].lstrip('#')[2:4], 16), int(data['col'].lstrip('#')[4:6], 16)
        if mode == "litery":
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550)
            pdf.set_xy(0, 45); pdf.cell(210, 200, name.upper(), align='C')
        else:
            pdf.set_draw_color(r, g, b); pdf.set_line_width(2); pdf.rect(10, 10, 277, 190)
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=60); pdf.set_y(40); pdf.cell(0, 20, data['title'], align='C', ln=1)
            pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20); pdf.cell(0, 15, "dla", align='C', ln=1)
            pdf.set_font(fn, size=45); pdf.set_text_color(r, g, b); pdf.cell(0, 25, name, align='C', ln=1)
            pdf.set_font(fn, size=22); pdf.set_text_color(70, 70, 70); pdf.set_y(125); pdf.multi_cell(0, 12, f"za {data['za_co']}", align='C')
            pdf.set_y(175); pdf.set_font(fn, size=12); pdf.set_x(25); pdf.cell(100, 10, f"Data: {data['date']}")
    return bytes(pdf.output())

# --- UI ---
st.title("✨ MagicColor Studio")
st.markdown("##### Nowoczesny kreator pomocy dydaktycznych")

menu = st.sidebar.radio("WYBIERZ NARZĘDZIE", ["🔠 Napisy ścienne", "📜 Generator Dyplomów"])

if menu == "🔠 Napisy ścienne":
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="editor-card">', unsafe_allow_html=True)
        txt = st.text_input("Treść napisu:", "WITAJ")
        kol = st.color_picker("Kolor przewodni:", "#6366f1")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("GENERUJ PLIK PDF"):
            out = create_pdf_final("litery", {'items': [c for c in txt if not c.isspace()], 'col': kol, 'ori': 'P'})
            st.download_button("POBIERZ GOTOWY PROJEKT", out, "napisy.pdf")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'<div class="canvas-container"><h1 style="font-size:300px; color:{kol}; margin:0;">{txt[0].upper() if txt else "?"}</h1><p style="color:#94a3b8">Podgląd strony A4</p></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="editor-card">', unsafe_allow_html=True)
    c_okazja, c_imiona = st.columns(2)
    with c_okazja:
        wybor = st.selectbox("Wybierz styl okazji:", list(MOTYWY.keys()))
        t_za_co = st.text_area("Treść wyróżnienia:", MOTYWY[wybor]["desc"])
    with c_imiona:
        t_imiona = st.text_area("Lista uczniów (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        t_data = st.text_input("Data i miejscowość:", "Warszawa, 2026")
    st.markdown('</div>', unsafe_allow_html=True)

    col_btn, col_pre = st.columns([1, 2])
    with col_btn:
        t_kolor = st.color_picker("Dostosuj kolor motywu:", MOTYWY[wybor]["c"])
        if st.button("WYGENERUJ WSZYSTKIE DYPLOMY"):
            lista = [i.strip() for i in t_imiona.split('\n') if i.strip()]
            out_d = create_pdf_final("dyplomy", {'items': lista, 'col': t_kolor, 'title': MOTYWY[wybor]["t"], 'za_co': t_za_co, 'date': t_data, 'ori': 'L'})
            st.download_button("POBIERZ PACZKĘ PDF", out_d, "dyplomy.pdf")
            
    with col_pre:
        imie_pre = t_imiona.split('\n')[0]
        st.markdown(f"""
            <div class="canvas-container" style="border: 8px double {t_kolor};">
                <h2 style="color:{t_kolor}; margin-top:0;">{MOTYWY[wybor]["t"]}</h2>
                <p style="font-size:14px; color:#64748b;">dla</p>
                <h1 style="color:{t_kolor}; margin:10px 0;">{imie_pre}</h1>
                <p style="font-size:18px; color:#334155; text-align:center; padding:0 40px;">za {t_za_co}</p>
                <div style="width:100%; display:flex; justify-content:space-between; margin-top:50px; font-size:12px; color:#94a3b8;">
                    <span>{t_data}</span><span>Podpis: ........................</span>
                </div>
            </div>
        """, unsafe_allow_html=True)