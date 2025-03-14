from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import difflib
import json
import os

app = FastAPI()

class ExerciseInput(BaseModel):
    name: str
    german_text: str
    english_text: str

class TranslationInput(BaseModel):
    exercise_name: str
    user_translation: str
    sentence_index: int

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

def list_exercises():
    files = [f for f in os.listdir() if f.endswith(".json")]
    return [f[:-5] for f in files]

def load_exercise(name):
    try:
        with open(f"{name}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

@app.post("/create_exercise/")
def create_exercise(exercise: ExerciseInput):
    save_exercise(exercise.name, exercise.german_text, exercise.english_text)
    return {"message": f"Exercise '{exercise.name}' created successfully!"}

@app.get("/list_exercises/")
def get_exercises():
    exercises = list_exercises()
    return {"exercises": exercises}

@app.get("/get_exercise/{name}")
def get_exercise(name: str):
    exercise = load_exercise(name)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@app.post("/check_translation/")
def check_translation(data: TranslationInput):
    exercise = load_exercise(data.exercise_name)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if data.sentence_index >= len(exercise["english"]):
        raise HTTPException(status_code=400, detail="Invalid sentence index")
    
    correct_translation = exercise["german"][data.sentence_index]
    if data.user_translation == correct_translation:
        return {"correct": True, "message": "Correct! Moving to the next sentence."}
    else:
        highlighted = highlight_errors(data.user_translation, correct_translation)
        return {"correct": False, "message": "Incorrect translation.", "correct_translation": correct_translation, "errors": highlighted}

@app.get("/")
def root():
    return {"message": "Translation Learning API is running!"}
