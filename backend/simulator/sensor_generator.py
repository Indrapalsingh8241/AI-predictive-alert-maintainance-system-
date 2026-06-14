import random
import time
import requests

API_URL = "http://127.0.0.1:8000/sensor-data"
machine_status = {
    "M101": "RUNNING",
    "M102": "RUNNING",
    "M103": "RUNNING",
    "M104": "RUNNING"
}
   
while True:

    temperature = round(random.uniform(90, 100), 2)
    pressure = round(random.uniform(10, 50), 2)
    vibration = round(random.uniform(0, 10), 2)
    humidity = round(random.uniform(20, 90), 2)
    voltage = round(random.uniform(210, 250), 2)
    current = round(random.uniform(1, 20), 2)

    if temperature > 85 and vibration > 6:
        failure = 1
    else:
        failure = 0

    machine_id = random.choice(list(machine_status.keys()))

    if machine_status[machine_id] == "STOPPED":
        print(f"{machine_id} is stopped")
        continue

    data = {
        "machine_id":machine_id,
        "temperature": temperature,
        "pressure": pressure,
        "vibration": vibration,
        "humidity": humidity,
        "voltage": voltage,
        "current": current,
      
    }

    response = requests.post(
        API_URL,
        json=data
    )
    print("Sent:", data)
    print("Status:", response.status_code)
    result = response.json()

    machine_status[machine_id] = result["status"]
   

    time.sleep(5)