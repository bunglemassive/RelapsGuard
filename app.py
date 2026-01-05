import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Custom CSS for sleek concise look
st.markdown("""
<style>
    .main {background-color: #f0f4f8;}
    .card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.8rem;
        text-align: center;
    }
    .panic-btn {
        background-color: #d32f2f;
        color: white;
        font-size: 1.2rem;
        padding: 0.8rem 1.5rem;
        border-radius: 0.8rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    h1, h2 {color: #1565c0; text-align: center;}
    .stPlotlyChart {height: 250px !important;} /* Smaller graphs */
</style>
""", unsafe_allow_html=True)

st.title("Nervosense Dashboard")

# Fake patient names (more realistic)
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
patients = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(200)]

# Select patient
patient_name = st.selectbox("Select Patient", options=patients, index=0)

# Fake data
avg_hr = round(random.uniform(70, 90), 1)
med_rate = round(random.uniform(85, 98))
points = random.randint(180, 224)
journal = random.choice([
    "Feeling balanced today – good breathing exercises.",
    "Stress lower after walk in park.",
    "Heart rate steady, slept well.",
    "Challenging morning but used app reminder.",
    "Positive day – connected with support."
])

# Concise metrics (smaller cards)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><h4>Avg Heart Rate</h4><h2>{avg_hr} bpm</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h4>Med Acknowledged</h4><h2>{med_rate}%</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><h4>Data Points</h4><h2>{points}</h2></div>', unsafe_allow_html=True)

# Smaller progress graph
st.markdown('<div class="card"><h3>30-Day Trend</h3></div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(5, 2.5))
dates = pd.date_range(end=datetime.today(), periods=30)
values = [random.uniform(60, 90) for _ in range(30)]
ax.plot(dates, values, marker='o', linewidth=2, color='#1565c0')
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Concise journal
st.markdown('<div class="card"><h3>Latest Journal Entry</h3><p>{}</p></div>'.format(journal), unsafe_allow_html=True)

# Centred panic button
st.markdown('<div class="text-center"><button class="panic-btn">Panic Button – Request Support</button></div>', unsafe_allow_html=True)

# Optional GIS (collapsible)
with st.expander("AI Location Insights (Opt-In)"):
    st.write("Nearby calming alternatives:")
    st.write("• Park (0.4km) – good for breathing exercises")
    st.write("• Quiet café (0.8km) – low-stress environment")
