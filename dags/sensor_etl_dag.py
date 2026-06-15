from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal

from backend.app.airflow_databse import SessionLocal1
from backend.app.model_pred import PredictionLog
from backend.services.prediction_service import predict_sensor

from backend.alerts.alert_engine import check_alert
from backend.alerts.telegram_alert import send_telegram_alert







def process_latest_sensor():

    db: Session = SessionLocal()

    try:
        machines = (
            db.query(PredictionLog.machine_id)
            .distinct()
            .all()
                        )

        for (machine_id,) in machines:

            latest = (
            db.query(PredictionLog)
            .filter(PredictionLog.machine_id == machine_id)
            .order_by(PredictionLog.timestamp.desc())
            .first()
                     )

            prediction, probability, explanation = predict_sensor(latest)

            print(
            f"Machine: {latest.machine_id}, "
            f"Prediction: {prediction}, "
            f"Probability: {probability:.2%}"
        )

            alert_message = check_alert(
            machine_id=latest.machine_id,
            failure_probability=probability,
            explanation=explanation
        )

            if alert_message:
                send_telegram_alert(alert_message)
                print("Telegram alert sent")

    finally:
        db.close()


with DAG(
    dag_id="predictive_alert_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["predictive-maintenance"],
) as dag:

    prediction_task = PythonOperator(
        task_id="predict_and_alert",
        python_callable=process_latest_sensor,
    )




def generate_daily_report():

    db: Session = SessionLocal1()

    try:

        records = db.query(PredictionLog).all()

        total_records = len(records)

        total_alerts = len([
            r for r in records
            if r.prediction == 1
        ])

        running = len([
            r for r in records
            if r.status == "RUNNING"
        ])

        warning = len([
            r for r in records
            if r.status == "WARNING"
        ])

        stopped = len([
            r for r in records
            if r.status == "STOPPED"
        ])

        avg_risk = (
            sum(r.probability for r in records)
            / total_records
            if total_records > 0 else 0
        )

        report = f"""
🏭 DAILY FACTORY REPORT

📊 Total Records: {total_records}
🚨 Total Alerts: {total_alerts}

🟢 Running Machines: {running}
🟠 Warning Machines: {warning}
🔴 Stopped Machines: {stopped}

📈 Average Risk: {avg_risk:.2%}
"""

        send_telegram_alert(report)

        print(report)

    finally:
        db.close()


with DAG(
    dag_id="daily_factory_report",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["report"],
) as dag:

    report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_daily_report
    )