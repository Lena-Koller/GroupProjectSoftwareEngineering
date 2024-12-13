# Finanzplaner

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
    - Standardkategorien wie „Einkommen“, „Lebensmittel“ und „Freizeit“ werden ebenfalls angelegt.

