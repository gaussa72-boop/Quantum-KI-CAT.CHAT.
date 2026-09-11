# Quantum-KI-CAT.CHAT.

Quantum-Cat-Chat-Prototyp mit Flask, OpenAI und SQLite.

## Bereinigung
Der beschädigte doppelte `main.py` wurde entfernt und `app.py` zum einzigen Backend-Einstiegspunkt gemacht. Secrets werden nicht mehr im Code hinterlegt; `OPENAI_API_KEY`, `SECRET_KEY`, `OPENAI_MODEL` und `PORT` kommen aus der Umgebung.
