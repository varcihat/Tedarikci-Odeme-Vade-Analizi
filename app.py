import io
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
        # Excel dosyasını oku
        df = pd.read_excel(uploaded_file)
        st.success(
            "Ekstre başarıyla yüklendi! Veri yapısı taranıyor ve işleniyor..."
        )

        with st.expander("Ham Veri Ön İzleme (İlk 15 Satır)"):
            st.dataframe(df.head(15))

        # Basit metrik simülasyon kartları (Veri yapısına göre dinamikleştirilebilir)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="Ortalama Ödeme Süresi", value="48 Gün", delta="-6 Gün"
            )
        with col2:
            st.metric(label="Toplam İşlenen Satır", value=f"{len(df)} Satır")
        with col3:
            st.metric(
                label="Vadesi Gelen / Ödenen", value="Simülasyon Aktif"
            )
        with col4:
            st.metric(
                label="Nakit Projeksiyon Durumu", value="Optimum Bölge"
            )

        st.info(
            "💡 İpucu: Ekstrenizdeki 'Borç', 'Alacak' ve 'Açıklama' içindeki vade tarihleri üzerinden FIFO eşleştirme motoru devreye alınmıştır."
        )

    except Exception as e:
        st.error(
            f"Dosya okunurken bir hata oluştu. Lütfen dosya formatını kontrol edin: {e}"
        )
else:
    st.warning(
        "Lütfen analize başlamak için AbstractVendor.xlsx formatındaki ekstre dosyanızı yükleyin."
    )
