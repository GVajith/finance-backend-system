FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip setuptools wheel

COPY requirements.docker.txt .

RUN pip install --no-cache-dir --only-binary=:all: -r requirements.docker.txt

COPY app .

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]