import streamlit as st
from fpdf import FPDF
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="MagicColor Studio Ultra", layout="wide", page_icon="🎨")

# --- FORSOWANIE DESIGNU XXI WIEKU ---
st.markdown("""
    <style>
    /* Usuwanie szarych pól i ustawienie czystego tła */
    .stApp { background-color: #f1f5f9 !important; }
    
    /* Naprawa kontenerów - koniec z szarymi blokami */
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Nowoczesna karta edytora - biała, czysta, z cieniem */
    .editor-card {
        background: white !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) !important;
        border: 1px solid #e2e8f0 !important;
        color: #1e293b !important;
    }

    /* Płótno podglądu - centralny punkt */
    .canvas-pro {
        background: white !important;
        border-radius: 15px;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        padding: 40px;
        border: 2px solid #e2e8f0;
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }

    /* Przyciski Akcji */
    div.stButton > button {
        background: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover { background: #334155 !important; transform: translateY(-2px); }
    
    /* Przyciski Pobierania */
    div.stDownloadButton > button {
        background: #059669 !important;
        color: white !important;
        border-radius: 10px !important;
        width: 100% !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAZA OKAZJI ---
BAZA = {
    "🎓 Pasowanie": {"t": "DYPLOM PASOWANIA", "s": "NA UCZNIA KLASY PIERWSZEJ", "z": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej", "c": "#1e3a8a"},
    "🏆 Koniec Roku": {"t": "DYPLOM UZNANIA", "s": "ZA WYBITNE OSIĄGNIĘCIA", "z": "bardzo dobre wyniki w nauce oraz wzorowe zachowanie", "c": "#92400e"},
    "🌸 Dzień Rodziców": {"t": "PODZIĘKOWANIE", "s": "DLA KOCHANYCH RODZICÓW", "z": "ogromną miłość, wsparcie i codzienne starania", "c": "#9d174d"},
    "🧸 Dzień Misia": {"t": "PRZYJACIEL MISIA", "s": "CERTYFIKAT MIŁOŚNIKA PLUSZAKÓW", "z": "wspaniałą zabawę w Dniu Pluszowego Misia", "c": "#78350f"}
}

def get_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_pro_border(pdf, r, g, b):
    # Nowoczesna, minimalistyczna rama
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.5)
    pdf.rect(7, 7, 283, 196) # Cienka linia zewnętrzna
    pdf.set_line_width(2)
    # Akcenty narożne
    pdf.line(5, 5, 30, 5); pdf.line(5, 5, 5, 30) # GL
    pdf.line(267, 5, 292, 5); pdf.line(292, 5, 292, 30) # GP
    pdf.line(5, 177, 5, 202); pdf.line(5, 202, 30, 202) # DL
    pdf.line(292, 177, 292, 202); pdf.line(267, 202, 292, 202) # DP

def create_pdf(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = get_font(pdf)
    r, g, b = int(data['col'][1:3], 16), int(data['col'][3:5], 16), int(data['col'][5:7], 16)

    for item in data['items']:
        pdf.add_page()
        if mode == "dyplomy":
            draw_pro_border(pdf, r, g, b)
            # Treść
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50); pdf.set_y(35); pdf.cell(0, 20, data['title'], align='C', ln=1)
            pdf.set_font(fn, size=16); pdf.set_text_color(80, 80, 80); pdf.cell(0, 10, data['sub'], align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_text_color(r, g, b); pdf.set_y(85); pdf.cell(0, 30, item.upper(), align='C', ln=1)
            pdf.set_font(fn, size=22); pdf.set_text_color(40, 40, 40); pdf.set_y(125); pdf.multi_cell(0, 12, f"za {data['za_co']}", align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(25); pdf.cell(0, 10, f"Data: {data['date']}")
            pdf.set_x(180); pdf.cell(0, 10, "Podpis: ............................")
        else:
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=550); pdf.set_xy(0, 45); pdf.cell(210, 200, item.upper(), align='C')
    return bytes(pdf.output())

# --- UI ---
st.title("🎨 MagicColor Studio Ultra")

nav = st.sidebar.radio("FUNKCJA", ["Napisy A4", "Dyplomy"])

if nav == "Napisy A4":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="editor-card">', unsafe_allow_html=True)
        txt = st.text_input("Treść:", "WITAJ")
        kol = st.color_picker("Kolor:", "#4f46e5")
        if st.button("GENERUJ NAPIS"):
            out = create_pdf("litery", {'items': [c for c in txt if not c.isspace()], 'col': kol, 'ori': 'P'})
            st.download_button("POBIERZ PDF", out, "napis.pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="canvas-pro"><h1 style="font-size:250px; color:{kol}; margin:0;">{txt[0].upper() if txt else "?"}</h1></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="editor-card">', unsafe_allow_html=True)
    o1, o2, o3 = st.columns([1, 1, 1])
    with o1:
        wb = st.selectbox("Okazja:", list(BAZA.keys()))
        t_za = st.text_area("Za co:", BAZA[wb]["z"])
    with o2:
        t_im = st.text_area("Uczniowie:", "Jan Kowalski\nAnna Nowak")
        t_dt = st.text_input("Data:", "29.03.2026")
    with o3:
        t_kl = st.color_picker("Kolor:", BAZA[wb]["c"])
        if st.button("GENERUJ WSZYSTKIE"):
            lst = [i.strip() for i in t_im.split('\n') if i.strip()]
            out_d = create_pdf("dyplomy", {'items': lst, 'col': t_kl, 'title': BAZA[wb]["t"], 'sub': BAZA[wb]["s"], 'za_co': t_za, 'date': t_dt, 'ori': 'L'})
            st.download_button("POBIERZ DYPLOMY", out_d, "dyplomy.pdf")
    st.markdown('</div>', unsafe_allow_html=True)

    # Podgląd dyplomu bez szarych pól
    st.markdown(f"""
        <div class="canvas-pro" style="border-top: 5px solid {t_kl};">
            <h2 style="color:{t_kl}; margin:0;">{BAZA[wb]["t"]}</h2>
            <small style="color:#64748b;">{BAZA[wb]["sub"]}</small>
            <h1 style="color:{t_kl}; margin:30px 0;">{t_im.split('\\n')[0]}</h1>
            <p style="text-align:center; color:#334155;">za {t_za}</p>
        </div>
    """, unsafe_allow_html=True)