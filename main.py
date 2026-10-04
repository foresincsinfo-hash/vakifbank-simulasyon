import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# 1. Sayfa Ayarları ve VakıfBank Teması
st.set_page_config(page_title="VakıfBank Mobil Simülasyonu", page_icon="🏦", layout="wide")

# Oturum Durumu (Session State) Tanımlamaları
if 'balance' not in st.session_state:
    st.session_state.balance = 50000.00
if 'history' not in st.session_state:
    st.session_state.history = [
        {"Tarih": "2026-10-04 14:20", "İşlem Türü": "Gelen Havale", "Açıklama": "Maaş Ödemesi", "Tutar": "+50,000.00 TL", "Bakiye": "50,000.00 TL"}
    ]
if 'sms_pending' not in st.session_state:
    st.session_state.sms_pending = False
if 'pending_amount' not in st.session_state:
    st.session_state.pending_amount = 0.0
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Karanlık Mod / Aydınlık Mod Dinamik CSS Ayarları
if st.session_state.dark_mode:
    bg_color = "#121212"
    text_color = "#FFFFFF"
    card_bg = "#1E1E1E"
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .bank-card {{ background-color: {card_bg}; padding: 20px; border-radius: 15px; border-left: 8px solid #FFC72C; color: white; margin-bottom: 20px; }}
        </style>
        """, unsafe_allow_html=True
    )
else:
    bg_color = "#F4F6F9"
    text_color = "#1A1A1A"
    card_bg = "#FFFFFF"
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .bank-card {{ background-color: {card_bg}; padding: 20px; border-radius: 15px; border-left: 8px solid #FFC72C; box-shadow: 2px 4px 10px rgba(0,0,0,0.08); color: #1A1A1A; margin-bottom: 20px; }}
        </style>
        """, unsafe_allow_html=True
    )

# Üst Bar: Logo, Kullanıcı Bilgisi ve Gece Modu Butonu
col_logo, col_user, col_theme = st.columns(3)
with col_logo:
    st.markdown("<h2 style='color:#FFC72C; margin:0;'>VakıfBank</h2><p style='font-size:12px; margin:0; opacity:0.8;'>Burada Başlar, Burada Büyür</p>", unsafe_allow_html=True)
with col_user:
    st.markdown("<div style='text-align: right; padding-top: 10px;'><b>Sayın Bülent Erdost</b><br><span style='font-size:12px; opacity:0.7;'>Müşteri No: 98765432</span></div>", unsafe_allow_html=True)
with col_theme:
    if st.button("🌙 Gece Modu Değiştir" if not st.session_state.dark_mode else "☀️ Aydınlık Moda Geç"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("<hr style='margin-top:10px; margin-bottom:20px;'>", unsafe_allow_html=True)

# Sol Kolon (İşlemler ve Bakiye Kartı) | Sağ Kolon (Grafik Analizi)
col_left, col_right = st.columns(2)

with col_left:
    # Bakiye ve Kart Bilgileri Alanı
    st.markdown(
        f"""
        <div class="bank-card">
            <span style="font-size: 14px; uppercase; opacity: 0.8;">VakıfBank Bankomat Hesap</span>
            <h1 style="color: #FFC72C; margin: 10px 0;">{st.session_state.balance:,.2f} TL</h1>
            <p style="font-size: 13px; margin: 0; font-family: monospace;">IBAN: TR93 0001 5001 5800 0019 5400 12</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Menü Sekmeleri: Bakiye Yükle & Para Transferi
    tab1, tab2 = st.tabs(["➕ Hesaba Bakiye Ekle", "💸 Para Transferi (EFT/Havale)"])
    
    with tab1:
        st.subheader("Güvenli Bakiye Yükleme Paneli")
        amount_to_add = st.number_input("Yüklenecek Tutar (TL)", min_value=10.0, max_value=100000.0, value=1000.0, step=500.0)
        
        if st.button("Bakiye Yükleme İşlemini Başlat"):
            st.session_state.pending_amount = amount_to_add
            st.session_state.sms_pending = True
            st.rerun()

        # 3D Secure SMS Pop-up Simülasyonu
        if st.session_state.sms_pending:
            st.warning("🔒 3D Secure Güvenlik Doğrulaması Adımı")
            st.info("Bülent Erdost adına kayıtlı +90 53* *** ** 54 telefonuna gönderilen doğrulama kodunu giriniz.")
            sms_code = st.text_input("SMS Onay Kodu (İpucu: 1954)", max_chars=4)
            
            col_sms1, col_sms2 = st.columns(2)
            with col_sms1:
                if st.button("Onayla"):
                    if sms_code == "1954":
                        st.session_state.balance += st.session_state.pending_amount
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.session_state.history.append({
                            "Tarih": now_str,
                            "İşlem Türü": "Bakiye Yükleme",
                            "Açıklama": "3D Secure Mobil Yükleme",
                            "Tutar": f"+{st.session_state.pending_amount:,.2f} TL",
                            "Bakiye": f"{st.session_state.balance:,.2f} TL"
                        })
                        st.success(f"Başarılı! Hesabınıza {st.session_state.pending_amount:,.2f} TL eklenmiştir.")
                        st.session_state.sms_pending = False
                        st.session_state.pending_amount = 0.0
                        st.rerun()
                    else:
                        st.error("Hatalı SMS kodu girdiniz! Lütfen tekrar deneyin.")
            with col_sms2:
                if st.button("İptal Et"):
                    st.session_state.sms_pending = False
                    st.session_state.pending_amount = 0.0
                    st.rerun()

    with tab2:
        st.subheader("Yeni Havale / EFT Gönderimi")
        transfer_name = st.text_input("Alıcı Adı Soyadı")
        transfer_iban = st.text_input("Alıcı IBAN Numarası", placeholder="TR00 0000...")
        transfer_amount = st.number_input("Gönderilecek Tutar (TL)", min_value=1.0, max_value=st.session_state.balance, value=100.0)
        transfer_desc = st.text_input("Açıklama", value="Diğer Ödemeler")
        
        if st.button("Para Transferini Gerçekleştir"):
            if transfer_name and transfer_iban:
                if transfer_amount <= st.session_state.balance:
                    st.session_state.balance -= transfer_amount
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.history.append({
                        "Tarih": now_str,
                        "İşlem Türü": "Giden Transfer",
                        "Açıklama": f"{transfer_name} - {transfer_desc}",
                        "Tutar": f"-{transfer_amount:,.2f} TL",
                        "Bakiye": f"{st.session_state.balance:,.2f} TL"
                    })
                    st.success(f"{transfer_name} hesabına {transfer_amount:,.2f} TL başarıyla gönderildi!")
                    st.rerun()
                else:
                    st.error("Yetersiz bakiye! Lütfen gönderim tutarını kontrol edin.")
            else:
                st.error("Lütfen Alıcı Adı ve IBAN alanlarını boş bırakmayınız.")

with col_right:
    st.subheader("📊 Demo Bakiye Hareketi")
    try:
        balance_points = [float(item["Bakiye"].replace(" TL", "").replace(",", "")) for item in st.session_state.history]
        time_points = [item["Tarih"] for item in st.session_state.history]
        
        df_chart = pd.DataFrame({"Zaman": time_points, "Bakiye (TL)": balance_points})
        fig = px.line(df_chart, x="Zaman", y="Bakiye (TL)", markers=True, color_discrete_sequence=["#FFC72C"])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#FFFFFF" if st.session_state.dark_mode else "#1A1A1A"
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Grafik oluşturulması için hareket bekleniyor.")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🧾 Son Hesap Hareketleri")
if st.session_state.history:
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history.iloc[::-1], use_container_width=True)
else:
    st.info("Henüz bir hesap hareketi bulunmuyor.")

st.markdown(
    """
