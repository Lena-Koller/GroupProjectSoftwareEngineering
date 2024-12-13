# Finanzplaner
Ein benutzerfreundliches Finanzverwaltungstool, mit dem man seine Ausgaben, Einnahmen und Transaktionen im Blick behalten kann. Mit zusätzlichen Funktionen wie Währungsumrechnung und Wechselkursübersicht lassen sich die Ausgaben noch effizienter organisieren.

FEATURES:
- Hinzufügen neuer Transaktionen (inkl. Datum, Betrag, Kategorie und Beschreibung).
- Löschen von Transaktionen.
- Anzeigen einer Liste aller Transaktionen.
- Wechselkurs-Integration
- Abrufen aktueller Wechselkurse basierend auf der Frankfurter API.
- Konvertieren von Beträgen zwischen verschiedenen Währungen.
- Übersicht der Einnahmen und Ausgaben nach Kategorien.
- Berechnung des Überschusses (Einnahmen - Ausgaben).
- Benutzerfreundliche Oberfläche
- Intuitive GUI auf Basis von Tkinter.


VORAUSSETZUNGEN:
1. Python-Version:
    - Das Programm erfordert mindestens Python 3.10. Beim Start überprüft das Programm automatisch deine Python-Version. 
    - Wenn deine Version nicht kompatibel ist, erhältst Du eine Anleitung zur Aktualisierung.
   


2. Python Package Installer:
    - Führe in der Kommandozeile oder im Terminal folgenden Befehl aus: 'pip --version'. 
    - Falls eine Fehlermeldung wie 'pip: command not found' oder Ähnliches erscheint, ist pip nicht installiert.
    - Installiere pip mit 'python -m ensurepip --upgrade'.


3. Benötigte Python-Module:
    - requests: Für die Nutzung der Wechselkurs-API. Installiere es mit 'pip install requests',
    - tinkter: Wird standardmäßig mit Python geliefert. Falls es nicht vorhanden ist, installiere es über den Paketmanager,
    - sqlite3: SQLite ist standardmäßig in Python integriert.


4. Initialisierung der Datenbank:
    - Beim ersten Start wird automatisch eine SQLite-Datenbank (finanzplaner.db) erstellt, falls diese noch nicht existiert. 

5. API-Nutzung
   - Für die Nutzung des Währungsumrechners und Wechselkurse ist eine Internetverbindung erforderlich.


ANWENDUNG:
1. Starte die Anwendung: Ein Hauptfenster wird angezeigt, das Zugriff auf alle Funktionen bietet.

2. Funktionen nutzen:

    - Transaktionen verwalten: Füge neue Transaktionen hinzu oder lösche bestehende Einträge.
    - Wechselkurse anzeigen: Sieh dir aktuelle Wechselkurse basierend auf EUR an.
    - Währungen umrechnen: Konvertiere Beträge zwischen verschiedenen Währungen.
    - Übersicht anzeigen: Analysiere deine Einnahmen und Ausgaben nach Kategorien.



TECHNISCHE DETAILS:
 1. Hauptmodule:
    - tkinter für GUI-Interaktionen.
    - sqlite3 für die Datenbank.
    - requests für API-Abfragen.
      
2. Datenbankstruktur:

    - Tabelle transactions: Speichert alle Transaktionen mit Details wie Datum, Betrag, Kategorie, Beschreibung und Währung.
    - Tabelle categories: Enthält Standardkategorien und deren Einkommensstatus.
   
