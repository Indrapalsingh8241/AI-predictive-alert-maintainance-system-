import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ==========================

# Database Connection

# ==========================

DATABASE_URL = "postgresql://postgres:postgres123@localhost:5433/predictive_alert_db"

engine = create_engine(DATABASE_URL)

# ==========================

# Auto Refresh

# ==========================

st_autorefresh(
interval=2000,
key="datarefresh"
)

# ==========================

# Page Config

# ==========================

st.set_page_config(
page_title="Industrial Predictive Alert System",
layout="wide"
)

st.title("🏭 Industrial Predictive Alert System")

st.caption(
f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
)

# ==========================

# Load Data

# ==========================

query = """
SELECT *
FROM prediction_logs
ORDER BY timestamp DESC
"""

df = pd.read_sql(query, engine)

if df.empty:
    st.warning("No sensor data available.")
    st.stop()

# ==========================

# KPI Cards

# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        len(df)
    )

with col2:
    st.metric(
        "Total Alerts",
        len(df[df["prediction"] == 1])
    )

with col3:
    st.metric(
        "Machines",
        df["machine_id"].nunique()
    )

with col4:
    st.metric(
        "Average Risk %",
        round(df["probability"].mean() * 100, 2)
    )

st.divider()

# ==========================

# Machine Filter

# ==========================

machines = sorted(
df["machine_id"].unique()
)

selected_machine = st.selectbox(
"Select Machine",
machines
)

machine_df = df[
df["machine_id"] == selected_machine
]

# ==========================

# Latest Machine Status

# ==========================

latest = machine_df.iloc[0]

probability = latest["probability"]

if probability >= 0.9:
    status = "🔴 Critical"

elif probability >= 0.7:
    status = "🟠 Warning"

else:
    status = "🟢 Healthy"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Machine",
        selected_machine
    )

with col2:
    st.metric(
        "Risk %",
        f"{probability * 100:.2f}"
    )

with col3:
    st.metric(
        "Status",
        status
    )

st.divider()

# ==========================

# Latest Data

# ==========================

st.subheader("Latest Records")

st.dataframe(
machine_df.head(20)
)

# ==========================

# Charts

# ==========================

df_chart = (
machine_df
.sort_values("timestamp")
.tail(20)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Temperature (°C)")
    st.line_chart(
        df_chart.set_index("timestamp")["temperature"]
    )

with col2:
    st.subheader("💧 Humidity (%)")
    st.line_chart(
        df_chart.set_index("timestamp")["humidity"]
    )

col3, col4 = st.columns(2)

with col3:
    st.subheader("⚙️ Pressure")
    st.line_chart(
        df_chart.set_index("timestamp")["pressure"]
    )

with col4:
    st.subheader("📳 Vibration")
    st.line_chart(
        df_chart.set_index("timestamp")["vibration"]
    )

# ==========================

# AI Analysis

# ==========================

st.divider()

st.subheader("🤖 Latest AI Analysis")

st.info(
latest["explanation"]
)

# ==========================

# Alert History

# ==========================

st.divider()

st.subheader("🚨 Recent Alerts")

alerts = machine_df[
machine_df["prediction"] == 1
]

st.dataframe(
alerts.head(10)
)
