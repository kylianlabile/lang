console.log("javascript file is linked");

// Function to load exercises
function loadExercises() {
    fetch('YOUR_RENDER_API_URL/list_exercises/')
        .then(response => response.json())
        .then(data => {
            const exerciseList = document.getElementById('exerciseList');
            exerciseList.innerHTML = ''; // Clear previous buttons
            data.exercises.forEach(exercise => {
                const button = document.createElement('button');
                button.textContent = exercise;
                button.addEventListener('click', () => {
                    loadExercise(exercise);
                });
                exerciseList.appendChild(button);
            });
        });
}

// Function to load a specific exercise
function loadExercise(exerciseName) {
    fetch(`YOUR_RENDER_API_URL/get_exercise/${exerciseName}`)
        .then(response => response.json())
        .then(data => {
            const exerciseArea = document.getElementById('exerciseArea');
            const exerciseNameDisplay = document.getElementById('exerciseName');
            const germanSentenceDisplay = document.getElementById('germanSentence');
            exerciseArea.style.display = 'block'; // Show exercise area
            exerciseNameDisplay.textContent = data.name;
            germanSentenceDisplay.textContent = data.german[0]; // Display the first sentence
            exerciseArea.dataset.exerciseName = exerciseName; // Store exercise name
            exerciseArea.dataset.sentenceIndex = 0; // Store sentence index
        });
}

// Function to check the translation
function checkTranslation() {
    const exerciseArea = document.getElementById('exerciseArea');
    const userTranslation = document.getElementById('userTranslation').value;
    const exerciseName = exerciseArea.dataset.exerciseName;
    const sentenceIndex = parseInt(exerciseArea.dataset.sentenceIndex);

    fetch('YOUR_RENDER_API_URL/check_translation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            exercise_name: exerciseName,
            user_translation: userTranslation,
            sentence_index: sentenceIndex
        })
    })
        .then(response => response.json())
        .then(data => {
            const feedback = document.getElementById('feedback');
            feedback.innerHTML = ''; // Clear previous feedback

            if (data.correct) {
                feedback.textContent = data.message;
                exerciseArea.dataset.sentenceIndex = sentenceIndex + 1; // Move to next sentence
                loadExercise(exerciseName); //reload the exercise.
            } else {
                feedback.textContent = data.message + " Correct answer: " + data.correct_translation + " Errors: " + data.errors;
            }
        });
}

// Event listener for the check button
document.getElementById('checkButton').addEventListener('click', checkTranslation);

// Load exercises when the page loads
loadExercises();
