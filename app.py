import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nervosense Dashboard", page_icon="🧠", layout="wide")

st.title("🧠 Nervosense – Your Nervous System Dashboard")
st.markdown("Real-time view of HRV trends, sleep patterns, recovery states, stress signatures, and body budget fluctuations.")

dates = pd.date_range("2026-01-01", periods=7, freq="D")
df = pd.DataFrame({
    "Date": dates,
    "HRV (ms)": np.random.normal(60, 10, 7),
    "Sleep Score": np.random.randint(70, 95, 7),
    "Stress Level": np.random.uniform(0, 10, 7),
    "Recovery (%)": np.random.randint(50, 100, 7),
    "Body Budget": np.cumsum(np.random.normal(0, 5, 7))
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("HRV Trends")
    fig_hrv = px.line(df, x="Date", y="HRV (ms)", title="Heart Rate Variability")
    st.plotly_chart(fig_hrv, use_container_width=True)

    st.subheader("Sleep Patterns")
    fig_sleep = px.bar(df, x="Date", y="Sleep Score", title="Daily Sleep Score")
    st.plotly_chart(fig_sleep, use_container_width=True)

with col2:
    st.subheader("Stress & Recovery")
    fig_stress = px.line(df, x="Date", y=["Stress Level", "Recovery (%)"], title="Stress vs Recovery")
    st.plotly_chart(fig_stress, use_container_width=True)

    st.subheader("Body Budget Fluctuations")
    fig_budget = px.area(df, x="Date", y="Body Budget", title="Daily Body Budget")
    st.plotly_chart(fig_budget, use_container_width=True)

st.header("Key Insights")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Average HRV", f"{df['HRV (ms)'].mean():.1f} ms")
col_b.metric("Average Sleep", f"{df['Sleep Score'].mean():.0f}")
col_c.metric("Stress Trend", "Moderate")
col_d.metric("Recovery State", "Balanced")

st.caption("Data shown is simulated. Connect wearable for real metrics.")