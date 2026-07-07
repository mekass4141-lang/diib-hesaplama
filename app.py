import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_from_pdfs(inv, pack):
    # Packing List'i tara
    pack_data = {}
    with pdfplumber.open(pack) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    # Tablonun her satırında 'Product Code' ve 'KG' değerlerini arayalım
                    # Genelde kod 0. sütunda, KG 6. sütunda olur, ancak daha geniş arıyoruz
                    try:
                        # Kod içeren satırları filtrele
                        code = str(row[0]).strip() if row[0] else ""
                        kg_val = 0.0
                        
                        # KG değerini satırın içindeki tüm hücrelerde arayalım
                        for cell in row:
                            if cell and "KG" in str(cell).upper():
                                kg_val = float(str(cell).replace(' KG', '').replace(',', '.'))
                        
                        if len(code) > 3:
                            pack_data[code] = pack_data.get(code, 0) + kg_val
                    except: continue

    if not pack_data:
        st.error("Veriler okunamadı! Lütfen PDF'lerin tablo yapısını kontrol edin.")
        return

    st.subheader("Hesaplama Sonuçları")
    for i, (code, kg) in enumerate(pack_data.items(), 1):
        st.write(f"Line {i} = {kg:.2f} kg")
    
    st.success("Hesaplama tamamlandı.")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
