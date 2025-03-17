console.log("javascript file is linked");

function loadExercises() {
    fetch('https://lang-q7ua.onrender.com/list_exercises/')
        .then(response => response.json())
        .then(data => {
            // ...
        });
}

function loadExercise(exerciseName) {
    fetch(`https://lang-q7ua.onrender.com/get_exercise/${exerciseName}`)
        .then(response => response.json())
        .then(data => {
            // ...
        });
}

function checkTranslation() {
    // ...
    fetch('https://lang-q7ua.onrender.com/check_translation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            // ...
        })
    })
        .then(response => response.json())
        .then(data => {
            // ...
        });
}

// ...
