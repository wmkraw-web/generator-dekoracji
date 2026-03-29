import streamlit as st
import os
from fpdf import FPDF
import pandas as pd

# --- KONFIGURACJA BIZNESOWA ---
st.set_page_config(page_title="EduStudio Biznes", layout="wide")

try:
    from fpdf import FPDF
except ImportError:
    st.error("Instalacja bibliotek... Odśwież stronę za chwilę.")
    st.stop()

# --- STYLIZACJA ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; color: #1e293b; }
    .main-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .stButton>button { background: #2563eb; color: white; border-radius: 8px; border: none; padding: 10px 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SILNIK PDF PRO (Z OBSŁUGĄ TŁA) ---
class DyplomEngine(FPDF):
    def add_background(self, image_path):
        if os.path.exists(image_path):
            # Wstawia tło na całą stronę A4
            self.image(image_path, 0, 0, 297, 210) 

def generate_business_pdf(u_list, tlo_path, tresc, data_miejsc, okazja, color_hex):
    pdf = DyplomEngine(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(False)
    
    # Konwersja koloru
    r, g, b = int(color_hex[1:3], 16), int(color_hex[3:5], 16), int(color_hex[5:7], 16)

    for student in u_list:
        pdf.add_page()
        # 1. Nakładamy tło graficzne
        pdf.add_background(tlo_path)
        
        # 2. Nakładamy tekst (Pozycje x,y musimy dobrać do tła)
        pdf.set_text_color(r, g, b)
        
        # Tytuł Okazji
        pdf.set_font("Helvetica", "B", 40)
        pdf.set_y(45)
        pdf.cell(297, 20, okazja.upper(), align='C', ln=1)
        
        # Imię i Nazwisko
        pdf.set_font("Helvetica", "B", 50)
        pdf.set_y(85)
        pdf.cell(297, 30, student.upper(), align='C', ln=1)
        
        # Treść / Rymowanka
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "", 20)
        pdf.set_y(125)
        pdf.set_left_margin(40)
        pdf.set_right_margin(40)
        pdf.multi_cell(217, 10, tresc, align='C')
        
        # Stopka
        pdf.set_left_margin(0)
        pdf.set_y(180)
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_x(30)
        pdf.cell(100, 10, data_miejsc)
        
    return bytes(pdf.output())

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("💼 EduStudio Pro: Panel Zarządzania")

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Ustawienia Projektu")
        okazja = st.selectbox("Wybór Szablonu (Okazja):", ["Pasowanie", "Dzień Kropki", "Dzień Dinozaura", "Inny"])
        
        # Symulacja wyboru tła (W wersji docelowej tu będą pliki z folderu assets)
        tlo_file = "assets/tlo_1.png" 
        
        color = st.color_picker("Kolor czcionki głównej:", "#1d4ed8")
        rymowanka = st.text_area("Treść dyplomu / Rymowanka:", "Za wielką odwagę, uśmiech od ucha do ucha i bycie wzorowym przedszkolakiem!")
        data_m = st.text_input("Miejscowość i data:", "Leżajsk, 2026")

    with col2:
        st.subheader("2. Zarządzanie Listą")
        input_mode = st.radio("Metoda wprowadzania:", ["Ręcznie", "Plik Excel/CSV"])
        
        if input_mode == "Ręcznie":
            studenci = st.text_area("Wpisz imiona (jedno pod drugim):", "Jan Kowalski\nAnna Nowak")
            lista_final = [s.strip() for s in studenci.split('\n') if s.strip()]
        else:
            uploaded_file = st.file_uploader("Wgraj plik z listą dzieci:", type=['xlsx', 'csv'])
            if uploaded_file:
                # Tu w przyszłości dodamy logikę odczytu Excela
                st.info("Plik wgrany poprawnie (funkcja odczytu w fazie Pro)")
                lista_final = ["Uczeń z pliku 1", "Uczeń z pliku 2"]
            else:
                lista_final = []

        if st.button("🚀 GENERUJ DYPLOMY PREMIUM"):
            if not os.path.exists(tlo_file):
                st.warning(f"Brak pliku tła: {tlo_file}. System wygeneruje dyplom bez tła graficznego.")
                # Fallback: pusta ścieżka
                tlo_file = ""
            
            with st.spinner("Tworzenie plików wysokiej jakości..."):
                pdf_bytes = generate_business_pdf(lista_final, tlo_file, rymowanka, data_m, okazja, color)
                st.download_button("📥 POBIERZ GOTOWY PAKIET", pdf_bytes, "dyplomy_premium.pdf")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- PODGLĄD WIZUALNY ---
st.markdown("### 👁️ Podgląd kompozycji")
st.info("W wersji biznesowej tutaj zobaczysz dokładny skład tekstu na wybranym tle graficznym.")