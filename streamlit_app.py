import streamlit as st
import os

try:
    from fpdf import FPDF
    st.success("✅ SILNIK PDF DZIAŁA!")
except Exception as e:
    st.error(f"❌ BŁĄD SILNIKA: {e}")

st.title("TEST POŁĄCZENIA v10.1")
st.write("Jeśli widzisz ten napis, to znaczy, że pokonaliśmy serwer.")

tekst = st.text_input("Wpisz cokolwiek:", "DZIAŁA")
if st.button("TESTUJ GENEROWANIE"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=50)
    pdf.cell(200, 100, txt=tekst, ln=1, align='C')
    out = bytes(pdf.output())
    st.download_button("POBIERZ TEST", out, "test.pdf")