import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh
from datetime import datetime


# ==========================

# Database Connection

# ==========================
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)

# ==========================

# Auto Refresh

# ==========================

st_autorefresh(
interval=5000,
key="datarefresh"
)

# ==========================

# Page Config

# ==========================

st.set_page_config(
page_title="Industrial Predictive Alert System",
layout="wide"
)
st.title(
    "🏭 AI-Powered Real-Time Industrial Predictive Alert System"
)

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

conn = engine.raw_connection()

try:
    df = pd.read_sql_query(query, conn)
finally:
    conn.close()

if df.empty:
    st.warning("No sensor data available.")
    st.stop()

# ==========================

# KPI Cards

# ==========================
with st.sidebar:
    st.title("🏭 Factory Control")

    st.success("System Online")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Machine Health",
            "Analytics",
            "AI Analysis",
            "Alerts"
        ]
    )

    st.divider()

    st.write(f"Records: {len(df)}")
    st.write(f"Machines: {df['machine_id'].nunique()}")
if page == "Dashboard":
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

    running = len(df[df["status"] == "RUNNING"])
    warning = len(df[df["status"] == "WARNING"])
    stopped = len(df[df["status"] == "STOPPED"])

    st.subheader("🏭 Factory Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("🟢 Running", running)
    c2.metric("🟠 Warning", warning)
    c3.metric("🔴 Stopped", stopped)

    st.divider()
    latest_status = (
    df.sort_values("timestamp", ascending=False)
      .drop_duplicates("machine_id")
      [["machine_id", "status", "probability"]]
      .sort_values("probability", ascending=False)
)

    st.subheader("⚙️ Machine Health Summary")

    st.dataframe(
    latest_status,
    use_container_width=True
)
elif page == "Machine Health":
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

    st.subheader("📋 Latest Records")

    st.dataframe(
    machine_df.head(20),
    use_container_width=True
)
elif page == "Analytics":

    machines = sorted(
        df["machine_id"].unique()
    )

    selected_machine = st.selectbox(
        "Select Machine",
        machines,
        key="analytics_machine"
    )

    machine_df = df[
        df["machine_id"] == selected_machine
    ]

    df_chart = (
        machine_df
        .sort_values("timestamp")
        .tail(20)
    )

    st.subheader(
        f"📊 Analytics Dashboard - {selected_machine}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌡️ Temperature")
        st.line_chart(
            df_chart.set_index("timestamp")[
                "temperature"
            ]
        )

    with col2:
        st.subheader("💧 Humidity")
        st.line_chart(
            df_chart.set_index("timestamp")[
                "humidity"
            ]
        )

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("⚙️ Pressure")
        st.line_chart(
            df_chart.set_index("timestamp")[
                "pressure"
            ]
        )

    with col4:
        st.subheader("📳 Vibration")
        st.line_chart(
            df_chart.set_index("timestamp")[
                "vibration"
            ]
        )

    st.divider()

    st.subheader(
        "📈 Failure Probability Trend"
    )

    st.line_chart(
        df_chart.set_index("timestamp")[
            "probability"
        ]
    )
elif page == "AI Analysis":

    machines = sorted(
        df["machine_id"].unique()
    )

    selected_machine = st.selectbox(
        "Select Machine",
        machines,
        key="ai_machine"
    )

    machine_df = df[
        df["machine_id"] == selected_machine
    ]

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

    st.subheader(
        "🤖 AI Failure Analysis"
    )

    if probability >= 0.9:
        st.error(
            latest["explanation"]
        )

    elif probability >= 0.7:
        st.warning(
            latest["explanation"]
        )

    else:
        st.success(
            latest["explanation"]
        )

    st.divider()

    st.subheader(
        "📝 Latest Prediction Details"
    )

    st.write(
        {
            "machine_id": latest["machine_id"],
            "prediction": int(
                latest["prediction"]
            ),
            "probability": round(
                probability * 100,
                2
            ),
            "status": latest["status"]
        }
    )
elif page == "Alerts":

    alerts = df[
        df["prediction"] == 1
    ]

    st.subheader(
        "🚨 Alert Monitoring Center"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Alerts",
            len(alerts)
        )

    with col2:

        critical = len(
            alerts[
                alerts["probability"] >= 0.9
            ]
        )

        st.metric(
            "Critical Alerts",
            critical
        )

    with col3:

        warning = len(
            alerts[
                (alerts["probability"] >= 0.7)
                &
                (alerts["probability"] < 0.9)
            ]
        )

        st.metric(
            "Warning Alerts",
            warning
        )

    st.divider()

    if not alerts.empty:

        latest_alert = alerts.iloc[0]

        st.error(
            f"""
🚨 Latest Alert

Machine: {latest_alert['machine_id']}

Risk: {latest_alert['probability']*100:.2f}%

Status: {latest_alert['status']}
"""
        )

    st.divider()

    st.subheader(
        "📋 Alert History"
    )

    st.dataframe(
        alerts.head(50),
        use_container_width=True
    )