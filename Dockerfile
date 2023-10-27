FROM python:3.11-slim

WORKDIR /src

COPY ../../requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ../.. .
CMD python -m uvicorn main:app --host 0.0.0.0 --port $PORT