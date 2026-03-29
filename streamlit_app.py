import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA PREMIUM ---
st.set_page_config(page_title="EduStudio Ultra 2026", layout="wide")

# Forsowanie nowoczesnego wyglądu (Dark & Sleek)
st.markdown("""
    <style>
    /* Główny motyw - głęboki granat/antracyt */
    .stApp { background-color: #0f172a !important; }
    
    /* Wyraźne karty zamiast pustych pól */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    /* Wszystkie napisy w UI muszą być białe/jasne */
    h1, h2, h3, p, label, .stMarkdown { color: #f8fafc !important; }
    
    /* Naprawa pól tekstowych */
    input, textarea, select {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }

    /* Przyciski - Gradient Vivid */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        height: 3.5em !important;
    }
    
    /* Płótno podglądu - Kontrastowe */
    .preview-box {
        background: white !important;
        border-radius: 15px;
        padding: 30px;
        color: #0f172a !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KALENDARZ ŚWIĄT NIETYPOWYCH ---
KALENDARZ = {
    "✨ Pasowanie na Ucznia": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej",
    "🎨 Dzień Kropki (15.09)": "odkrywanie talentów, kreatywność i odwagę w tworzeniu",
    "🦕 Dzień Dinozaura": "zdobycie wiedzy o prehistorycznym świecie i pasję badacza",
    "🧸 Dzień Pluszowego Misia": "przyjaźń z pluszakami i udział w misiowych zabawach",
    "🌍 Dzień Ziemi": "postawę proekologiczną i dbanie o naszą planetę",
    "🍎 Dzień Edukacji": "trud włożony w naukę i wzorowe wypełnianie obowiązków",
    "🧩 Dzień Łamigłówek": "wybitne zdolności logiczne i determinację w rozwiązywaniu zadań"
}

def setup_pdf_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_diploma_decor(pdf, r, g, b):
    # Nowoczesne obramowanie geometryczne
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(1.5)
    pdf.rect(7, 7, 283, 196) # Główna rama
    pdf.set_line_width(0.3)
    pdf.rect(9, 9, 279, 192) # Wewnętrzna nitka
    
    # Narożniki PRO
    pdf.set_fill_color(r, g, b)
    pdf.rect(5, 5, 15, 15, 'F')   # GL
    pdf.rect(277, 5, 15, 15, 'F') # GP
    pdf.rect(5, 190, 15, 15, 'F') # DL
    pdf.rect(277, 190, 15, 15, 'F') # DP

def create_ultra_pdf(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = setup_pdf_font(pdf)
    r, g, b = int(data['col'][1:3], 16), int(data['col'][3:5], 16), int(data['col'][5:7], 16)

    for item in data['items']:
        pdf.add_page()
        if mode == "dyplom":
            draw_diploma_decor(pdf, r, g, b)
            # Tytuł
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, data['title'].upper(), align='C', ln=1)
            # Treść
            pdf.set_font(fn, size=20); pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 10, "otrzymuje", align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, item.upper(), align='C', ln=1)
            pdf.set_y(120); pdf.set_font(fn, size=24); pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 15, f"za {data['za_co']}", align='C')
            # Stopka
            pdf.set_y(178); pdf.set_font(fn, size=12)
            pdf.set_x(25); pdf.cell(0, 10, f"Data: {data['date']}")
            pdf.set_x(185); pdf.cell(0, 10, "Podpis: ..........................")
        else:
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, item.upper(), align='C')
    return bytes(pdf.output())

# --- INTERFEJS GŁÓWNY ---
st.title("🚀 EduStudio Ultra 2026")
st.markdown("### Profesjonalne Centrum Pomocy Dydaktycznych")

tab_n, tab_d = st.tabs(["🔠 Napisy A4", "🏆 Dyplomy Klasowe"])

with tab_n:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("⚙️ Konfiguracja")
        txt = st.text_input("Hasło napisu:", "WITAJ", key="n_input")
        n_kol = st.color_picker("Kolor liter:", "#6366f1")
        if st.button("GENERUJ NAPIS PDF"):
            pdf = create_ultra_pdf("napis", {'items': [c for c in txt if not c.isspace()], 'col': n_kol, 'ori': 'P'})
            st.download_button("📥 POBIERZ PLIK PDF", pdf, "napisy.pdf")
    with c2:
        st.subheader("👁️ Podgląd kartki")
        char = txt[0].upper() if txt else "?"
        st.markdown(f'<div class="preview-box"><h1 style="font-size:250px; color:{n_kol}; margin:0;">{char}</h1></div>', unsafe_allow_html=True)

with tab_d:
    okazja = st.selectbox("Wybierz okazję z kalendarza:", list(KALENDARZ.keys()))
    col1, col2 = st.columns([1, 1])
    with col1:
        imiona = st.text_area("Lista uczniów (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        d_za_co = st.text_area("Treść (za co):", value=KALENDARZ[okazja])
    with col2:
        d_data = st.text_input("Miejscowość i data:", "Leżajsk, 2026")
        d_kol = st.color_picker("Motyw kolorystyczny:", "#f59e0b")
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            lista = [i.strip() for i in imiona.split('\n') if i.strip()]
            pdf_d = create_ultra_pdf("dyplom", {'items': lista, 'col': d_kol, 'title': okazja[2:], 'za_co': d_za_co, 'date': d_data, 'ori': 'L'})
            st.download_button("📥 POBIERZ PACZKĘ PDF", pdf_d, "dyplomy.pdf")
    
    st.subheader("🖼️ Podgląd projektu")
    p_imię = imiona.split('\n')[0] if imiona else "Imię Nazwisko"
    st.markdown(f"""
        <div class="preview-box" style="border: 5px solid {d_kol}; color: #0f172a !important;">
            <h2 style="color:{d_kol} !important; margin:0;">{okazja[2:].upper()}</h2>
            <p style="color:#64748b !important;">dla</p>
            <h1 style="color:{d_kol} !important; margin:10px 0;">{p_imię}</h1>
            <p style="text-align:center; padding:0 30px; color:#1e293b !important;">za {d_za_co}</p>
        </div>
    """, unsafe_allow_html=True)