import json
import random

# Count of rounds for singleplayer and multiplayer
roundsSingleplayer = 5
roundsMultiplayer = 3

# Load and save questions
def load_questions(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file)
        questions = []
        for category, qs in data.items():
            for q in qs:
                q['category'] = category
                questions.append(q)
        return questions

def save_questions(filename, data):
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def play_quiz(questions):
    score = 0
    random.shuffle(questions)  # Shuffle questions to ensure randomness
    for i in range(min(roundsSingleplayer, len(questions))):
        question = questions[i]
        print(f"Frage: {question['question']}")
        
        shuffled_options = question['options'].copy()
        random.shuffle(shuffled_options)
        
        print(f"Optionen: " + ", ".join(shuffled_options))
        answer = input("Deine Antwort: ")
        if answer.strip().lower() == question['answer'].strip().lower():
            print("Richtig! \n")
            score += 1
        else:
            print(f"Falsch! Die richtige Antwort war: {question['answer']} \n")
    print(f"Dein Punktestand: {score}/{roundsSingleplayer}")

def filter_by_category(questions, category):
    return [q for q in questions if q['category'] == category]

def multiplayer_mode(questions, players):
    scores = {player: 0 for player in players}
    random.shuffle(questions)  # Shuffle questions to ensure randomness
    question_index = 0
    for player in players:
        print(f"{player}'s Runde!")
        score = 0
        for _ in range(min(roundsMultiplayer, len(questions) - question_index)):  # Ensure we don't go out of bounds
            question = questions[question_index]
            question_index += 1
            print(f"\nFrage: {question['question']}")
            print(f"Optionen: " + ", ".join(question['options']))
            answer = input(f"{player}, deine Antwort: ")
            if answer.strip().lower() == question['answer'].strip().lower():
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

    while True:
        print("\nPub-Quiz-Tool")
        print("1. Quiz starten")
        print("2. Kategorie auswählen")
        print("3. Multiplayer-Modus")
        print("4. Beenden")
        choice = input("Wähle eine Option: ")
        
        if choice == '1':
            try:
                play_quiz(questions)
            except Exception as e:
                print(f"Fehler beim Starten des Quiz: {e}")
        elif choice == '2':
            print("Verfügbare Kategorien: ", set(q['category'] for q in questions))
            category = input("Kategorie: ")
            try:
                filtered_questions = filter_by_category(questions, category)
                play_quiz(filtered_questions)
            except Exception as e:
                print(f"Fehler beim Filtern der Fragen: {e}")
        elif choice == '3':
            players = input("Spieler (kommagetrennt): ").split(',')
            try:
                multiplayer_mode(questions, players)
            except Exception as e:
                print(f"Fehler im Multiplayer-Modus: {e}")
        elif choice == '4':
            print("Danke fürs Spielen!")
            break
        else:
            print("Ungültige Auswahl!")

main()