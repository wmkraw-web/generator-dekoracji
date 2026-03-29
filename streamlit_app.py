import streamlit as st
from fpdf import FPDF
import os

# --- KONFIGURACJA EKSTRA ---
st.set_page_config(page_title="EduStudio PRO 2026", layout="wide")

# TOTALNA BLOKADA STYLI (Fix dla szarych pól i niewidocznych tekstów)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; }
    
    /* Naprawa tych nieszczęsnych bloków Streamlit */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }

    /* Wszystkie etykiety i teksty UI */
    label, p, span, h1, h2, h3 { color: #e6edf3 !important; font-family: 'Segoe UI', sans-serif !important; }
    
    /* PRZYCISKI - Nowoczesny look */
    div.stButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 3em !important;
        border-radius: 10px !important;
    }

    /* PŁÓTNO PODGLĄDU - Musi być białe i wyraźne */
    .canvas-container {
        background-color: #ffffff !important;
        border-radius: 20px;
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Tekst wewnątrz białego podglądu MA BYĆ CZARNY */
    .canvas-container h1, .canvas-container h2, .canvas-container p {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAZA OKAZJI (KALENDARZ PRZEDSZKOLAKA) ---
KALENDARZ = {
    "✨ Pasowanie na Ucznia": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej",
    "🔵 Dzień Kropki (15.09)": "odkrywanie talentów, wielką kreatywność i odwagę",
    "🦖 Dzień Dinozaura": "zdobycie wiedzy o prehistorycznym świecie i pasję odkrywcy",
    "🧸 Dzień Pluszowego Misia": "przyjaźń z pluszakami i udział w misiowych zabawach",
    "🌍 Dzień Ziemi": "postawę proekologiczną i dbanie o naszą wspólną planetę",
    "🧩 Dzień Łamigłówek": "wybitne zdolności logiczne i determinację w działaniu",
    "🎖️ Dzień Przedszkolaka": "radosne reprezentowanie grupy i bycie super kolegą/koleżanką"
}

def get_pdf_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

def draw_border_2026(pdf, r, g, b):
    pdf.set_draw_color(r, g, b)
    # Potrójna rama (Styl PRO)
    pdf.set_line_width(2)
    pdf.rect(6, 6, 285, 198)
    pdf.set_line_width(0.3)
    pdf.rect(8, 8, 281, 194)
    pdf.set_line_width(0.8)
    pdf.rect(9, 9, 279, 192)

def create_pdf(mode, data):
    pdf = FPDF(orientation=data['ori'], unit='mm', format='A4')
    fn = get_pdf_font(pdf)
    r, g, b = int(data['col'][1:3], 16), int(data['col'][3:5], 16), int(data['col'][5:7], 16)

    for item in data['items']:
        pdf.add_page()
        if mode == "dyplom":
            draw_border_2026(pdf, r, g, b)
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, data['title'].upper(), align='C', ln=1)
            pdf.set_font(fn, size=18); pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 10, "otrzymuje", align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_text_color(r, g, b)
            pdf.cell(0, 30, item.upper(), align='C', ln=1)
            pdf.set_y(120); pdf.set_font(fn, size=22); pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 12, f"za {data['za_co']}", align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12)
            pdf.set_x(25); pdf.cell(0, 10, f"Data: {data['date']}")
            pdf.set_x(180); pdf.cell(0, 10, "Podpis: ............................")
        else:
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            pdf.set_xy(0, 45); pdf.cell(210, 200, item.upper(), align='C')
    return bytes(pdf.output())

# --- MAIN UI ---
st.title("🍎 EduStudio Ultra PRO 2026")

side = st.sidebar.radio("NARZĘDZIE", ["Litery ścienne", "Dyplomy seryjne"])

if side == "Litery ścienne":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("⚙️ Konfiguracja")
        lit_txt = st.text_input("Wpisz hasło:", "WITAJ")
        lit_kol = st.color_picker("Wybierz kolor:", "#1f6feb")
        if st.button("GENERUJ PDF Z NAPISAMI"):
            p = create_pdf("lit", {'items': [c for c in lit_txt if not c.isspace()], 'col': lit_kol, 'ori': 'P'})
            st.download_button("📥 POBIERZ NAPIS", p, "napisy.pdf")
    with c2:
        char = lit_txt[0].upper() if lit_txt else "?"
        st.markdown(f'<div class="canvas-container"><h1 style="font-size:300px; color:{lit_kol}; margin:0;">{char}</h1><p>Podgląd strony A4</p></div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Wybierz okazję (Kalendarz Świąt):", list(KALENDARZ.keys()))
    col1, col2 = st.columns([1, 1])
    with col1:
        lista = st.text_area("Lista uczniów (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        tresc = st.text_area("Treść (za co):", value=KALENDARZ[okazja])
    with col2:
        data_miasto = st.text_input("Data i miasto:", "Leżajsk, 2026")
        kolor_dyp = st.color_picker("Kolor motywu:", "#f59e0b")
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            lst = [i.strip() for i in lista.split('\n') if i.strip()]
            p_dyp = create_pdf("dyplom", {'items': lst, 'col': kolor_dyp, 'title': okazja[2:], 'za_co': tresc, 'date': data_miasto, 'ori': 'L'})
            st.download_button("📥 POBIERZ PACZKĘ PDF", p_dyp, "dyplomy_klasowe.pdf")
    
    st.markdown("### 👁️ Podgląd projektu")
    p_imie = lista.split('\n')[0] if lista else "Imię Nazwisko"
    st.markdown(f"""
        <div class="canvas-container" style="border: 10px double {kolor_dyp};">
            <h2 style="color:{kolor_dyp} !important;">{okazja[2:].upper()}</h2>
            <p>dla</p>
            <h1 style="color:{kolor_dyp} !important;">{p_imie}</h1>
            <p style="text-align:center; padding: 0 40px;">za {tresc}</p>
        </div>
    """, unsafe_allow_html=True)