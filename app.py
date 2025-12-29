import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Relapse Guard PoC", layout="wide")
st.title("Relapse Guard - Proof of Concept")

# Groq cloud AI
api_key = st.secrets["GROQ_API_KEY"]
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
model = "llama-3.3-70b-versatile"

# Dummy data generation
if 'data_generated' not in st.session_state:
    centres = ["Cape Town Rehab", "Johannesburg Recovery", "Durban Wellness", "Pretoria Healing"]
    addictions = ["Alcohol", "Opioids", "Stimulants", "Cannabis", "Gambling"]
    patients = []
    for i in range(1,201):
        centre = random.choice(centres)
        addiction = random.choice(addictions)
        history_days = 60
        history = []
        base_risk = random.uniform(0.15, 0.6)
        for d in range(history_days):
            date = (datetime.now() - timedelta(days=history_days-d)).strftime("%Y-%m-%d")
            heart_rate = random.randint(60, 100) + random.randint(-15,30)
            breathing = random.randint(12,20) if heart_rate < 110 else random.randint(8,16)
            activity = random.randint(2000,15000)
            risk = max(0.1, min(0.9, base_risk + random.uniform(-0.15,0.15)))
            history.append({"date": date, "heart_rate": heart_rate, "breathing": breathing, "activity": activity, "risk": risk})
        patients.append({
            "id": i,
            "name": f"Patient {i}",
            "addiction": addiction,
            "centre": centre,
            "current_risk": history[-1]["risk"],
            "journal": [f"Day {d}: Sample reflection." for d in range(1,8)],
            "history": history
        })
    st.session_state.patients = patients
    st.session_state.data_generated = True

# Summary & At-Risk
all_patients_df = pd.DataFrame([{"Name": p["name"], "Centre": p["centre"], "Addiction": p["addiction"], "Current Risk": round(p["current_risk"],2)} for p in st.session_state.patients])
at_risk_df = all_patients_df[all_patients_df["Current Risk"] > 0.3].sort_values("Current Risk", ascending=False)

st.header("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", len(st.session_state.patients))
col2.metric("At Risk (>0.3)", len(at_risk_df))
col3.metric("Critical (>0.6)", len(all_patients_df[all_patients_df["Current Risk"] > 0.6]))

st.header("At-Risk Patients")
st.dataframe(at_risk_df.style.background_gradient(cmap="Reds", subset=["Current Risk"]))

# Drill-Down
st.header("Patient Drill-Down")
patient_name = st.selectbox("Select Patient", [p["name"] for p in st.session_state.patients])
patient = next(p for p in st.session_state.patients if p["name"] == patient_name)

df_hist = pd.DataFrame(patient["history"])
col1, col2 = st.columns(2)
with col1:
    fig_risk = px.line(df_hist, x="date", y="risk", title="Risk Trend")
    st.plotly_chart(fig_risk, use_container_width=True)
    fig_hr = px.line(df_hist, x="date", y="heart_rate", title="Heart Rate")
    st.plotly_chart(fig_hr, use_container_width=True)
with col2:
    fig_breath = px.line(df_hist, x="date", y="breathing", title="Breathing Rate")
    st.plotly_chart(fig_breath, use_container_width=True)
    fig_act = px.line(df_hist, x="date", y="activity", title="Activity")
    st.plotly_chart(fig_act, use_container_width=True)

st.write("**Journals**")
for entry in patient["journal"]:
    st.text(entry)

if st.button("Analyse Patient Record with AI"):
    prompt = f"Analyse {patient['name']} ({patient['addiction']}): Risk {patient['current_risk']:.2f}. Last 14 days metrics: {df_hist.tail(14).to_dict('records')}. Journals: {patient['journal']}. Provide relapse insights, anomalies, forecast, recommendations."
    with st.spinner("AI analysing..."):
        response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
        st.markdown(response.choices[0].message.content)

st.info("PoC with dummy data. AI via Groq cloud.")
