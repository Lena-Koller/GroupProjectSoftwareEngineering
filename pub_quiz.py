import json
import random
import tkinter as tk
from tkinter import messagebox
 
# Festlegen der Anzahl von Runden für Einzelspieler und Mehrspieler
roundsSingleplayer = 5
roundsMultiplayer = 3
questionsjson = 'questions.json' # Variable definiert
 
# Funktion zum Laden von Fragen aus einer JSON-Datei
def load_questions(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
            questions = []
            if not isinstance(data, dict):
                raise ValueError("Datenstruktur ist nicht wie erwartet. Es sollte ein Wörterbuch sein.")
 
            for category, qs in data.items():
                if not isinstance(qs, list):
                    raise ValueError(f"Erwartet eine Liste von Fragen in der Kategorie {category}, gefunden {type(qs)}.")
                for q in qs:
                    if not ('question' in q and 'options' in q and 'answer' in q):
                        raise ValueError("Jede Frage muss 'question', 'options' und 'answer' enthalten.")
                    q['category'] = category
                    questions.append(q)
            return questions
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei {filename} wurde nicht gefunden.")
    except json.JSONDecodeError:
        raise ValueError("JSON-Daten konnten nicht geparst werden. Überprüfen Sie die Datei auf Fehler.")
    except Exception as e:
        raise Exception(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
 
 
# Hauptklasse für die Quiz-Anwendung
class QuizApp:
    # Initialisierung der QuizApp-Klasse
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.score = 0
        self.current_question_index = 0
        self.selected_category = None
        self.players = []
        self.current_player_index = 0
        self.multiplayer_scores = {}
 
        self.root.title("Pub Quiz")
 
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)
 
        self.title_label = tk.Label(self.main_frame, text="Pub Quiz", font=("Arial", 24))
        self.title_label.pack(pady=10)
 
        self.start_single_button = tk.Button(self.main_frame, text="Einzelspieler Quiz starten", command=self.start_quiz)
        self.start_single_button.pack(pady=5)
 
        self.start_multi_button = tk.Button(self.main_frame, text="Mehrspielermodus starten", command=self.start_multiplayer_setup)
        self.start_multi_button.pack(pady=5)
 
        self.category_button = tk.Button(self.main_frame, text="Kategorie wählen", command=self.choose_category)
        self.category_button.pack(pady=5)
 
        self.quit_button = tk.Button(self.main_frame, text="Beenden", command=self.root.destroy)
        self.quit_button.pack(pady=5)
 
    # Startet den Einzelspieler-Quizmodus
    def start_quiz(self):
        random.shuffle(self.questions)
        self.score = 0
        self.current_question_index = 0
        self.questions = self.questions[:roundsSingleplayer]  # Ensure the number of questions is limited
        self.selected_option = tk.StringVar(value="")  # Ensure no option is selected by default
        self.show_question()
 
    # Öffnet ein Setup-Fenster für den Mehrspielermodus
    def start_multiplayer_setup(self):
        setup_window = tk.Toplevel(self.root)
        setup_window.title("Spieler einrichten")
 
        tk.Label(setup_window, text="Spielernamen eingeben (kommagetrennt):").pack(pady=10)
        player_entry = tk.Entry(setup_window)
        player_entry.pack(pady=5)
 
        tk.Button(
            setup_window,
            text="Starten",
            command=lambda: self.setup_multiplayer(player_entry.get(), setup_window)
        ).pack(pady=10)
 
    # Initialisiert die Spieler und startet den Mehrspielermodus
    def setup_multiplayer(self, player_input, setup_window):
        players = [player.strip() for player in player_input.split(',') if player.strip()]
        if not players:
            messagebox.showerror("Fehler", "Es müssen mindestens ein Spieler eingegeben werden!")
            return
        if len(set(players)) != len(players):
            messagebox.showerror("Fehler", "Duplikate in den Spielernamen gefunden! Jeder Spielername muss einzigartig sein.")
            return
 
        setup_window.destroy()
        self.multiplayer_quiz = MultiplayerQuiz(self.root, self.questions, players)
        self.multiplayer_quiz.start()
 
    # Ermöglicht die Auswahl einer Kategorie
    def choose_category(self):
        categories = list(set(q['category'] for q in self.questions))
        self.selected_category = tk.StringVar(value=categories[0])
 
        category_window = tk.Toplevel(self.root)
        category_window.title("Kategorie wählen")
 
        tk.Label(category_window, text="Wähle eine Kategorie:").pack(pady=10)
        for category in categories:
            tk.Radiobutton(
                category_window,
                text=category,
                variable=self.selected_category,
                value=category
            ).pack(anchor="w")
 
        tk.Button(
            category_window,
            text="Bestätigen",
            command=lambda: [self.filter_questions(), category_window.destroy()]
        ).pack(pady=10)
 
    # Filtert die Fragen basierend auf der gewählten Kategorie
    def filter_questions(self):
        if not self.selected_category:
            messagebox.showerror("Fehler", "Keine Kategorie ausgewählt!")
            return
 
        category = self.selected_category.get()
        filtered_questions = [q for q in self.questions if q['category'] == category]
        if not filtered_questions:
            messagebox.showerror("Fehler", "Keine Fragen in dieser Kategorie gefunden!")
            return
        
        self.questions = filtered_questions
 
    # Zeigt eine Frage an (Singleplayer oder Multiplayer)
    def show_question(self, multiplayer=False):
        if self.current_question_index >= len(self.questions):
            self.display_results(multiplayer=multiplayer)
            return
 
        question = self.questions[self.current_question_index]
        shuffled_options = question['options'].copy()
        random.shuffle(shuffled_options)
 
        self.clear_frame()
 
        if multiplayer:
            player = self.players[self.current_player_index]
            tk.Label(self.main_frame, text=f"Spieler: {player}", font=("Arial", 16)).pack(pady=5)
 
        tk.Label(self.main_frame, text=f"Frage {self.current_question_index + 1}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text=question['question'], wraplength=400).pack(pady=10)
 
        self.selected_option.set("")  # Ensure no option is selected by default
        for option in shuffled_options:
            tk.Radiobutton(
                self.main_frame,
                text=option,
                variable=self.selected_option,
                value=option
            ).pack(anchor="w", pady=5)
 
        tk.Button(
            self.main_frame,
            text="Bestätigen",
            command=lambda: self.check_answer(multiplayer)
        ).pack(pady=10)
 
    # Überprüft die Antwort und aktualisiert den Spielstand
    def check_answer(self, multiplayer):
        question = self.questions[self.current_question_index]
        selected = self.selected_option.get()
 
        if multiplayer:
            player = self.players[self.current_player_index]
            if selected == question['answer']:
                self.multiplayer_scores[player] += 1
                messagebox.showinfo("Richtig!", "Das war die richtige Antwort!")
            else:
                messagebox.showerror("Falsch!", f"Die richtige Antwort war: {question['answer']}")
 
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if self.current_player_index == 0:
                self.current_question_index += 1
            self.start_multiplayer_quiz()
        else:
            if selected == question['answer']:
                self.score += 1
                messagebox.showinfo("Richtig!", "Das war die richtige Antwort!")
            else:
                messagebox.showerror("Falsch!", f"Die richtige Antwort war: {question['answer']}")
            self.current_question_index += 1
            self.show_question()
 
    # Zeigt die Ergebnisse des Einzelspieler-Quiz an
    def show_results(self):
        self.clear_frame()
 
        tk.Label(self.main_frame, text="Quiz beendet!", font=("Arial", 16)).pack(pady=10)
        tk.Label(
            self.main_frame,
            text=f"Dein Punktestand: {self.score}/{min(roundsSingleplayer, len(self.questions))}",
            font=("Arial", 14)
        ).pack(pady=10)
 
        tk.Button(
            self.main_frame,
            text="Zurück zum Hauptmenü",
            command=self.reset_quiz
        ).pack(pady=10)
 
    # Zeigt die Ergebnisse des Mehrspieler-Quiz an
    def show_multiplayer_results(self):
        self.clear_frame()
 
        tk.Label(self.main_frame, text="Multiplayer Ergebnis", font=("Arial", 16)).pack(pady=10)
        for player, score in self.multiplayer_scores.items():
            tk.Label(self.main_frame, text=f"{player}: {score}", font=("Arial", 14)).pack(pady=5)
 
        tk.Button(
            self.main_frame,
            text="Zurück zum Hauptmenü",
            command=self.reset_quiz
        ).pack(pady=10)
 
    # Setzt das Quiz zurück und kehrt zum Hauptmenü zurück
    def reset_quiz(self):
        self.clear_frame()
        self.reset_variables()
        self.create_main_menu()
 
    # Setzt die Variablen der Anwendung auf ihre Standardwerte zurück
    def reset_variables(self):
        self.questions = load_questions(questionsjson)  # Änderung auf Variable
        self.score = 0
        self.current_question_index = 0
        self.selected_category = None
        self.players = []
        self.multiplayer_scores = {}
        self.current_player_index = 0
 
    # Erstellt das Hauptmenü der Anwendung
    def create_main_menu(self):
        self.__init__(self.root, self.questions)
 
    # Entfernt alle Widgets aus dem aktuellen Frame
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
 
    # Zeigt die Ergebnisse an (Singleplayer oder Multiplayer)
    def display_results(self, multiplayer=False):
        self.clear_frame()
 
        if multiplayer:
            title_text = "Multiplayer Ergebnis"
            score_text = "\n".join(f"{player}: {score}" for player, score in self.multiplayer_scores.items())
        else:
            title_text = "Quiz beendet!"
            score_text = f"Dein Punktestand: {self.score}/{min(roundsSingleplayer, len(self.questions))}"
 
        tk.Label(self.main_frame, text=title_text, font=("Arial", 16)).pack(pady=10)
        results_label = tk.Label(self.main_frame, text=score_text, font=("Arial", 14))
        results_label.pack(pady=10)
 
        tk.Button(
            self.main_frame,
            text="Zurück zum Hauptmenü",
            command=self.reset_quiz
        ).pack(pady=10)

class MultiplayerQuiz:
    def __init__(self, root, questions, players):
        self.root = root
        self.questions = questions
        self.players = players
        self.current_player_index = 0
        self.current_question_index = 0
        self.scores = {player: 0 for player in players}
        self.selected_option = tk.StringVar(value="")

    def start(self):
        random.shuffle(self.questions)
        self.questions = self.questions[:roundsMultiplayer]
        self.show_question()

    def show_question(self):
        if self.current_question_index >= len(self.questions):
            self.display_results()
            return

        question = self.questions[self.current_question_index]
        shuffled_options = question['options'].copy()
        random.shuffle(shuffled_options)

        self.clear_frame()

        player = self.players[self.current_player_index]
        tk.Label(self.root, text=f"Spieler: {player}", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.root, text=f"Frage {self.current_question_index + 1}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=question['question'], wraplength=400).pack(pady=10)

        self.selected_option.set("")
        for option in shuffled_options:
            tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected_option,
                value=option
            ).pack(anchor="w", pady=5)

        tk.Button(
            self.root,
            text="Bestätigen",
            command=self.check_answer
        ).pack(pady=10)

    def check_answer(self):
        question = self.questions[self.current_question_index]
        selected = self.selected_option.get()
        player = self.players[self.current_player_index]

        if selected == question['answer']:
            self.scores[player] += 1
            messagebox.showinfo("Richtig!", "Das war die richtige Antwort!")
        else:
            messagebox.showerror("Falsch!", f"Die richtige Antwort war: {question['answer']}")

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.current_question_index += 1
        self.show_question()

    def display_results(self):
        self.clear_frame()
        tk.Label(self.root, text="Multiplayer Ergebnis", font=("Arial", 16)).pack(pady=10)
        for player, score in self.scores.items():
            tk.Label(self.root, text=f"{player}: {score}", font=("Arial", 14)).pack(pady=5)
        tk.Button(
            self.root,
            text="Zurück zum Hauptmenü",
            command=self.root.destroy
        ).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Hauptprogramm
# Hauptfunktion der Anwendung
def main():
    questions = None
 
    try:
        questions = load_questions(questionsjson)  # Änderung auf Variable
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden der Fragen: {e}")
        return
 
    root = tk.Tk()
    QuizApp(root, questions)
    root.geometry('500x500')  # größeres Ausgabefenster UI
    root.mainloop()
 
if __name__ == "__main__":
    main()