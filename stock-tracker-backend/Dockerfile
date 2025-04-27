# Dockerfile

# 1. Basis-Image: ein kleines Python-Image nehmen
FROM python:3.11-slim

# 2. Arbeitsverzeichnis im Container setzen
WORKDIR /app

# 3. Anforderungen kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Den Rest der App kopieren
COPY . .

# 5. Port freigeben (optional aber gut)
EXPOSE 5000

# 6. Startbefehl
CMD ["python", "app.py"]
