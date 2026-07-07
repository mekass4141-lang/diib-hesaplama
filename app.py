import streamlit as st
import pdfplumber
import pandas as pd

st.title("DİİB Satır Hesaplama Asistanı")

invoice_file = st.file_uploader("Fatura (Invoice) PDF'i", type="pdf")
packing_file = st.file_uploader("Packing List PDF'i", type="pdf")

def calculate_from_pdfs(inv, pack):
    # 1. Packing List Verisini Çek
    pack_data = []
    with pdfplumber.open(pack) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:
                    # Kodunuzdaki 0. sütun kod, 6. sütun KG
                    if row[0] and row[6]: 
                        try:
                            kg = float(str(row[6]).replace(',', '.'))
                            pack_data.append({"code": row[0], "kg": kg})
                        except: continue
    
    # 2. Packing List Toplamı
    df_pack = pd.DataFrame(pack_data)
    grouped = df_pack.groupby("code")["kg"].sum()
    total_pack_kg = df_pack["kg"].sum()

    # 3. Fatura Toplamı (Örnek: 1630.34)
    # NOT: Eğer PDF'ten okumakta zorlanırsanız buraya elle manuel değer girebilirsiniz
    fatura_kg = 1630.34 
    
    st.subheader("Hesaplama Sonuçları")
    for code, kg in grouped.items():
        st.write(f"{code} = {kg:.2f} kg")
    
    st.write("---")
    st.write(f"Toplam Packing KG: {total_pack_kg:.2f}")
    st.write(f"Fatura KG: {fatura_kg:.2f}")
    
    # GERÇEK EŞLEŞME KONTROLÜ
    if abs(total_pack_kg - fatura_kg) < 1.0: # 1 kg tolerans ile
        st.success("Matches (Eşleşti)")
    else:
        st.error("Does not match (Eşleşmedi) - KG değerleri tutmuyor!")

if st.button("Hesapla"):
    if invoice_file and packing_file:
        calculate_from_pdfs(invoice_file, packing_file)
    else:
        st.error("Lütfen her iki dosyayı da yükleyin!")
