from db_setup import check_python
from db_setup import (initialize_database)
from gui import start_gui

if __name__ == "__main__":
# Überprüft, ob eine kompatible Python-Version verwendet wird
    check_python()
# Stellt sicher, dass die Datenbank existiert
    initialize_database()
# Startet die GUI
    start_gui()

