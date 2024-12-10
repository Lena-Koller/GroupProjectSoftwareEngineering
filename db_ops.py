import sqlite3

def add_transaction(date, amount, category, description, currency):
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (date, amount, category, description, currency)
        VALUES (?, ?, ?, ?, ?)
        """, (date, amount, category, description, currency))
        conn.commit()

def get_transactions():
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()

def delete_transaction(transaction_id):
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()

def add_category(name):
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_categories():
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        rows = cursor.fetchall()
        return [r[0] for r in rows]

def get_category_stats():
    """
    Berechnet Summe aller Transaktionen für anschließende Übersicht
    """
    with sqlite3.connect("finanzplaner.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        rows = cursor.fetchall()

    category_sums = {}
    for cat, s in rows:
        category_sums[cat] = s if s is not None else 0.0

    total_income = category_sums.get("Einkommen", 0.0)
    total_expenses = sum(s for c, s in category_sums.items() if c != "Einkommen")
    difference = total_income - total_expenses

    return category_sums, total_income, total_expenses, difference
