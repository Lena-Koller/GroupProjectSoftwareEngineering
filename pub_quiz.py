import json
import random

# Festlegen der Anzahl von Runden für Einzelspieler und Mehrspieler
roundsSingleplayer = 5
roundsMultiplayer = 3

# Funktion zum Laden von Fragen aus einer JSON-Datei
def load_questions(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file)
        questions = []
        # Iterieren durch jede Kategorie und Frage, wobei Kategorieinformationen zu jeder Frage hinzugefügt werden
        for category, qs in data.items():
            for q in qs:
                q['category'] = category
                questions.append(q)
        return questions

# Funktion zum Speichern von Fragen in einer JSON-Datei
def save_questions(filename, data):
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Hauptfunktion zum Spielen des Quiz
def play_quiz(questions):
    score = 0
    total_questions = len(questions)
    rounds = min(roundsSingleplayer, total_questions)  # Maximale Rundenanzahl an die verfügbare Anzahl Fragen anpassen
    random.shuffle(questions)  # Fragen mischen für zufällige Reihenfolge
    
    for i in range(rounds):
        question = questions[i]
        print(f"Frage: {question['question']}")

        # Optionen mischen und mit Nummern präsentieren
        shuffled_options = question['options'].copy()
        random.shuffle(shuffled_options)
        options_dict = {str(index + 1): option for index, option in enumerate(shuffled_options)}
        print(" \n".join([f"{k}: {v}" for k, v in options_dict.items()]))
        answer = input("Wähle eine Option (1-4): ")
        if options_dict.get(answer.strip()) == question['answer']:
            print("Richtig! \n")
            score += 1
        else:
            print(f"Falsch! Die richtige Antwort war: {question['answer']} \n")
    print(f"Dein Punktestand: {score}/{rounds}")

# Funktion zum Filtern von Fragen nach Kategorie
def filter_by_category(questions, category):
    return [q for q in questions if q['category'] == category]

# Funktion für den Mehrspielermodus
def multiplayer_mode(questions, players):
    scores = {player: 0 for player in players}
    random.shuffle(questions)  # Fragen für Zufälligkeit mischen
    question_index = 0
    # Durchspieler rotieren, jedem eine feste Anzahl von Fragen zuweisen
    for player in players:
        print(f"Runde von {player}!")
        score = 0
        for _ in range(min(roundsMultiplayer, len(questions) - question_index)):
            question = questions[question_index]
            question_index += 1
            print(f"\nFrage: {question['question']}")

            shuffled_options = question['options'].copy()
            random.shuffle(shuffled_options)
            options_dict = {str(index + 1): option for index, option in enumerate(shuffled_options)}
            print("Optionen: " + ", ".join([f"{k}: {v}" for k, v in options_dict.items()]))
            answer = input(f"{player}, deine Antwort (Nummer): ")
            if options_dict.get(answer.strip()) == question['answer']:
                score += 1
        scores[player] = score
    print("Endergebnis:")
    for player, score in scores.items():
        print(f"{player}: {score}")

def main():
    questions = None

    try:
        questions = load_questions('questions.json')
    except Exception as e:
        print(f"Fehler beim Laden der Fragen aus 'questions.json': {e}")
        try:
            questions = load_questions('PubQuiz/questions.json')
        except Exception as e:
            print(f"Fehler beim Laden der Fragen aus 'PubQuiz/questions.json': {e}")
            print("Fragen konnten nicht geladen werden.")
            return

    # Hauptprogrammschleife für Benutzerinteraktion
    while True:
        print("\nPub Quiz Tool")
        print("1. Quiz starten")
        print("2. Kategorie wählen")
        print("3. Mehrspielermodus")
        print("4. Beenden")
        choice = input("Wähle eine Option: ")
        
        if choice == '1':
            try:
                play_quiz(questions)
            except Exception as e:
                print(f"Fehler beim Starten des Quiz: {e}")
        elif choice == '2':
            print("Verfügbare Kategorien: ", set(q['category'] for q in questions))
            category = input("Kategorie wählen: ")
            try:
                filtered_questions = filter_by_category(questions, category)
                play_quiz(filtered_questions)
            except Exception as e:
                print(f"Fehler beim Filtern der Fragen: {e}")
        elif choice == '3':
            players = input("Spieler (kommagetrennt eingeben): ").split(',')
            try:
                multiplayer_mode(questions, players)
            except Exception as e:
                print(f"Fehler im Mehrspielermodus: {e}")
        elif choice == '4':
            print("Danke fürs Spielen!")
            break
        else:
            print("Ungültige Auswahl!")

main()

