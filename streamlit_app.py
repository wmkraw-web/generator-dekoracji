import streamlit as st
from fpdf import FPDF
import os

# --- STYLE I KONFIGURACJA ---
st.set_page_config(page_title="MagicColor Educator PRO", layout="wide", page_icon="🎨")

# Custom CSS dla lepszego wyglądu
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

OKAZJE = {
    "🌟 Pasowanie na Ucznia": {"tekst": "uroczyste ślubowanie i wstąpienie do grona społeczności szkolnej", "kolor": "#003366", "symbol": "🎓"},
    "❤️ Dzień Mamy i Taty": {"tekst": "ogromne serce, miłość i codzienne wsparcie w każdej chwili", "kolor": "#E6007E", "symbol": "🌸"},
    "🏆 Zakończenie Roku": {"tekst": "bardzo dobre wyniki w nauce oraz wzorowe zachowanie w roku szkolnym", "kolor": "#D4AF37", "symbol": "🎖️"},
    "🎤 Konkurs Recytatorski": {"tekst": "piękną interpretację utworów poetyckich i odwagę sceniczną", "kolor": "#228B22", "symbol": "📜"},
    "🎈 Super Przedszkolak": {"tekst": "dzielne stawianie pierwszych kroków w przedszkolu i uśmiech każdego dnia", "kolor": "#FF8C00", "symbol": "🧸"}
}

def setup_font(pdf):
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

# --- FUNKCJE GENERUJĄCE ---
def draw_diploma_content(pdf, imie, za_co, data, kolor, font_name, symbol=""):
    r, g, b = int(kolor.lstrip('#')[:2], 16), int(kolor.lstrip('#')[2:4], 16), int(kolor.lstrip('#')[4:6], 16)
    pdf.add_page()
    
    # Podwójna ramka
    pdf.set_line_width(1.5)
    pdf.set_draw_color(r, g, b)
    pdf.rect(10, 10, 277, 190)
    pdf.set_line_width(0.5)
    pdf.rect(13, 13, 271, 184)

    # Nagłówek
    pdf.set_text_color(r, g, b)
    pdf.set_font(font_name, size=60)
    pdf.set_y(35)
    pdf.cell(0, 25, "DYPLOM", align='C', ln=1)
    
    # Symbol
    pdf.set_font("Helvetica", size=40) # Standard dla emoji/symboli
    pdf.cell(0, 20, symbol, align='C', ln=1)

    # Treść
    pdf.set_text_color(40, 40, 40)
    pdf.set_font(font_name, size=20)
    pdf.cell(0, 15, "dla", align='C', ln=1)
    
    pdf.set_font(font_name, size=45)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 25, imie, align='C', ln=1)
    
    pdf.set_text_color(60, 60, 60)
    pdf.set_font(font_name, size=22)
    pdf.set_y(125)
    pdf.multi_cell(0, 12, f"za {za_co}", align='C')
    
    # Stopka
    pdf.set_y(175)
    pdf.set_font(font_name, size=12)
    pdf.set_x(25)
    pdf.cell(100, 10, f"Data: {data}", align='L')
    pdf.set_x(170)
    pdf.cell(100, 10, "Podpis wychowawcy: ........................", align='L')

# --- INTERFEJS ---
st.title("🚀 MagicColor Educator PRO")

tab1, tab2 = st.tabs(["🔠 Wielkie Napisy A4", "📜 Kreator Dyplomów"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("⚙️ Ustawienia")
        napis_txt = st.text_input("Hasło dekoracji:", "WITAJ")
        napis_kolor = st.color_picker("Kolor główny:", "#FF4B4B")
        napis_styl = st.selectbox("Wariant:", ["Pełny", "Kontur (oszczędny)"])
        gen_btn = st.button("Przygotuj Napis")
    
    with col2:
        st.subheader("👁️ Podgląd kartki")
        # Tu tworzymy wizualną symulację strony A4 w Streamlit
        st.markdown(f"""
            <div style="border: 2px solid #ddd; background: white; height: 400px; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <h1 style="font-size: 200px; color: {napis_kolor}; margin: 0; font-family: sans-serif;">
                    {napis_txt[0] if napis_txt else "?"}
                </h1>
            </div>
            <p style="text-align: center; color: gray;">(Podgląd pierwszej litery)</p>
        """, unsafe_allow_html=True)

with tab2:
    col_cfg, col_pre = st.columns([1, 1])
    
    with col_cfg:
        st.subheader("🖋️ Dane Dyplomu")
        okazja_sel = st.selectbox("Wybierz motyw:", list(OKAZJE.keys()))
        
        d_imie = st.text_input("Imię i nazwisko (lub lista):", "Jan Kowalski")
        d_za_co = st.text_area("Treść wyróżnienia:", value=OKAZJE[okazja_sel]["tekst"])
        
        c_a, c_b = st.columns(2)
        with c_a: d_data = st.text_input("Data:", "29 marca 2026")
        with c_b: d_kolor = st.color_picker("Kolor motywu:", OKAZJE[okazja_sel]["kolor"])
        
        d_btn = st.button("Wygeneruj Dyplomy")

    with col_pre:
        st.subheader("🖼️ Podgląd dyplomu")
        st.markdown(f"""
            <div style="border: 5px double {d_kolor}; padding: 20px; background: white; text-align: center; border-radius: 10px;">
                <h4 style="color: {d_kolor}; margin-bottom: 0;">DYPLOM</h4>
                <p style="font-size: 10px;">dla</p>
                <h2 style="color: {d_kolor}; margin: 10px 0;">{d_imie.split('\\n')[0]}</h2>
                <p style="font-size: 14px; color: #444;">za {d_za_co}</p>
                <br>
                <div style="display: flex; justify-content: space-between; font-size: 10px;">
                    <span>Data: {d_data}</span>
                    <span>........................<br>Podpis</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- LOGIKA PDF ---
if d_btn:
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    f_name = setup_font(pdf)
    imiona = d_imie.split('\n')
    for imie in imiona:
        if imie.strip():
            draw_diploma_content(pdf, imie.strip(), d_za_co, d_data, d_kolor, f_name, OKAZJE[okazja_sel]["symbol"])
    
    st.success("✨ Dyplomy wygenerowane pomyślnie!")
    st.download_button("📥 POBIERZ PACZKĘ PDF", bytes(pdf.output()), "dyplomy_pro.pdf")