from db_setup import check_python
from db_setup import (initialize_database)
from gui import start_gui

if __name__ == "__main__":
    check_python()
    initialize_database()
    start_gui()

