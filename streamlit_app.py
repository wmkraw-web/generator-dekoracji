import streamlit as st
from fpdf import FPDF
import os

# --- 1. DESIGN & CONFIG ---
st.set_page_config(page_title="EduStudio Ultra 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: white !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e293b !important; border: 1px solid #334155 !important; padding: 25px !important; border-radius: 20px !important; }
    
    /* PŁÓTNO PODGLĄDU - PANCERNE */
    .canvas-pro { 
        background: white !important; border-radius: 20px; padding: 50px; 
        min-height: 500px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 3px solid #e2e8f0; 
        position: relative; box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }
    
    /* GŁÓWNA LITERA PODGLĄDU */
    .letter-preview {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 900;
        margin: 0;
        line-height: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BAZA TREŚCI AI ---
KALENDARZ_PRO = {
    "Pasowanie na Ucznia": "Dziś pasowanie, wielkie wydarzenie, przed Tobą nauka i marzeń spełnienie!",
    "Dzień Kropki": "Od małej kropki talent się zaczyna, każda kropka to Twoja wielka mina!",
    "Dzień Dinozaura": "Dinozaury wielkie były, przez wieki w ziemi kości skryły.",
    "Dzień Ziemi": "Ziemia to dom nasz jedyny, dbajmy o nią dla wspólnej rodziny."
}

# --- 3. GENERATOR PDF (TERAZ GENERUJE CAŁOŚĆ) ---
def create_pdf_pancerny(mode, items, col, za_co, data, tytul, styl):
    pdf = FPDF(orientation='L' if mode=='dyp' else 'P', unit='mm', format='A4')
    
    if os.path.exists("Roboto-Bold.ttf"):
        pdf.add_font("Roboto", "", "Roboto-Bold.ttf")
        fn = "Roboto"
    else:
        fn = "Helvetica"
        
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)

    # KLUCZOWE: Sprawdzamy, czy items nie jest puste
    if not items:
        return None

    for name in items:
        pdf.add_page()
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(2)
        
        if mode == 'dyp':
            # Dyplom Klasyczny
            pdf.rect(7, 7, 285, 198)
            pdf.set_text_color(r, g, b); pdf.set_font(fn, size=50)
            pdf.set_y(35); pdf.cell(0, 20, tytul.upper(), align='C', ln=1)
            pdf.set_font(fn, size=55); pdf.set_y(85); pdf.cell(0, 30, name.upper(), align='C', ln=1)
            pdf.set_y(125); pdf.set_text_color(50, 50, 50); pdf.set_font(fn, size=20)
            pdf.multi_cell(0, 10, za_co, align='C')
            pdf.set_y(178); pdf.set_font(fn, size=12); pdf.set_x(30); pdf.cell(0, 10, f"Data: {data}")
        else:
            # Litery ścienne
            pdf.rect(7, 7, 196, 285)
            pdf.set_font(fn, size=550 if fn == "Roboto" else 500)
            
            if styl == "Kontur":
                pdf.set_text_color(255, 255, 255) # Białe wypełnienie
                # Bezpieczne renderowanie konturu (nie wszystkie wersje fpdf2 to mają)
                try:
                    pdf.set_text_render_mode(stroke=True, fill=False)
                    pdf.set_line_width(1)
                    pdf.set_draw_color(r, g, b)
                except:
                    pdf.set_text_color(r, g, b) # Fallback do pełnego
            else:
                pdf.set_text_color(r, g, b)
            
            pdf.set_xy(0, 45)
            pdf.cell(210, 200, name.upper(), align='C')
            # Reset trybu renderowania
            try:
                pdf.set_text_render_mode(stroke=False, fill=True)
            except:
                pass
            
    return bytes(pdf.output())

# --- 4. INTERFEJS ---
st.title("✨ EduStudio Ultra v8.0")

# Pamięć sesji - zapobiega czyszczeniu formularza
if 'liter_txt' not in st.session_state: st.session_state['liter_txt'] = "WITAJ"
if 'dyp_imiona' not in st.session_state: st.session_state['dyp_imiona'] = "Ania Nowak\nKuba Kowalski"

nav = st.sidebar.radio("Zadanie:", ["🔠 Napisy", "📜 Dyplomy & AI"])

if nav == "🔠 Napisy":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("Konfiguracja")
        st.session_state['liter_txt'] = st.text_input("Hasło dekoracji:", value=st.session_state['liter_txt'])
        kol_l = st.color_picker("Wybierz kolor:", "#6366f1", key="color_nap")
        styl_l = st.radio("Styl liter:", ["Pełny", "Kontur"], key="styl_nap")
        
        # Przygotowanie danych do generowania PDF
        name_list = [c for c in st.session_state['liter_txt'] if not c.isspace()]
        
        # Generowanie PDF
        if st.button("GENERUJ PACZKĘ PDF"):
            if not name_list:
                st.warning("Najpierw wpisz hasło napisu!")
            else:
                with st.spinner(f"Generowanie PDF dla {len(name_list)} liter..."):
                    out_l = create_pdf_pancerny('lit', name_list, kol_l, "", "", "", styl_l)
                    if out_l:
                        st.download_button(f"📥 POBIERZ PACZKĘ ({len(name_list)})", out_l, "napisy.pdf")
    with c2:
        st.subheader("Podgląd kartki A4")
        pierwsza = st.session_state['liter_txt'][0].upper() if st.session_state['liter_txt'] else "?"
        
        # Dynamiczny podgląd konturu i koloru (CSS PRO)
        if styl_l == "Kontur":
            html_preview = f'<h1 class="letter-preview" style="font-size:350px; -webkit-text-stroke: 6px {kol_l}; color: white;">{pierwsza}</h1>'
        else:
            html_preview = f'<h1 class="letter-preview" style="font-size:350px; color:{kol_l};">{pierwsza}</h1>'
            
        st.markdown(f'<div class="canvas-pro">{html_preview}</div>', unsafe_allow_html=True)

else:
    st.subheader("Okazje")
    okazja = st.selectbox("Wybierz z kalendarza:", list(KALENDARZ_PRO.keys()))
    if st.button("✨ AI: GENERUJ RYMOWANKĘ"):
        st.session_state.tresc_ai_final = KALENDARZ_PRO[okazja]
        st.balloons()
    
    colA, colB = st.columns(2)
    with colA:
        st.session_state['dyp_imiona'] = st.text_area("Lista dzieci (jeden pod drugim):", value=st.session_state['dyp_imiona'])
        final_tresc = st.text_area("Za co:", value=st.session_state.get('tresc_ai_final', 'za wzorową postawę'))
    with colB:
        miejsc = st.text_input("Data:", "Leżajsk, 2026")
        kol_d = st.color_picker("Kolor dyplomu:", "#f59e0b", key="color_dyp")
        
        # Lista imion
        name_list_d = [i.strip() for i in st.session_state['dyp_imiona'].split('\n') if i.strip()]
        
        if st.button("GENERUJ WSZYSTKIE DYPLOMY"):
            if not name_list_d:
                st.warning("Wpisz imiona dzieci!")
            else:
                with st.spinner(f"Generowanie PDF dla {len(name_list_d)} dyplomów..."):
                    out_d = create_pdf_pancerny('dyp', name_list_d, kol_d, final_tresc, miejsc, okazja, "")
                    if out_d:
                        st.download_button(f"📥 POBIERZ PACZKĘ ({len(name_list_d)})", out_d, "dyplomy.pdf")
            
    st.markdown("### Podgląd projektu")
    p_imię = st.session_state['dyp_imiona'].split('\n')[0] if st.session_state['dyp_imiona'] else "Imię Nazwisko"
    st.markdown(f"""
        <div class="canvas-pro" style="border: 10px double {kol_d}">
            <h2 style="color:{kol_d}; margin:0;">{okazja.upper()}</h2>
            <p style="color:#555;">dla</p>
            <h1 style="color:{kolor_dyp}; margin:30px 0;">{p_imię}</h1>
            <p style="text-align:center; padding:0 30px; color:#1e293b;">za {final_tresc}</p>
        </div>
    """, unsafe_allow_html=True)