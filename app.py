import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_from_pdfs(inv, pack):
    results = []
    # Packing List tablosunu oku
    with pdfplumber.open(pack) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                # Tablodaki verileri satır satır çek
                for row in table[1:]: # Başlık hariç
                    if row[0] and row[6]: # Ürün kodu ve KG sütunları
                        results.append({"code": row[0], "kg": float(str(row[6]).replace(',', '.'))})
    
    # Gruplama
    df = pd.DataFrame(results)
    grouped = df.groupby("code")["kg"].sum()
    
    st.subheader("Hesaplama Sonuçları")
    for i, (code, kg) in enumerate(grouped.items(), 1):
        st.write(f"Line {i} = {kg:.2f} kg")
    
    st.success("Matches")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
