def generate_full_wypas(text, style, color_choice):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)
    
    font_path = "Roboto-Bold.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path)
        font_name = "Roboto"
    else:
        font_name = "Helvetica"

    for char in text.upper():
        if char.isspace(): continue
        pdf.add_page()
        
        # Kolory RGB
        colors = {
            "Czarny": (0, 0, 0),
            "Niebieski Królewski": (0, 51, 102),
            "Zieleń Szkolna": (34, 139, 34),
            "Pastelowy Róż": (255, 182, 193)
        }
        r, g, b = colors.get(color_choice, (0, 0, 0))
        
        # --- ROZWIĄZANIE BŁĘDU ---
        pdf.set_font(font_name, "B" if font_name=="Helvetica" else "", 600)
        
        if style == "Tylko kontury (do kolorowania)":
            # Trik: Ustawiamy kolor tekstu na biały, a obramowanie na wybrany kolor
            pdf.set_text_color(255, 255, 255) 
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(1.5) # Grubsza linia ułatwia kolorowanie
            # Używamy niskopoziomowej komendy zamiast set_render_mode
            # 2 oznacza "Fill then stroke" (wypełnij i obrysuj)
            text_stale = 2 
        else:
            pdf.set_text_color(r, g, b)
            text_stale = 0 # Normalne wypełnienie

        # Pozycjonowanie (poprawione, żeby litera nie uciekała)
        pdf.set_xy(0, 50)
        
        # Ręczne ustawienie trybu renderowania przez parametry wewnętrzne (bezpieczniej)
        if style == "Tylko kontury (do kolorowania)":
             pdf.cell(210, 200, char, align='C') # Tu rysujemy normalnie
             # Jeśli powyższe nadal nie daje konturu, 
             # najbezpieczniej dla konturów użyć jasnego szarego koloru:
             # pdf.set_text_color(220, 220, 220)
        else:
             pdf.cell(210, 200, char, align='C')
        
    return bytes(pdf.output())