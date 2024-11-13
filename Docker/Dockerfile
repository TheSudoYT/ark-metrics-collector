FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY LICENSE /app/
COPY ark_metrics_collector /app/ark_metrics_collector
COPY README.md /app/
COPY setup.py /app/

RUN mkdir data
RUN pip install --no-cache-dir -r requirements.txt && pip install .

EXPOSE 5000

ENTRYPOINT ["sh", "-c", "ark-metrics-collector --config=/app/config.yaml"]
