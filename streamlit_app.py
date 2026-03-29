import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Generator Dekoracji")

st.title("🎨 Generator Liter A4")

text_input = st.text_input("Wpisz napis do druku:")

if text_input:
    pdf = FPDF()
    pdf.set_font("Helvetica", "B", 160)
    
    for char in text_input.upper():
        if char.isspace(): continue
        pdf.add_page()
        pdf.cell(0, 250, char, align='C')
    
    pdf_output = pdf.output()
    
    st.success("✅ Plik gotowy!")
    st.download_button(
        label="📥 Pobierz PDF",
        data=bytes(pdf_output),
        file_name="dekoracja.pdf",
        mime="application/pdf"
    )