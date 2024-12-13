import os  # Importiert das os-Modul, um Funktionen wie os.path.exists() zu nutzen.
import sqlite3  # Importiert SQLite, ein eingebettetes Datenbanksystem.


def check_python():  # Überprüft die Python-Version, um sicherzustellen, dass das Programm korrekt ausgeführt wird.
    import sys  # Importiert das sys-Modul, um auf Versionsinformationen von Python zuzugreifen.
    if sys.version_info.major < 3 :  # Prüft, ob die Hauptversion von Python kleiner als 3.1 ist.
        print('''
        Dieses Programm erfordert Python 3.1 (oder aktuellere Version), um korrekt ausgeführt zu werden.

        So installieren Sie die neue Version:

        1. Gehen Sie auf die offizielle Website von Python: https://www.python.org.
        2. Navigieren Sie zum Bereich "Downloads" und wählen Sie die Version für Ihr Betriebssystem aus (Windows, macOS oder Linux).
        3. Laden Sie die Installationsdatei herunter.
            - Für Windows: Laden Sie die .exe-Datei herunter.
            - Für macOS: Laden Sie die .pkg-Datei herunter.
            - Für Linux: Installieren Sie Python über Ihren Paketmanager oder durch Kompilierung aus dem Quellcode.
        4. Führen Sie das Installationsprogramm aus.
        5. Folgen Sie den Anweisungen des Installationsassistenten.
        6. Nach der Installation überprüfen Sie, ob Python korrekt installiert wurde:
            - Öffnen Sie eine Kommandozeile oder ein Terminal.
            - Geben Sie python --version oder python3 --version ein.
            - Es sollte die aktuellste Version angezeigt werden. ''')  # Zeigt eine detaillierte Anleitung zur Installation von Python <3.1

        sys.exit(1)  # Beendet das Programm, wenn die Python-Version nicht kompatibel ist

# Initialisiert die SQLite-Datenbank
def initialize_database():
    db_exists = os.path.exists("finanzplaner.db")  # Prüft, ob die Datenbankdatei "finanzplaner.db" bereits existiert.
    conn = sqlite3.connect(
        "finanzplaner.db")
    cursor = conn.cursor()

# Erstellt die Tabelle "transactions", falls sie noch nicht existiert
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        date TEXT NOT NULL,  
        amount REAL NOT NULL,  
        category TEXT NOT NULL,  
        description TEXT,  
        currency TEXT NOT NULL  
    )
    """)

# Erstellt die Tabelle "categories", falls sie noch nicht existiert
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        name TEXT UNIQUE NOT NULL,  
        is_income_category INTEGER NOT NULL DEFAULT 0     )
    """)

    conn.commit()  # Speichert die Änderungen in der Datenbank

    # Definiert Standardkategorien und deren Einkommensstatus
    standard_kategorien = [
        ("Einkommen", 1),  # Einkommenskategorie.
        ("Lebensmittel", 0),  # Ausgabenkategorie.
        ("Haushalt", 0),  # Ausgabenkategorie.
        ("Mobilität", 0),  # Ausgabenkategorie.
        ("Freizeit", 0),  # Ausgabenkategorie.
        ("Versicherungen", 0),  # Ausgabenkategorie.
        ("Sonstiges", 0)  # Ausgabenkategorie.
    ]

    # Fügt die Standardkategorien in die Tabelle ein, wenn sie noch nicht existieren
    for cat, inc in standard_kategorien:
        try:
            cursor.execute("INSERT INTO categories (name, is_income_category) VALUES (?, ?)", (cat, inc))
        except sqlite3.IntegrityError:
            pass

    conn.commit()  # Speichert die Änderungen in der Datenbank.
    conn.close()  # Schließt die Verbindung zur Datenbank.

# Falls die Datenbank neu erstellt wurde
    if not db_exists:
        print("Neue Datenbank wurde erstellt, da zum jetzigen Zeitpunkt noch keine existiert.")
        return True  # Gibt zurück, dass eine neue Datenbank erstellt wurde.
    else:  # Falls die Datenbank bereits existierte.
        print("Bestehende Datenbank wird verwendet.")
        return False  # Gibt zurück, dass eine bestehende Datenbank verwendet wird.

