# GroupProjectSoftwareEngineering
Final Group Profect for Introduction to Software Engineering course
# Pub Quiz Tool

Überblick
Das Pub Quiz Tool ist ein interaktives Quizspiel, das sowohl im Einzelspieler- als auch im Mehrspielermodus genutzt werden kann. Es ermöglicht den Benutzern, Fragen aus einer JSON-Datei zu laden und nach Kategorien zu filtern. Die Spieler können ihr Wissen testen, Punkte sammeln und sich mit anderen Spielern messen.

---

## Funktionen

1. Einzelspielermodus
   Spielen Sie ein Quiz mit zufälligen Fragen. Die maximale Anzahl der Fragen pro Runde beträgt standardmäßig 5 (kann aber durch die Verfügbarkeit der Fragen in der Kategorie begrenzt sein).

2. Kategoriefilterung  
   Wählen Sie eine spezifische Kategorie, um sich nur auf die Fragen dieser Kategorie zu konzentrieren.

3. Mehrspielermodus  
   Spielen Sie gegen Freunde. Jeder Spieler erhält eine feste Anzahl von Fragen (standardmäßig 3) und Punkte werden individuell gezählt.

4. Fragenverwaltung  
   Fragen können in einer JSON-Datei gespeichert und geladen werden. Jede Frage enthält eine Kategorie, mehrere Antwortmöglichkeiten und die richtige Antwort.

---

## Voraussetzungen

- Python
- Eine gültige JSON-Datei mit den Fragen (siehe Struktur unten).

---

## JSON-Dateistruktur
Die Datei `questions.json` muss das folgende Format haben:

```json
{
    "Kategorie1": [
        {
            "question": "Frage 1?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        },
        {
            "question": "Frage 2?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option B"
        }
    ],
    "Kategorie2": [
        {
            "question": "Frage 1?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option C"
        }
    ]
}
```

---

## Verwendung

### Start des Programms
Führen Sie die Datei aus:

```bash
python quiz.py
```

### Menü
Nach dem Start sehen Sie das Hauptmenü:

```
Pub Quiz Tool
1. Einzelspiel Quiz starten
2. Mehrspeilermodus starten
3. Kategorie wählen
4. Beenden
```

1. Einzelspiel Quiz starten: Startet ein zufälliges Quiz mit allen verfügbaren Fragen.  
2. Mehrspielermodus starten: Startet ein Multiplayer-Quiz. Geben Sie die Spielernamen als kommagetrennte Liste ein.  
3. Kategorie wählen: Zeigt verfügbare Kategorien an und ermöglicht es, ein Quiz mit Fragen aus nur einer Kategorie zu spielen.  
4. Beenden: Beendet das Programm.

### Fragen beantworten
Jede Frage wird mit vier Antwortmöglichkeiten angezeigt. Wählen Sie die richtige Antwort, indem Sie die entsprechende Nummer eingeben.

Beispiel:

```
Frage: Was ist die Hauptstadt von Frankreich?
1: Paris
2: London
3: Berlin
4: Madrid
Wähle eine Option (1-4): 
```

### Punktestand
Nach jeder Runde wird der Punktestand angezeigt:

```
Dein Punktestand: 3/5
```

Im Mehrspielermodus wird am Ende eine Übersicht der Punkte aller Spieler ausgegeben:

```
Endergebnis:
Alice: 2
Bob: 3
```

---

## Anpassungen

### Rundenanzahl ändern
Die Standardanzahl von Runden kann im Code durch folgende Variablen angepasst werden:

```python
roundsSingleplayer = 5
roundsMultiplayer = 3
```

### Fragen hinzufügen
Fügen Sie neue Fragen direkt zur `questions.json`-Datei hinzu. Achten Sie darauf, dass jede Frage eine Kategorie, Optionen und eine richtige Antwort hat.

---

## Fehlerbehebung

1. Fragen konnten nicht geladen werden 
   - Überprüfen Sie, ob die `questions.json`-Datei im korrekten Format vorliegt.
   - Stellen Sie sicher, dass die Datei sich im selben Verzeichnis wie das Skript befindet.

2. Ungültige Auswahl 
   - Geben Sie nur die angezeigten Nummern für Optionen und Menüauswahlen ein.

---

## Erweiterungsmöglichkeiten

- Online-Modus: Fragen aus einer Datenbank oder API laden.  
- Zeitlimit: Begrenzte Zeit für jede Antwort.  

---

## Lizenz
Dieses Projekt ist Open Source und steht unter der MIT-Lizenz. Feel free to use and modify!
