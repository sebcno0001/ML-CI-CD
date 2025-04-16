FROM python:3.10-slim

# Praca z katalogiem roboczym
WORKDIR /app

# Skopiuj zależności i zainstaluj je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj całą aplikację
COPY . .

# Komenda uruchamiająca API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
