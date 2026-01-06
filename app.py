import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import ollama  # For AI chat

# Custom CSS for sexy concise landscape look
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #e3f2fd;
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
    h1 {color: #1565c0; text-align: center;}
    h2, h3 {color: #1565c0;}
    .support-text {font-size: 1.1rem; line-height: 1.6; color: #444;}
</style>
""", unsafe_allow_html=True)

st.title("Nervosense Dashboard")

# Supportive intro text
st.markdown('<div class="card support-text"><p>Welcome back. This dashboard shows your body\'s natural patterns – ups and downs are normal. You\'re doing the work every day.</p></div>', unsafe_allow_html=True)

# Fake data generation (deterministic)
random.seed(42)
addictions = ['Alcohol', 'Opioids', 'Cocaine', 'Cannabis', 'Gambling', 'Other']
centres = ['Harmony Recovery Centre', 'Serenity Rehab', 'Hope Haven', 'Renewal Centre']
fake_names = [f"{random.choice(['John', 'Emma', 'Michael', 'Sophia', 'James', 'Olivia'])} {random.choice(['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Martinez'])}" for _ in range(100)]
patient_data = {i: {"name": fake_names[i-1], "addiction": random.choice(addictions), "centre": random.choice(centres)} for i in range(1, 101)}

# Increased data points: 30 days of HRV, sleep, recovery, stress, body budget
metrics = []
start_date = datetime(2025, 12, 6)
for pid in range(1, 101):
    for day in range(30):
        date = start_date + timedelta(days=day)
        metrics.append({
            "patient_id": pid,
            "date": date.strftime('%Y-%m-%d'),
            "hrv": random.randint(50, 100),
            "sleep_hours": random.uniform(5, 9),
            "recovery_state": random.choice(['Low', 'Medium', 'High']),
            "stress_level": random.randint(1, 10),
            "body_budget": random.uniform(40, 90)
        })

metrics_df = pd.DataFrame(metrics)

# Populated journals (15 per patient)
journals = []
for pid in range(1, 101):
    num = 15
    for _ in range(num):
        date = start_date + timedelta(days=random.randint(0, 29))
        entry = random.choice([
            "Body budget felt low today – rested and recovered.",
            "High stress level, but managed with breathing.",
            "Good sleep last night – recovery state high.",
            "HRV improved after walk – positive trend.",
            "Stress signature from work – noted for therapist.",
            "Balanced body budget – small win."
        ])
        journals.append({"patient_id": pid, "date": date.strftime('%Y-%m-%d'), "entry": entry})

journals_df = pd.DataFrame(journals)

# Select patient
patient_id = st.selectbox("Select Patient ID", options=list(range(1, 101)), index=0)
patient = patient_data[patient_id]
patient_metrics = metrics_df[metrics_df['patient_id'] == patient_id]
patient_journals = journals_df[journals_df['patient_id'] == patient_id].sort_values('date', ascending=False)

# Patient header with name
st.markdown(f'<div class="card"><h2>Welcome back, {patient["name"]}</h2><p>Addiction Focus: {patient["addiction"]} | Centre: {patient["centre"]}</p></div>', unsafe_allow_html=True)

# Concise metrics (horizontal for landscape)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    hrv_avg = patient_metrics['hrv'].mean()
    st.markdown(f'<div class="metric-card"><h4>HRV</h4><h2>{hrv_avg:.1f}</h2></div>', unsafe_allow_html=True)
with col2:
    sleep_avg = patient_metrics['sleep_hours'].mean()
    st.markdown(f'<div class="metric-card"><h4>Sleep (hrs)</h4><h2>{sleep_avg:.1f}</h2></div>', unsafe_allow_html=True)
with col3:
    recovery_mode = patient_metrics['recovery_state'].mode()[0] if not patient_metrics['recovery_state'].empty else 'N/A'
    st.markdown(f'<div class="metric-card"><h4>Recovery</h4><h2>{recovery_mode}</h2></div>', unsafe_allow_html=True)
with col4:
    stress_avg = patient_metrics['stress_level'].mean()
    st.markdown(f'<div class="metric-card"><h4>Stress</h4><h2>{stress_avg:.1f}</h2></div>', unsafe_allow_html=True)
with col5:
    body_budget_avg = patient_metrics['body_budget'].mean()
    st.markdown(f'<div class="metric-card"><h4>Body Budget</h4><h2>{body_budget_avg:.1f}%</h2></div>', unsafe_allow_html=True)

# Supportive text
st.markdown('<div class="card support-text"><p>These numbers show your body\'s natural patterns – ups and downs are normal. You\'re doing the work every day.</p></div>', unsafe_allow_html=True)

# Recent journals (latest 8 for more content)
st.markdown('<div class="card"><h3>Recent Journal Entries (Latest 8)</h3></div>', unsafe_allow_html=True)
for _, row in patient_journals.head(8).iterrows():
    st.markdown(f"**{row['date']}**: {row['entry']}")

# Panic button with suggested call
if st.button("Simulated Panic Button – Request Check-in", key="panic"):
    st.success("Suggested check-in: within 30 minutes by your nominated therapist/support contact")

# Optional GIS/AI (collapsible for conciseness)
with st.expander("AI Location Insights (Voluntary Opt-In)"):
    st.write("Nearby positive alternatives:")
    st.write("• Gym (0.5km) – great for stress relief")
    st.write("• Recovery Centre (1.2km) – drop-in support available")
    st.write("(No tracking – search when you choose)")

# AI Chat Popup for Metric Changes (voluntary)
with st.expander("AI Chat (Voluntary – Ask About Metrics)"):
    st.write("The AI can ask supportive questions about today's patterns – completely optional.")
    if st.button("Enable AI Chat"):
        # Dummy metric change detection
        metric_change = "body budget fluctuated today"
        gis_context = "near a gym"
        prompt = f"Generate a non-judgemental, encouraging question about {metric_change}. Include positive GIS context: {gis_context}."
        try:
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])['message']['content']
            st.write("AI Question: " + response)
        except Exception as e:
            st.write("AI not available right now – try journaling your thoughts instead. Your reflections are valuable.")
        user_input = st.text_input("Your Response (optional)")
        if user_input:
            st.write("Thank you for sharing – your insights matter.")