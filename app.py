import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_diib(invoice_pdf, packing_pdf):
    # PDF'leri okuma ve işleme mantığı buraya gelecek
    st.write("---")
    st.subheader("Hesaplama Sonuçları")
    # Örnek test çıktısı
    st.write("Line 4 = 1500 kg")
    st.write("Line 11 = 200 kg")
    st.success("Matches / Does not match")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_diib(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
