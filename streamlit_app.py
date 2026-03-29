import streamlit as st
from fpdf import FPDF
import os

# 1. Konfiguracja na samym początku
st.set_page_config(page_title="Generator Dekoracji", layout="centered")

def generuj_pdf(napis, styl, kolor_nazwa):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)
    
    # Czcionka - bezpieczne ładowanie
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        pdf.set_font("Roboto", "", 550) # Rozmiar idealny pod środek
    else:
        pdf.set_font("Helvetica", "B", 500)

    # Definicja kolorów
    kolory = {
        "Czarny": (0, 0, 0),
        "Niebieski": (0, 51, 102),
        "Zielony": (34, 139, 34),
        "Szary (do kolorowania)": (220, 220, 220)
    }
    r, g, b = kolory.get(kolor_nazwa, (0, 0, 0))

    for litera in napis.upper():
        if litera.isspace(): continue
        pdf.add_page()
        
        # Jeśli wybrano styl "Kontury", używamy jasnego szarego (bezpieczne!)
        if styl == "Tylko kontury (do kolorowania)":
            pdf.set_text_color(220, 220, 220)
        else:
            pdf.set_text_color(r, g, b)
        
        # Centrowanie - x=0, y=50 (obniżone, żeby nie uciekało w górę)
        pdf.set_xy(0, 55)
        pdf.cell(210, 200, litera, align='C')
        
    return bytes(pdf.output())

# --- INTERFEJS ---
st.title("🎨 Profesjonalny Generator Napisów")

col1, col2 = st.columns(2)
with col1:
    tekst = st.text_input("Wpisz hasło:", value="WITAJ")
with col2:
    wybrany_kolor = st.selectbox("Kolor:", ["Czarny", "Niebieski", "Zielony", "Szary (do kolorowania)"])

wybrany_styl = st.radio("Styl:", ["Pełny kolor", "Tylko kontury (do kolorowania)"], horizontal=True)

if tekst:
    try:
        pdf_wynik = generuj_pdf(tekst, wybrany_styl, wybrany_kolor)
        
        st.success(f"✅ Przygotowano {len(tekst.replace(' ',''))} stron(y).")
        
        st.download_button(
            label="📥 POBIERZ PDF (A4)",
            data=pdf_wynik,
            file_name=f"dekoracja_{tekst.lower()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Wystąpił błąd: {e}")

st.divider()
st.caption("Stabilna wersja 2.1")