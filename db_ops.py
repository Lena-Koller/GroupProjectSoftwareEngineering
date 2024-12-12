import sqlite3  # SQLite-Bibliothek importieren, um mit einer SQLite-Datenbank zu interagieren

# Neue Transaktion hinzufügen
def add_transaction(date, amount, category, description, currency):
    """
    Parameter:
        date (str): Datum der Transaktion (im Format DD.MM.YYYY)
        amount (float): Betrag der Transaktion
        category (str): Kategorie der Transaktion (z. B. "Lebensmittel", "Einkommen")
        description (str): Beschreibung der Transaktion
        currency (str): Währung der Transaktion (z. B. "EUR", "USD")
    """

# Verbindung zur SQLite-Datenbank herstellen
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
# SQL-Befehl zum Einfügen einer neuen Zeile in die Tabelle 'transactions'
        cursor.execute("""
        INSERT INTO transactions (date, amount, category, description, currency)
        VALUES (?, ?, ?, ?, ?)
        """, (date, amount, category, description, currency))
        conn.commit()  # Änderungen in der Datenbank speichern

# Funktion: Alle Transaktionen abrufen
def get_transactions():
    """
    Rückgabewert:
        list: Liste aller Transaktionsdatensätze aus der Datenbank
    """
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
# SQL-Befehl, um alle Zeilen aus der Tabelle 'transactions' abzurufen
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()  # Alle Ergebnisse zurückgeben

# Funktion: Transaktion löschen
def delete_transaction(transaction_id):
    with sqlite3.connect("finanzplaner.db") as conn:  # Verbindung zur SQLite-Datenbank herstellen
        cursor = conn.cursor()
# SQL-Befehl, um eine Transaktion anhand ihrer ID zu löschen
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()  # Änderungen in der Datenbank speichern

# Funktion: Neue Kategorie hinzufügen
def add_category(name):

    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()  # Änderungen in der Datenbank speichern
            return True  # Erfolgreiches Hinzufügen
        except sqlite3.IntegrityError:  # Fehlerbehandlung für Duplikate
            return False  # Fehler, Kategorie existiert bereits

# Funktion: Alle Kategorien abrufen
def get_categories():
    """
    Ruft alle Kategorien aus der Tabelle 'categories' ab und gibt sie alphabetisch sortiert zurück.

    Rückgabewert:
        list: Alphabetisch sortierte Liste der Kategoriennamen.
    """
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        # SQL-Befehl, um alle Kategorien alphabetisch sortiert abzurufen
        cursor.execute("SELECT name FROM categories ORDER BY name")
        rows = cursor.fetchall()
        return [r[0] for r in rows]  # Nur die Namen der Kategorien zurückgeben

# Funktion: Statistik zu Kategorien abrufen
def get_category_stats():
    """
    Berechnet die Gesamtsumme der Beträge jeder Kategorie sowie Einkommens- und Ausgabenstatistiken.

    Rückgabewert:
        tuple: Ein Tuple mit folgenden Werten:
            - category_sums (dict): Dictionary mit Kategorien und deren Gesamtsummen.
            - total_income (float): Gesamteinnahmen (Summe aller Transaktionen der Kategorie "Einkommen").
            - total_expenses (float): Gesamtausgaben (Summe aller Transaktionen außer "Einkommen").
            - difference (float): Differenz zwischen Einnahmen und Ausgaben.
    """
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        # SQL-Befehl, um die Summe der Beträge pro Kategorie zu berechnen
        cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        rows = cursor.fetchall()

    category_sums = {}  # Dictionary für Kategorien und deren Gesamtsummen
    for cat, s in rows:
        category_sums[cat] = s if s is not None else 0.0  # Null-Werte durch 0.0 ersetzen

    # Berechnung der Gesamteinnahmen, Gesamtausgaben und der Differenz
    total_income = category_sums.get("Einkommen", 0.0)  # Einnahmen (Kategorie "Einkommen")
    total_expenses = sum(s for c, s in category_sums.items() if c != "Einkommen")  # Summe der Ausgaben
    difference = total_income - total_expenses  # Differenz zwischen Einnahmen und Ausgaben

    return category_sums, total_income, total_expenses, difference
