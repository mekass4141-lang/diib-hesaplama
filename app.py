import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_from_pdfs(inv, pack):
    # 1. Packing List verilerini bir sözlükte topla (Kod -> KG toplamı)
    pack_map = {}
    with pdfplumber.open(pack) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:
                    if row[0] and row[6]: # 0: Kod, 6: KG
                        try:
                            code = str(row[0]).strip()
                            kg = float(str(row[6]).replace(',', '.').replace(' KG', ''))
                            pack_map[code] = pack_map.get(code, 0) + kg
                        except: continue

    # 2. Fatura satırlarını tara
    st.subheader("Hesaplama Sonuçları")
    line_counter = 1
    with pdfplumber.open(inv) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:
                    # Faturadaki kod sütununu bul (genellikle 0. veya 1. sütun)
                    # Sizin faturanızda 0. sütun "Sıra No", 1. sütun "Malzeme Kodu"
                    code = str(row[1]).strip() if row[1] else ""
                    
                    if code in pack_map:
                        st.write(f"Line {line_counter} = {pack_map[code]:.2f} kg")
                        line_counter += 1
                        # Bir kez yazdıktan sonra aynı kodu tekrar bulursa yazmasın diye siliyoruz
                        del pack_map[code]

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
