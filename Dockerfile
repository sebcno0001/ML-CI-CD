
FROM python:3.9-slim

# katalog roboczy
WORKDIR /app

# kopiowanie plikow aplikacji
COPY . .

# instalowanie zależności 
RUN pip install --no-cache-dir -r requirements.txt

# otwieranie portu
EXPOSE 8000

# start serwera
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
