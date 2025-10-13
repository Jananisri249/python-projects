import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Advanced Hospital Sensor Monitoring",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏥 Advanced Hospital Sensor Live Monitoring")
st.write("This dashboard simulates live sensor data for multiple patients and includes a real-time chart and alert system for critical imbalances.")
time_placeholder = st.empty()

# --- Alert Thresholds ---
HEART_RATE_NORMAL = (60, 100)
TEMPERATURE_NORMAL = (36.5, 37.5)
OXYGEN_NORMAL = (95, 100)

# --- Patient Management ---
if "patients" not in st.session_state:
    st.session_state.patients = ["Alice", "Bob", "Charlie"]
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = st.session_state.patients[0]
if "data_history_dict" not in st.session_state:
    st.session_state.data_history_dict = {name: pd.DataFrame(columns=['timestamp', 'Heart Rate', 'Temperature', 'Oxygen Level']) for name in st.session_state.patients}
if "running" not in st.session_state:
    st.session_state.running = False

# Patient selection
st.sidebar.header("Patient Selection")
selected_patient = st.sidebar.selectbox("Choose patient", st.session_state.patients)
st.session_state.selected_patient = selected_patient

# Add new patient
new_patient = st.sidebar.text_input("Add new patient")
if st.sidebar.button("Add Patient") and new_patient.strip():
    if new_patient not in st.session_state.patients:
        st.session_state.patients.append(new_patient)
        st.session_state.data_history_dict[new_patient] = pd.DataFrame(columns=['timestamp', 'Heart Rate', 'Temperature', 'Oxygen Level'])
        st.session_state.selected_patient = new_patient

st.header(f"Monitoring: {st.session_state.selected_patient}")

def sensor_data_stream():
    """Generates a stream of simulated sensor data, occasionally outside normal ranges."""
    if random.random() < 0.1:
        hr = random.choice([random.randint(40, 55), random.randint(105, 120)])
        temp = round(random.choice([random.uniform(35.0, 36.2), random.uniform(37.8, 39.0)]), 1)
        oxy = random.randint(88, 94)
    else:
        hr = random.randint(HEART_RATE_NORMAL[0], HEART_RATE_NORMAL[1])
        temp = round(random.uniform(TEMPERATURE_NORMAL[0], TEMPERATURE_NORMAL[1]), 1)
        oxy = random.randint(OXYGEN_NORMAL[0], OXYGEN_NORMAL[1])
    yield {
        "heart_rate": hr,
        "temperature": temp,
        "oxygen_level": oxy
    }

# --- Start/Stop Buttons ---
col_btn1, col_btn2 = st.columns([1,1])
with col_btn1:
    if st.button("Start"):
        st.session_state.running = True
with col_btn2:
    if st.button("Stop"):
        st.session_state.running = False

# --- UI Layout ---
alert_placeholder = st.empty()
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("❤️ Heart Rate")
    hr_metric = st.empty()
with col2:
    st.subheader("🌡️ Temperature")
    temp_metric = st.empty()
with col3:
    st.subheader("💨 Oxygen Level (SpO2)")
    oxy_metric = st.empty()
st.subheader("Live Sensor Data History")
chart_placeholder = st.empty()

# --- Live Data Update ---
if st.session_state.running:
    for data in sensor_data_stream():
        heart_rate = data["heart_rate"]
        temperature = data["temperature"]
        oxygen_level = data["oxygen_level"]
        timestamp = datetime.now()

        # --- Live Clock ---
        time_placeholder.markdown(f"### Last Update: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        # --- Check for Alerts ---
        alert_messages = []
        if not (HEART_RATE_NORMAL[0] <= heart_rate <= HEART_RATE_NORMAL[1]):
            alert_messages.append(f"Critical Heart Rate: {heart_rate} BPM!")
        if not (TEMPERATURE_NORMAL[0] <= temperature <= TEMPERATURE_NORMAL[1]):
            alert_messages.append(f"Critical Temperature: {temperature}°C!")
        if not (OXYGEN_NORMAL[0] <= oxygen_level <= OXYGEN_NORMAL[1]):
            alert_messages.append(f"Critical Oxygen Level: {oxygen_level}%!")

        if alert_messages:
            alert_placeholder.error("🚨 ALERT: " + " | ".join(alert_messages))
        else:
            alert_placeholder.empty()

        # --- Update Metrics ---
        hr_metric.metric(label="BPM", value=f"{heart_rate}", delta=f"{heart_rate - 75}")
        temp_metric.metric(label="Celsius", value=f"{temperature}°C", delta=f"{round(temperature - 37.0, 1)}")
        oxy_metric.metric(label="%", value=f"{oxygen_level}", delta=f"{oxygen_level - 98}")

        # --- Update Data History for selected patient ---
        new_data = pd.DataFrame([{
            'timestamp': timestamp,
            'Heart Rate': heart_rate,
            'Temperature': temperature,
            'Oxygen Level': oxygen_level
        }])
        history = st.session_state.data_history_dict[st.session_state.selected_patient]
        history = pd.concat([history, new_data], ignore_index=True)
        if len(history) > 100:
            history = history.tail(100)
        st.session_state.data_history_dict[st.session_state.selected_patient] = history

        # --- Update Chart ---
        chart_data = history.melt(
            id_vars=['timestamp'],
            value_vars=['Heart Rate', 'Temperature', 'Oxygen Level'],
            var_name='Metric',
            value_name='Value'
        )
        import altair as alt
        line_chart = alt.Chart(chart_data).mark_line(interpolate='basis').encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('Value:Q', title='Sensor Value'),
            color=alt.Color('Metric:N', title='Metric')
        ).properties(
            title=f"{st.session_state.selected_patient} Sensor Readings Over Time"
        )
        chart_placeholder.altair_chart(line_chart, use_container_width=True)
        time.sleep(1)
        st.experimental_rerun()
        