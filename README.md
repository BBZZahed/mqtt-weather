# MQTT Wetterstationen

Dieses Projekt simuliert verteilte Wetterstationen, die Messdaten über MQTT an einen Broker senden.

## Setup

1. Starte alles mit:
   ```bash
   docker-compose up --build
   ```

2. Öffne ein neues Terminal und starte den Subscriber:
   ```bash
   cd subscriber
   pip install -r requirements.txt
   python main.py
   ```

## Aufgabe

- Abonniere Wetterdaten vom Topic `weather`
- Speichere die Daten sinnvoll (z. B. JSON-Datei, SQLite)
- Erstelle einfache Auswertungen (Durchschnitt, Verlauf, usw.)
---

## CI/CD Beschreibung Projektaufgabe

Für das **mqtt-weather-project** wurde ein separates GitHub-Repo erstellt.  
Bei jedem Push auf den `main`-Branch wird automatisch eine **GitHub-Actions-Pipeline** ausgeführt. Diese überprüft den Python-Code mittels Linting (flake8) und erstellt anschliessend ein Docker-Image der Wetterstation.  
Das erstellte Docker-Image wird danach automatisch in ein **Docker-Hub-Repo** publiziert.