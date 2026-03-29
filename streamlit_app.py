import streamlit as st
from fpdf import FPDF
import os
import random

# --- KONFIGURACJA I STYLIZACJA ---
st.set_page_config(page_title="EduStudio Master 2026", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; padding: 30px !important; border-radius: 25px !important; }
    
    .canvas-pro { 
        background: white !important; border-radius: 20px; padding: 40px; 
        min-height: 550px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 4px solid #e2e8f0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .stButton > button { 
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important; 
        color: white !important; font-weight: bold !important; border-radius: 12px !important;
        border: none !important; transition: 0.3s;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- BAZA WIEDZY AI (RYMOWANKI) ---
RYMOWANKI = {
    "Pasowanie na Ucznia": "Dzielny uczniu, ślubuj szczerze, w Twoją mądrość mocno wierzę! Niech nauka radość niesie, w każdym dniu i w każdym lesie.",
    "Dzień Kropki": "Mała kropka, wielka sprawa, to jest twórcza dziś zabawa! Odkryj talent, który drzemie, Ty podbijesz całą ziemię.",
    "Dzień Dinozaura": "T-Rex, diplodok i inne gady, dają nam dzisiaj ważne rady: Bądź odważny, badaj świat, jak odkrywca z dawnych lat!",
    "Dzień Ziemi": "Małe ręce, wielkie chęci, niech ekologia Cię zakręci! Za dbanie o drzewa i czystą wodę, dostajesz dziś od nas wielką nagrodę.",
    "Super Przedszkolak": "Uśmiech od ucha do samego ucha, to jest cecha super zucha! Za zabawę i dzielność w grupie, jesteś dziś w honorowej trupie.",
    "Dzień Misia": "Misiu puszysty, misiu brązowy, do przytulania zawsze gotowy. Za wielkie serce dla przytulanki, przyjmij te nasze radosne rymowanki!"
}

# --- FUNKCJE POMOCNICZE ---
def get_pdf_font(pdf):
    # Próba załadowania profesjonalnej czcionki z polskimi znakami
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        return "Roboto"
    return "Helvetica"

def draw_background_pattern(pdf, r, g, b, mode):
    # Subtelne kropki w tle (wygląda pro)
    pdf.set_draw_color(r, g, b)
    pdf.set_fill_color(r, g, b)
    max_x = 297 if mode == 'L' else 210
    max_y = 210 if mode == 'L' else 297
    for _ in range(30):
        pdf.set_alpha(0.1)
        pdf.circle(random.randint(5, max_x-5), random.randint(5, max_y-5), 0.3, 'F')
    pdf.set_alpha(1.0)

# --- GŁÓWNY SILNIK PDF ---
def generate_master_pdf(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    
    fn = get_pdf_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for name in items:
        pdf.add_page()
        draw_background_pattern(pdf, r, g, b, pdf.cur_orientation)
        
        pdf.set_draw_color(r, g, b)
        if mode == 'dyp':
            # DYPLOM POZIOMY
            pdf.set_line_width(2); pdf.rect(10, 10, 277, 190) 
            pdf.set_line_width(0.5); pdf.rect(12, 12, 273, 186)
            
            # Treść dyplomu
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50 if fn=="Roboto" else 45)
            pdf.set_y(35); pdf.cell(297, 20, tytul.upper(), align='C', ln=1)
            
            pdf.set_text_color(100, 100, 100); pdf.set_font(fn, size=20)
            pdf.set_y(60); pdf.cell(297, 10, "otrzymuje", align='C', ln=1)
            
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=55)
            pdf.set_y(80); pdf.cell(297, 30, name.upper(), align='C', ln=1)
            
            pdf.set_y(120); pdf.set_text_color(40, 40, 40); pdf.set_font(fn, size=22)
            pdf.set_left_margin(35); pdf.set_right_margin(35)
            pdf.multi_cell(227, 12, za_co, align='C')
            
            pdf.set_left_margin(0); pdf.set_y(175); pdf.set_font(fn, size=14)
            pdf.set_x(25); pdf.cell(100, 10, f"Data: {data}")
            pdf.set_x(180); pdf.cell(100, 10, "Podpis: ............................", align='R')
        else:
            # NAPIS PIONOWY
            pdf.set_line_width(1.5); pdf.rect(8, 8, 194, 281)
            pdf.set_font(fn, size=550 if fn=="Roboto" else 500)
            if styl == "Kontur":
                pdf.set_text_color(255, 255, 255)
                pdf.set_draw_color(r, g, b); pdf.set_line_width(1.5)
                pdf._out("1 Tr") # Tryb konturu
                pdf.set_y(50); pdf.cell(210, 210, name.upper(), align='C')
                pdf._out("0 Tr")
            else:
                pdf.set_text_color(r, g, b)
                pdf.set_y(50); pdf.cell(210, 210, name.upper(), align='C')
            
    return bytes(pdf.output())

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("✨ EduStudio Master 2026")
st.sidebar.title("🛠️ Narzędzia")
narzedzie = st.sidebar.radio("Co robimy?", ["Napisy ścienne", "Generator Dyplomów"])

if 'napis_txt' not in st.session_state: st.session_state.napis_txt = "WITAJ"
if 'uczniowie_txt' not in st.session_state: st.session_state.uczniowie_txt = "Jan Kowalski\nAnna Nowak"

if narzedzie == "Napisy ścienne":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.session_state.napis_txt = st.text_input("Treść napisu:", value=st.session_state.napis_txt)
        k_n = st.color_picker("Kolor napisu:", "#6366f1")
        s_n = st.radio("Styl liter:", ["Pełny", "Kontur"])
        if st.button("GENERUJ NAPISY"):
            list_l = [c for c in st.session_state.napis_txt if not c.isspace()]
            out = generate_master_pdf('lit', list_l, k_n, "", "", "", s_n)
            st.download_button("📥 Pobierz plik PDF", out, "napisy_edustudio.pdf")
    with c2:
        lit = st.session_state.napis_txt[0].upper() if st.session_state.napis_txt else "?"
        stroke = f"-webkit-text-stroke: 6px {k_n}; color: white;" if s_n == "Kontur" else f"color: {k_n};"
        st.markdown(f'<div class="canvas-pro"><h1 style="font-size:380px; {stroke} margin:0; font-family: Arial;">{lit}</h1></div>', unsafe_allow_html=True)

else:
    okazja = st.selectbox("Wybierz okazję z kalendarza:", list(RYMOWANKI.keys()))
    if st.button("✨ GENERUJ RYMOWANKĘ AI"):
        st.session_state.ai_text = RYMOWANKI[okazja]
        st.balloons()
        
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.uczniowie_txt = st.text_area("Lista uczniów:", value=st.session_state.uczniowie_txt)
        tresc_d = st.text_area("Treść dyplomu (edytuj jeśli chcesz):", value=st.session_state.get('ai_text', 'za wzorowe zachowanie'))
    with c2:
        m_d = st.text_input("Miejscowość i data:", "Leżajsk, 2026")
        k_d = st.color_picker("Kolor przewodni:", "#f59e0b")
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            u_lista = [i.strip() for i in st.session_state.uczniowie_txt.split('\n') if i.strip()]
            out_d = generate_master_pdf('dyp', u_lista, k_d, tresc_d, m_d, okazja, "")
            st.download_button("📥 Pobierz paczkę dyplomów", out_d, "dyplomy_edustudio.pdf")
            
    st.markdown("### 👁️ Podgląd pierwszej strony")
    p_im = st.session_state.uczniowie_txt.split('\n')[0] if st.session_state.uczniowie_txt else "Uczeń"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 12px double {k_d}">
            <h2 style="color:{k_d}; margin:0;">{okazja.upper()}</h2>
            <p style="color:#666; margin:5px 0;">otrzymuje</p>
            <h1 style="color:{k_d}; margin:15px 0;">{p_im}</h1>
            <p style="color:#333; font-size:20px; text-align:center; padding:0 40px;">{tresc_d}</p>
        </div>
    """, unsafe_allow_html=True)