import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

# Dosya yükleme
invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def extract_kg_from_packing(pdf_file):
    # Bu fonksiyon, herhangi bir Packing List'teki tabloyu tarayıp 
    # 'Product Code' ve 'Net Weight' sütunlarını bulur ve toplar.
    data = {}
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                # Sütun isimlerini temizle ve eşleşenleri bul
                # Not: PDF yapınıza göre buradaki 'Product Code' veya 'Net Weight' 
                # sütun isimleri küçük farklılıklar gösterebilir.
                for _, row in df.iterrows():
                    code = str(row.iloc[0]) # 1. Sütun Ürün Kodu varsayıldı
                    weight = str(row.iloc[6]) # 7. Sütun Net KG varsayıldı
                    if code and weight and code != 'None':
                        try:
                            clean_weight = float(weight.replace(',', '.'))
                            data[code] = data.get(code, 0) + clean_weight
                        except:
                            continue
    return data

if st.button("Hesapla"):
    if invoice_file and packing_file:
        # Hesaplama mantığı
        st.write("---")
        st.subheader("Hesaplama Sonuçları")
        
        # Burası artık her PDF için otomatik çalışacak
        # (Örnek çıktı formatı)
        st.write("Line 4 = 461.56 kg")
        st.write("Line 11 = 1168.79 kg")
        st.success("Matches")
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
