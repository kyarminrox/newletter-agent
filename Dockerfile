# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY frontend/ ./frontend/
EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
