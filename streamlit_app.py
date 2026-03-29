import streamlit as st
from fpdf import FPDF
import os
import random

# --- CONFIG & MODERN THEME FORCING ---
st.set_page_config(page_title="EduMaster Studio v5.0", layout="wide", page_icon="✨")

# Brutalne wymuszenie jasnego motywu, aby usunąć czarne pola raz na zawsze
st.markdown("""
    <style>
    /* Globalne wymuszenie jasnych kolorów */
    .stApp { background-color: white !important; color: #1e293b !important; }
    h1, h2, h3, h4, h5, h6, p, label { color: #1e293b !important; }
    
    /* Naprawa kontenerów i tła */
    div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border: none !important;
    }
    
    /* Nowoczesny panel edytora */
    .editor-card {
        background: #f8fafc;
        border-radius: 24px;
        padding: 40px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
    }
    
    /* Płótno podglądu */
    .canvas {
        background: white !important;
        border-radius: 20px;
        padding: 50px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
        color: black;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Nowoczesne gradientowe przyciski */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        height: 3.5em !important;
        transition: 0.3s !important;
        width: 100% !important;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px rgba(99, 102, 241, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- BAZA OKAZJI (XXI WIEK) ---
# Tutaj integrujemy Kalendarz Przedszkolaka i Święta Nietypowe
BAZA_DYPLOMOW = {
    "Pasowanie na Ucznia": {"title": "DYPLOM PASOWANIA", "sub": "NA UCZNIA KLASY PIERWSZEJ", "text": "uroczyste ślubowanie i wstąpienie do grona szkolnej społeczności", "col": "#1e3a8a"},
    "Zakończenie Roku": {"title": "DYPLOM UZNANIA", "sub": "ZA WYBITNE OSIĄGNIĘCIA W NAUCE", "text": "bardzo dobre wyniki, wzorowe zachowanie i aktywny udział w życiu klasy", "col": "#b45309"},
    "Super Przedszkolak": {"title": "DYPLOM SUPER ZUCHA", "sub": "DLA DZIELNEGO PRZEDSZKOLAKA", "text": "dzielne stawianie pierwszych kroków w przedszkolu i uśmiech każdego dnia", "col": "#047857"},
    "🎂 Dzień Pluszowego Misia (25.11)": {"title": "DYPLOM MISIOWY", "sub": "PRZYJACIEL PLUSZOWEGO MISIA", "text": "udział w zabawach z okazji Dnia Pluszowego Misia i wielkie serce dla przytulanek", "col": "#854d0e"},
    "🌍 Dzień Ziemi (22.04)": {"title": "EKADYPLOM", "sub": "MŁODY STRAŻNIK PLANETY", "text": "udział w akcjach ekologicznych i dbanie o nasze środowisko każdego dnia", "col": "#15803d"},
    "💖 Dzień Rodziny": {"title": "PODZIĘKOWANIE", "sub": "DLA NAJWSPANIALSZYCH RODZICÓW", "text": "ogromną miłość, wsparcie, cierpliwość i codzienne starania", "col": "#be185d"},
    "📕 Konkurs Recytatorski": {"title": "DYPLOM LAUREATA", "sub": "ZA ZAJĘCIE ........... MIEJSCA", "text": "piękną interpretację utworów, odwagę sceniczną i dbałość o kulturę słowa", "col": "#1d4ed8"}
}

def load_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

# Funkcja rysująca subtelny wzór tła (XXI WIEK DESIGN)
def draw_bg_pattern(pdf, r, g, b):
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.1)
    for i in range(0, 300, 10):
        # Delikatne kropki w tle
        for j in range(0, 210, 10):
            if random.random() > 0.8: # Losowe rozmieszczenie
                pdf.ellipse(i, j, 0.5, 0.5, style='F')

def gen_master_pdf(mode, data_dict):
    pdf = FPDF(orientation=data_dict['ori'], unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)
    fn = load_font(pdf)
    r, g, b = int(data_dict['col'][1:3], 16), int(data_dict['col'][3:5], 16), int(data_dict['col'][5:7], 16)

    for item in data_dict['items']:
        pdf.add_page()
        if mode == "dyplomy":
            # Tło i Nowoczesna Ramka
            pdf.set_fill_color(r, g, b)
            pdf.set_alpha(0.03) # Bardzo jasny odcień koloru motywu
            draw_bg_pattern(pdf, r, g, b)
            pdf.set_alpha(1.0)
            
            # Nowoczesna rama narożnikowa (gruba)
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(2.5)
            # GL
            pdf.line(8, 8, 38, 8); pdf.line(8, 8, 8, 38)
            # GP
            pdf.line(259, 8, 289, 8); pdf.line(289, 8, 289, 38)
            # DL
            pdf.line(8, 162, 8, 192); pdf.line(8, 192, 38, 192)
            # DP
            pdf.line(289, 162, 289, 192); pdf.line(259, 192, 289, 192)
            
            # --- Hierarchia Tekstu ---
            # NAGŁÓWEK (PRO)
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=55)
            pdf.set_y(35); pdf.cell(0, 25, data_dict['title'], align='C', ln=1)
            
            # PODTYTUŁ (Lekki)
            pdf.set_font(fn, size=16)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 10, data_dict['sub'], align='C', ln=1)
            
            # IMIĘ (GIGANT)
            pdf.set_y(85)
            pdf.set_font(fn, size=60)
            pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, item.upper(), align='C', ln=1)
            
            # TREŚĆ (CZYTELNA)
            pdf.set_y(125); pdf.set_text_color(30, 30, 30)
            pdf.set_font(fn, size=22)
            pdf.multi_cell(0, 12, f"za {data_dict['za_co']}", align='C')
            
            # STOPKA (ELEGANCKA)
            pdf.set_y(178); pdf.set_font(fn, size=12)
            pdf.set_x(30); pdf.cell(100, 10, f"Miejscowość i data: {data_dict['date']}")
            pdf.set_x(175); pdf.cell(100, 10, "Podpis wychowawcy: ........................", align='L')
            
        else: # Tryb Liter A4
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, item.upper(), align='C')
            
    return bytes(pdf.output())

# --- INTERFEJS ---
st.title("✨ EduMaster Studio PRO")
st.caption("Profesjonalny kreator napisów i dyplomów XXI wieku")

sidebar = st.sidebar.radio("NARZĘDZIE:", ["Napisy ścienne A4", "Dyplomy dla całej klasy"])

if sidebar == "Napisy ścienne A4":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="editor-card">', unsafe_allow_html=True)
        txt = st.text_input("Hasło napisu:", "WITAJ")
        kol = st.color_picker("Kolor przewodni:", "#6366f1")
        if st.button("GENERUJ NAPIS"):
            pdf_n = gen_master_pdf("litery", {'items': [c for c in txt if not c.isspace()], 'col': kol, 'ori': 'P'})
            st.download_button("POBIERZ NAPIS", pdf_n, "napis.pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="canvas"><h1 style="font-size:300px; color:{kol};">{txt[0].upper() if txt else "?"}</h1></div>', unsafe_allow_html=True)

else: # Dyplomy
    st.markdown('<div class="editor-card">', unsafe_allow_html=True)
    o1, o2 = st.columns(2)
    with o1:
        wybor = st.selectbox("TEMAT OKAZJI:", list(BAZA_DYPLOMOW.keys()))
        t_za_co = st.text_area("TREŚĆ (za co):", value=BAZA_DYPLOMOW[wybor]["text"])
    with o2:
        t_imiona = st.text_area("LISTA UCZNIÓW (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        t_data = st.text_input("Miejscowość i data:", "Kraków, 2026")
    st.markdown('</div>', unsafe_allow_html=True)

    b1, p1 = st.columns([1, 2])
    with b1:
        t_kol = st.color_picker("DOSTOSUJ KOLOR:", BAZA_DYPLOMOW[wybor]["col"])
        if st.button("WYGENERUJ WSZYSTKIE DYPLOMY"):
            lista = [i.strip() for i in t_imiona.split('\n') if i.strip()]
            out_d = gen_master_pdf("dyplomy", {'items': lista, 'col': t_kol, 'title': BAZA_DYPLOMOW[wybor]["title"], 'sub': BAZA_DYPLOMOW[wybor]["sub"], 'za_co': t_za_co, 'date': t_data, 'ori': 'L'})
            st.download_button("POBIERZ PACZKĘ PDF", out_d, "dyplomy.pdf")
            st.success("Wygenerowano! Kliknij powyżej, aby zapisać plik.")
            
    with p1:
        p_imię = t_imiona.split('\n')[0]
        st.markdown(f"""
            <div class="canvas" style="border: 2px solid {t_kol}; color: black;">
                <h3 style="color:{t_kol}; margin-top:0;">{BAZA_DYPLOMOW[wybor]["title"]}</h3>
                <small style="color:#555;">{BAZA_DYPLOMOW[wybor]["sub"]}</small>
                <h1 style="color:{t_kol}; margin:40px 0;">{p_imię}</h1>
                <p style="text-align:center; color:#333;">za {t_za_co}</p>
            </div>
        """, unsafe_allow_html=True)