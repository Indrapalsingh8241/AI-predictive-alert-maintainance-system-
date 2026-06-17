FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install requests pandas numpy

CMD ["python","sensor_generator.py"]