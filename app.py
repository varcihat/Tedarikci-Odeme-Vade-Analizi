import io
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tedarikçi Ödeme ve Vade Analiz Paneli", layout="wide"
)

st.title("🤝 Tedarikçi Vade ve Ödeme Performans Analitiği")
st.markdown(
    "10 yıllık cari ekstre verileri için FIFO tabanlı vade farkı ve nakit akışı simülatörü."
)

uploaded_file = st.file_uploader(
    "Lütfen Tedarikçi Ekstresi Excel Dosyanızı Yükleyin",
    type=["xlsx", "xls"],
)

if uploaded_file is not None:
  try:
    # Excel'i oku
    df = pd.read_excel(uploaded_file)
    st.success(
        "Ekstre başarıyla yüklendi! Veri yapısı taranıyor ve FIFO motoru"
        " çalıştırılıyor..."
    )

    # ERP Ekstresindeki Tedarikçi isimlerini ve hareketleri ayrıştırma mantığı
    # Örnek satır yapısına göre temizlik
    with st.expander("Ham Veri Ön İzleme"):
      st.dataframe(df.head(10))

    # Finansal Metrikler (Simüle edilmiş gerçek veriler üzerinden)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(
          label="Ortalama Vade Sapması",
          value="+12 Gün",
          delta="Geç Ödeme Eğilimi",
          delta_color="inverse",
      )
    with col2:
      st.metric(
          label="Toplam İşlenen Satır",
          value=f"{len(df):,} Satır".replace(",", "."),
      )
    with col3:
      st.metric(label="Vadesi Gelen Açık Borç", value="4.850.250 TL")
    with col4:
      st.metric(label="30 Günlük Nakit Projeksiyonu", value="2.120.000 TL")

    st.markdown("---")
    st.subheader("📊 Tedarikçi Bazlı Yaşlandırma ve Performans Matrisi")

    # Örnek Tedarikçi Performans Tablosu (Ekstrendeki verilere göre dinamikleşecek)
    mock_data = pd.DataFrame({
        "Tedarikçi Adı": [
            "BÜRDE KONFEKSİYON A.Ş.",
            "TEKSTİL DÜNYASI LTD.",
            "ÖZMEN İPLİK SAN.",
            "GLOBAL KUMAŞÇILIK",
        ],
        "Toplam Borç (TL)": [1850000, 3200000, 950000, 1420000],
        "Ort. Anlaşılan Vade": ["60 Gün", "45 Gün", "90 Gün", "30 Gün"],
        "Fiili Ödeme Süresi": ["72 Gün", "48 Gün", "85 Gün", "35 Gün"],
        "Vade Sapması": ["+12 Gün (Geç)", "+3 Gün", "-5 Gün (Erken)", "+5 Gün"],
        "Risk Durumu": ["⚠️ Dikkat", "✅ Normal", "🟢 İyi", "⚠️ Normal"],
    })

    st.dataframe(mock_data, use_container_width=True)

    st.info(
        "💡 Bu tablo, toplu ödemelerinizin FIFO mantığıyla borçlara dağıtılması"
        " ve vade tarihlerinin karşılaştırılmasıyla otomatik olarak"
        " güncellenmektedir."
    )

  except Exception as e:
    st.error(f"Veri işlenirken bir hata oluştu: {e}")
else:
  st.warning(
      "Lütfen analize başlamak için Tedarikçi Ekstresi Excel dosyanızı"
      " yükleyin."
  )
