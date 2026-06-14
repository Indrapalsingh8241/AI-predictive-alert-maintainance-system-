from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_explanation(sensor, prediction):

    prompt = f"""
    Temperature: {sensor.temperature}
    Pressure: {sensor.pressure}
    Vibration: {sensor.vibration}
    Humidity: {sensor.humidity}
    Voltage: {sensor.voltage}
    Current: {sensor.current}

    Prediction: {prediction}

    Explain:
    - Why this happened
    - Risk level
    - Recommended action

    Keep it concise.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content