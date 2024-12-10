import os
import sqlite3

def initialize_database():
    db_exists = os.path.exists("finanzplaner.db")

    conn = sqlite3.connect("finanzplaner.db")
    cursor = conn.cursor()

    # Tabelle für Transaktionen
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

    # Tabelle für Kategorien mit is_income_category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        is_income_category INTEGER NOT NULL DEFAULT 0
    )
    """)

    conn.commit()

    # Standardkategorien
    standard_kategorien = [
        ("Einkommen", 1),
        ("Lebensmittel", 0),
        ("Haushalt", 0),
        ("Mobilität", 0),
        ("Freizeit", 0),
        ("Versicherungen", 0),
        ("Sonstiges", 0)
    ]
    for cat, inc in standard_kategorien:
        try:
            cursor.execute("INSERT INTO categories (name, is_income_category) VALUES (?, ?)", (cat, inc))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    if not db_exists:
        print("Neue Datenbank wurde erstellt, da zum jetzigen Zeitpunkt noch keine existiert.")
        return True
    else:
        print("Bestehende Datenbank wird verwendet.")
        return False
