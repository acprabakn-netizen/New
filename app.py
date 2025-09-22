import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Swing Trading App", layout="wide")

st.title("📈 AI Swing Trading Helper")

# User input
ticker = st.text_input("Enter Stock Symbol (NSE: RELIANCE.BO, INFY.NS etc.)", "INFY.NS")
period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y"])
interval = st.selectbox("Select Interval", ["1d", "1wk"])

if st.button("Fetch Data"):
    try:
        data = yf.download(ticker, period=period, interval=interval)
        st.subheader(f"{ticker} Price Data")
        st.dataframe(data.tail())

        # Simple Swing Signal
        data["20SMA"] = data["Close"].rolling(window=20).mean()
        data["50SMA"] = data["Close"].rolling(window=50).mean()

        st.subheader("Price with Swing Trade Signals")
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(data["Close"], label="Close Price")
        ax.plot(data["20SMA"], label="20 SMA", alpha=0.7)
        ax.plot(data["50SMA"], label="50 SMA", alpha=0.7)
        ax.legend()
        st.pyplot(fig)

        # Buy/Sell logic
        if data["20SMA"].iloc[-1] > data["50SMA"].iloc[-1]:
            st.success("✅ Swing Trade Signal: BUY")
        else:
            st.error("❌ Swing Trade Signal: SELL")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
