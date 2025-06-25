# Wybierz oficjalny obraz Pythona jako bazowy
FROM python:3.11-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik requirements.txt do katalogu roboczego
COPY requirements.txt .

# Zainstaluj wymagane pakiety
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj pozostałą część aplikacji do katalogu roboczego
COPY . .

# Zmienna środowiskowa dla Flask, aby nie uruchamiać aplikacji w trybie deweloperskim
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Ustaw port do nasłuchiwania w kontenerze (domyślnie Flask działa na porcie 5000)
EXPOSE 5000

# Uruchom aplikację Flask za pomocą Gunicorn (lepsza opcja niż uruchamianie przez 'python main.py')
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
