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
                    # row[0] = Ürün Kodu, row[6] = KG
                    try:
                        code = str(row[0]).strip()
                        kg = float(str(row[6]).replace(',', '.').replace(' KG', ''))
                        if len(code) > 3 and kg > 0:
                            pack_data.append({"code": code, "kg": kg})
                    except:
                        continue
    
    # 6 satır yerine sadece benzersiz ürün kodlarını grupla
    df = pd.DataFrame(pack_data)
    grouped = df.groupby("code")["kg"].sum().reset_index()

    st.subheader("Hesaplama Sonuçları")
    # Gruplanmış veriyi yazdır
    for i, row in grouped.iterrows():
        st.write(f"Line {i+1} ({row['code']}) = {row['kg']:.2f} kg")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
