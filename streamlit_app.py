import streamlit as st
from fpdf import FPDF
import os

# --- 1. DESIGN ---
st.set_page_config(page_title="EduStudio PRO 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { 
        background-color: #161b22 !important; 
        border: 1px solid #30363d !important; 
        padding: 25px !important; 
        border-radius: 15px !important;
    }
    label, p, h1, h2, h3 { color: #e6edf3 !important; }
    
    /* BIAŁA KARTA PODGLĄDU */
    .preview-box { 
        background-color: white !important; 
        padding: 40px; 
        border-radius: 15px; 
        text-align: center; 
        min-height: 400px;
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    /* Tekst pomocniczy w podglądzie */
    .preview-label { color: #8b949e !important; font-size: 12px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BAZA OKAZJI ---
KALENDARZ = {
    "Pasowanie": "uroczyste ślubowanie i wstąpienie do społeczności szkolnej",
    "Dzień Kropki": "odkrywanie talentów, wielką kreatywność i odwagę",
    "Dzień Dinozaura": "zdobycie wiedzy o prehistorycznym świecie",
    "Dzień Misia": "przyjaźń z pluszakami i udział w misiowych zabawach",
    "Dzień Ziemi": "postawę proekologiczną i dbanie o naszą planetę",
    "Dzień Przedszkolaka": "radosne reprezentowanie grupy i bycie super kolegą"
}

def get_font(pdf):
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        return "Roboto"
    return "Helvetica"

# --- 3. GENERATOR PDF ---
def create_pdf(mode, items, col, za_co, data, tytul):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    fn = get_font(pdf)
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    for imie in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        # Solidna rama seryjna
        pdf.set_line_width(2)
        pdf.rect(7, 7, 285 if mode=='dyp' else 196, 198 if mode=='dyp' else 285)
        
        if mode == 'dyp':
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, size=55)
            pdf.set_y(85); pdf.cell(0, 30, imie.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(40, 40, 40)
            pdf.set_font(fn, size=22)
            pdf.multi_cell(0, 12, f"za {za_co}", align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            pdf.set_text_color(r, g, b)
            pdf.set_font(fn, size=500)
            pdf.set_xy(0, 50); pdf.cell(210, 200, imie.upper(), align='C')
    return bytes(pdf.output())

# --- 4. INTERFEJS ---
st.title("🍎 EduStudio PRO 2026")

menu = st.sidebar.radio("WYBIERZ NARZĘDZIE:", ["LITERY NA ŚCIANĘ", "DYPLOMY KLASOWE"])

if menu == "LITERY NA ŚCIANĘ":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("Ustawienia")
        napis = st.text_input("Treść hasła:", "WITAJ")
        kolor = st.color_picker("Kolor napisu:", "#4facfe")
        if st.button("GENERUJ NAPIS PDF"):
            res = create_pdf('lit', [c for c in napis if not c.isspace()], kolor, "", "", "")
            st.download_button("POBIERZ PLIK", res, "napis.pdf")
    with c2:
        pierwsza_litera = napis[0].upper() if napis else "?"
        st.markdown(f"""
            <div class="preview-box">
                <h1 style="font-size: 280px; color: {kolor} !important; margin: 0; line-height: 1;">
                    {pierwsza_litera}
                </h1>
                <p class="preview-label">Podgląd koloru na arkuszu A4</p>
            </div>
        """, unsafe_allow_html=True)

else:
    okazja = st.selectbox("Okazja z kalendarza:", list(KALENDARZ.keys()))
    c1, c2 = st.columns(2)
    with c1:
        lista_n = st.text_area("Lista uczniów (jeden pod drugim):", "Jan Kowalski\nAnna Nowak")
        za_co_n = st.text_area("Treść wyróżnienia:", value=KALENDARZ[okazja])
    with c2:
        data_n = st.text_input("Miejscowość i data:", "Leżajsk, 2026")
        kolor_d = st.color_picker("Kolor motywu dyplomu:", "#ffaa00")
        if st.button("WYGENERUJ WSZYSTKIE DYPLOMY"):
            u_lista = [i.strip() for i in lista_n.split('\n') if i.strip()]
            res_d = create_pdf('dyp', u_lista, kolor_d, za_co_n, data_n, okazja)
            st.download_button("POBIERZ PACZKĘ PDF", res_d, "dyplomy.pdf")
    
    st.markdown("### Podgląd pierwszej strony")
    p_imie = lista_n.split('\n')[0] if lista_n else "Imię Nazwisko"
    st.markdown(f"""
        <div class="preview-box" style="border: 12px double {kolor_d};">
            <h2 style="color: {kolor_d} !important; margin: 0;">{okazja.upper()}</h2>
            <p style="color: #666 !important; margin: 5px 0;">dla</p>
            <h1 style="color: {kolor_d} !important; margin: 10px 0;">{p_imie}</h1>
            <p style="color: #333 !important; font-size: 18px;">za {za_co_n}</p>
        </div>
    """, unsafe_allow_html=True)