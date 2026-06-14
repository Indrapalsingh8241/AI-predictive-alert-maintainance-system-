

def check_alert(machine_id, failure_probability, explanation):

    THRESHOLD = 0.80

    if failure_probability >= THRESHOLD:

        alert_message = f"""
🚨 INDUSTRIAL ALERT

Machine ID: {machine_id}

Failure Probability: {failure_probability:.2%}

Reason:
{explanation}

Action:
Inspect machine immediately.
"""

        return alert_message

    return None