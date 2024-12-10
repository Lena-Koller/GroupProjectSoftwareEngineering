import tkinter as tk
from tkinter import messagebox
from db_ops import add_transaction, get_transactions, delete_transaction, get_categories, get_category_stats

displayed_transactions = []

def update_listbox():
    global displayed_transactions
    lb_transactions.delete(0, tk.END)
    trans = get_transactions()
    displayed_transactions = trans

    for i, t in enumerate(trans):
        line = f"ID:{i} | {t[1]} | {t[2]} {t[5]} | {t[3]}"
        if t[4]:
            line += f" ({t[4]})"
        lb_transactions.insert(tk.END, line)

def delete_selected_transaction():
    selection = lb_transactions.curselection()
    if not selection:
        messagebox.showwarning("Fehler", "Bitte eine Transaktion auswählen.")
        return
    selected_index = selection[0]
    db_id = displayed_transactions[selected_index][0]
    delete_transaction(db_id)
    messagebox.showinfo("Info", "Transaktion gelöscht.")
    update_listbox()

def open_transaction_window():
    trans_win = tk.Toplevel(root)
    trans_win.title("Neue Transaktion")

    tk.Label(trans_win, text="Datum (DD.MM.YYYY:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    e_date = tk.Entry(trans_win)
    e_date.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(trans_win, text="Betrag:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    e_amount = tk.Entry(trans_win)
    e_amount.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(trans_win, text="Kategorie:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    cats = get_categories()
    if not cats:
        cats = ["Keine Kategorien vorhanden"]
    cat_var = tk.StringVar()
    cat_var.set(cats[0])
    cat_option = tk.OptionMenu(trans_win, cat_var, *cats)
    cat_option.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    tk.Label(trans_win, text="Beschreibung:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    e_desc = tk.Entry(trans_win)
    e_desc.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(trans_win, text="Währung (z.B. EUR):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    e_curr = tk.Entry(trans_win)
    e_curr.grid(row=4, column=1, padx=5, pady=5)

    def save_transaction():
        date = e_date.get().strip()
        amount = e_amount.get().strip()
        category = cat_var.get()
        desc = e_desc.get().strip()
        curr = e_curr.get().strip()

        if not date or not amount or not category or "Keine Kategorien" in category or not curr:
            messagebox.showwarning("Fehler", "Bitte alle erforderlichen Felder ausfüllen.")
            return
        try:
            amt = float(amount)
        except ValueError:
            messagebox.showwarning("Fehler", "Betrag muss eine Zahl sein.")
            return

        add_transaction(date, amt, category, desc, curr)
        messagebox.showinfo("Info", "Transaktion hinzugefügt.")
        trans_win.destroy()
        update_listbox()

    tk.Button(trans_win, text="Speichern", command=save_transaction).grid(row=5, column=0, columnspan=2, pady=10)

def show_overview():
    category_sums, total_income, total_expenses, difference = get_category_stats()

    overview_win = tk.Toplevel(root)
    overview_win.title("Übersicht")

    tk.Label(overview_win, text="Ausgaben und Einnahmen nach Kategorien:", font=("Arial", 12, "bold")).pack(pady=5)

    frame_cat_sum = tk.Frame(overview_win, padx=10, pady=10)
    frame_cat_sum.pack()
    r = 0
    for cat, val in category_sums.items():
        tk.Label(frame_cat_sum, text=f"{cat}: {val:.2f}").grid(row=r, column=0, sticky="w")
        r += 1

    tk.Label(overview_win, text=f"Gesamt-Einnahmen: {total_income:.2f}", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(overview_win, text=f"Gesamt-Ausgaben: {total_expenses:.2f}", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(overview_win, text=f"Überschuss (Einnahmen - Ausgaben): {difference:.2f}", font=("Arial", 10, "bold")).pack(pady=5)

def start_gui():
    global root, lb_transactions

    root = tk.Tk()
    root.title("Finanzplaner")

    tk.Label(root, text="Willkommen zu Ihrem Finanzplaner!", font=("Arial", 14, "bold")).pack(pady=10)

    frame_trans = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_trans.pack(pady=10, fill="both", expand=True)

    tk.Label(frame_trans, text="Transaktionen:").pack(anchor="w")

    lb_transactions = tk.Listbox(frame_trans, width=80, height=10)
    lb_transactions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_trans)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb_transactions.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lb_transactions.yview)

    frame_buttons = tk.Frame(root, padx=10, pady=10)
    frame_buttons.pack()

    tk.Button(frame_buttons, text="Neue Transaktion hinzufügen", command=open_transaction_window).grid(row=0, column=0, padx=10)
    tk.Button(frame_buttons, text="Ausgewählte Transaktion löschen", command=delete_selected_transaction).grid(row=0, column=1, padx=10)
    tk.Button(frame_buttons, text="Übersicht anzeigen", command=show_overview).grid(row=0, column=2, padx=10)

    update_listbox()

    root.mainloop()
