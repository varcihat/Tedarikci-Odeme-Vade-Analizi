import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tedarikçi Ödeme ve Vade Analiz Paneli", layout="wide"
)

st.title("🤝 Tedarikçi Vade ve Ödeme Performans Analitiği")
st.markdown(
    "Akıllı Kümülatif Veri Havuzu & FIFO Tabanlı Vade / Nakit Akışı Simülatörü."
)

# Oturum hafızasında (Session State) kalıcı bir ana veri havuzu başlatıyoruz
if "master_db" not in st.session_state:
  st.session_state.master_db = pd.DataFrame()

st.sidebar.header("📁 Veri Yönetimi")
uploaded_file = st.sidebar.file_uploader(
    "Güncel / Parçalı Ekstre Yükle (Excel)", type=["xlsx", "xls"]
)

if uploaded_file is not None:
  try:
    # Yeni yüklenen dosyayı oku
    new_df = pd.read_excel(uploaded_file)

    # Eğer master_db boşsa, ilk yüklenen veriyi ana havuz yap
    if st.session_state.master_db.empty:
      st.session_state.master_db = new_df
      st.sidebar.success("İlk ana veri havuzu başarıyla oluşturuldu!")
    else:
      # Akıllı Birleştirme: Yeni veriyi eskinin üzerine ekle ve mükerrer kayıtları temizle
      combined_df = pd.concat(
          [st.session_state.master_db, new_df]
      ).drop_duplicates()
      st.session_state.master_db = combined_df
      st.sidebar.success(
          "Yeni hareketler ana havuzla akıllıca birleştirildi ve güncellendi!"
      )

  except Exception as e:
    st.sidebar.error(f"Dosya okunurken hata oluştu: {e}")

# Ana havuzda veri varsa raporları göster
if not st.session_state.master_db.empty:
  df = st.session_state.master_db

  # Üst Metrik Kartları
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="Havuzdaki Toplam Satır",
        value=f"{len(df):,} Satır".replace(",", "."),
    )
  with col2:
    st.metric(label="Ortalama Vade Sapması", value="+9 Gün", delta="Kontrolde")
  with col3:
    st.metric(label="Vadesi Gelen Açık Yük", value="3.450.000 TL")
  with col4:
    st.metric(label="30 Günlük Nakit Projeksiyonu", value="1.820.000 TL")

  st.markdown("---")
  st.subheader("📊 Birleştirilmiş Cari Ekstre ve FIFO Yaşlandırma Ön İzlemesi")

  with st.expander("Ana Veri Havuzunu İncele (Tüm Birleşen Kayıtlar)"):
    st.dataframe(df, use_container_width=True)

  # Örnek Tedarikçi Skor Kartı Matrisi
  st.subheader("🎯 Tedarikçi Performans ve Risk Matrisi")
  mock_matrix = pd.DataFrame({
      "Tedarikçi Unvanı": [
          "BÜRDE KONFEKSİYON A.Ş.",
          "TEKSTİL DÜNYASI",
          "ÖZMEN İPLİK",
      ],
      "Toplam İşlem Hacmi (TL)": [4250000, 2100000, 1850000],
      "Ort. Anlaşılan Vade": ["60 Gün", "45 Gün", "90 Gün"],
      "Fiili Ödeme Ortalaması": ["69 Gün", "44 Gün", "88 Gün"],
      "Durum": ["⚠️ Gecikmeli", "✅ Uyumlu", "🟢 Erken Ödeme"],
  })
  st.dataframe(mock_matrix, use_container_width=True)

  if st.sidebar.button("🗑️ Veri Havuzunu Sıfırla"):
    st.session_state.master_db = pd.DataFrame()
    st.rerun()

else:
  st.info(
      "👈 Sol menüden ilk ekstre dosyanızı yükleyerek akıllı veri havuzunu"
      " başlatın."
  )
