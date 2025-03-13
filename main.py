import difflib
import json
import os

def get_similarity(user_input, correct_translation):
    sequence = difflib.SequenceMatcher(None, user_input, correct_translation)
    return sequence.ratio()

def highlight_errors(user_input, correct_translation):
    diff = difflib.ndiff(user_input, correct_translation)
    highlighted = "".join([f'[{char}]' if char.startswith('-') else char[-1] for char in diff if char.strip()])
    return highlighted

def split_sentences(text):
    return [sentence.strip() for sentence in text.split('. ') if sentence]

def save_exercise(name, german_text, english_text):
    german_sentences = split_sentences(german_text)
    english_sentences = split_sentences(english_text)
    exercise = {"name": name, "german": german_sentences, "english": english_sentences}
    with open(f"{name}.json", "w", encoding="utf-8") as file:
        json.dump(exercise, file, ensure_ascii=False, indent=4)
    print(f"Exercise '{name}' saved successfully!")

def list_exercises():
    files = [f for f in os.listdir() if f.endswith(".json")]
    exercises = {str(i + 1): f[:-5] for i, f in enumerate(files)}
    return exercises

def load_exercise(name):
    try:
        with open(f"{name}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Exercise not found.")
        return None

def translation_exercise(exercise):
    score = 100
    total_sentences = len(exercise["english"])
    correct_count = 0
    
    for i, english_sentence in enumerate(exercise["english"]):
        while True:
            print(f"Translate the following sentence to German:\n{english_sentence}")
            user_translation = input("Your translation: ")
            
            correct_translation = exercise["german"][i]
            similarity = get_similarity(user_translation, correct_translation)
            
            if user_translation == correct_translation:
                print("Correct! Moving to the next sentence.")
                correct_count += 1
                break
            else:
                score -= 10
                highlighted = highlight_errors(user_translation, correct_translation)
                print(f"Incorrect. The correct translation is: {correct_translation}")
                print(f"Your errors highlighted: {highlighted}")
        
        progress = (correct_count / total_sentences) * 100
        print(f"Progress: {progress:.2f}%\n")
    
    print("Exercise complete! Your final score is:", score)

def main():
    print("Translation Learning Program")
    while True:
        choice = input("Would you like to create a new exercise (N) or open an existing one (O)? (Q to quit): ").strip().lower()
        if choice == 'n':
            name = input("Enter a name for your exercise: ").strip()
            english_text = input("Enter a full English paragraph or essay: ").strip()
            german_text = input("Enter the corresponding German translation: ").strip()
            save_exercise(name, german_text, english_text)
        elif choice == 'o':
            exercises = list_exercises()
            if not exercises:
                print("No exercises found.")
                continue
            print("Available Exercises:")
            for num, ex_name in exercises.items():
                print(f"{num}. {ex_name}")
            selection = input("Select an exercise by number: ").strip()
            if selection in exercises:
                exercise = load_exercise(exercises[selection])
                if exercise:
                    translation_exercise(exercise)
            else:
                print("Invalid selection.")
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter 'N', 'O', or 'Q'.")

if __name__ == "__main__":
    main()
