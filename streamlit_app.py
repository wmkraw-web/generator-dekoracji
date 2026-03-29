# --- SŁOWNIK OKAZJI ---
OKAZJE = {
    "Własna (wpisz ręcznie)": {"tekst": "", "kolor": "#000000"},
    "Pasowanie na Ucznia": {"tekst": "uroczyste ślubowanie i wstąpienie do grona społeczności szkolnej", "kolor": "#003366"},
    "Dzień Mamy i Taty": {"tekst": "ogromne serce, miłość i codzienne wsparcie", "kolor": "#E6007E"},
    "Zakończenie Roku": {"tekst": "bardzo dobre wyniki w nauce oraz wzorowe zachowanie", "kolor": "#D4AF37"},
    "Konkurs Recytatorski": {"tekst": "piękną interpretację utworów poetyckich i odwagę sceniczną", "kolor": "#228B22"},
    "Super Przedszkolak": {"tekst": "dzielne stawianie pierwszych kroków w przedszkolu i uśmiech każdego dnia", "kolor": "#FF8C00"}
}

# --- W INTERFEJSIE (zakładka Dyplomy) ---
with tab2:
    st.subheader("🏆 Kreator Dyplomów Tematycznych")
    
    # Wybór okazji
    wybrana_okazja = st.selectbox("Wybierz okazję:", list(OKAZJE.keys()))
    
    colA, colB = st.columns([1, 1])
    with colA:
        tryb = st.radio("Tryb wpisywania:", ["Jeden uczeń", "Lista uczniów"])
        if tryb == "Jeden uczeń":
            lista_imion = st.text_input("Imię i nazwisko:")
        else:
            lista_imion = st.text_area("Wklej listę (jedno pod drugim):")
    
    with colB:
        # Automatyczne podpowiadanie tekstu na podstawie okazji
        domyslny_tekst = OKAZJE[wybrana_okazja]["tekst"]
        d_za_co = st.text_area("Treść dyplomu (za co):", value=domyslny_tekst)
        
        d_data = st.text_input("Data i miejscowość:", "Kraków, 2026")
        
        # Automatyczny dobór koloru
        domyslny_kolor = OKAZJE[wybrana_okazja]["kolor"]
        d_kolor = st.color_picker("Kolor motywu:", value=domyslny_kolor)

    # Przycisk generowania (reszta funkcji pozostaje bez zmian)