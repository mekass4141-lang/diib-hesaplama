import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_from_pdfs(inv, pack):
    pack_data = []
    with pdfplumber.open(pack) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    # row[6] Total Net (Kg) sütunudur
                    try:
                        kg = float(str(row[6]).replace(',', '.').replace(' KG', ''))
                        if kg > 0:
                            pack_data.append(kg)
                    except:
                        continue
    
    # Sizin kuralınıza göre: Tekrarlı ürün kodlarını önemsemeden 
    # satırları tek tek topluyoruz.
    st.subheader("Hesaplama Sonuçları")
    for i, kg in enumerate(pack_data, 1):
        st.write(f"Line {i} = {kg:.2f} kg")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
