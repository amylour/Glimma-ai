// Variable to track the current question index.
let currentQuestionIndex = 0;

// Obtain the total number of question containers.
const totalQuestions = document.querySelectorAll('.question-container').length;

function updateProgressBar() {
    const progressPercentage = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    document.querySelector('.progress-bar').style.width = `${progressPercentage}%`;
}

function displayNextQuestion() {
    // Hide the current question.
    const currentQuestion = document.getElementById(`question-${currentQuestionIndex}`);
    if (currentQuestion) {
        currentQuestion.style.display = 'none';
    } else {
        console.error("Couldn't find the current question in the DOM");
    }

    // Increment the current question index.
    currentQuestionIndex++;

    // If there are no more questions, redirect to chat page
    if (currentQuestionIndex >= totalQuestions) {
        window.location.href = '/chat';
        return;
    }

    // Update the progress bar.
    updateProgressBar();

    // Show the next question.
    const nextQuestion = document.getElementById(`question-${currentQuestionIndex}`);
    if (nextQuestion) {
        nextQuestion.style.display = 'block';
    } else {
        console.error(`Couldn't find the next question with ID 'question-${currentQuestionIndex}' in the DOM`);
    }
}

function submitAnswer(question, answer) {
    console.log(`Submitting answer for question: ${question}, Answer: ${answer}`);

    fetch('/save_answer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ question, answer })
    })
    .then(response => {
        // Check if the response is valid JSON.
        if (response.headers.get("content-type").includes("application/json")) {
            return response.json();
        }
        throw new Error("Received non-JSON response from server.");
    })
    .then(data => {
        if (data.status === 'success') {
            displayNextQuestion();
        } else {
            console.error("Error received from server:", data);
        }
    })
    .catch(error => {
        console.error("An error occurred:", error);
    });
}

function submitTextInput(question, inputId) {
    const userInput = document.getElementById(inputId).value;
    if (!userInput) {
        alert("Please enter your answer.");
        return;
    }
    submitAnswer(question, userInput);
}

function initializeQuiz() {
    // Hide all questions first.
    document.querySelectorAll('.question-container').forEach(question => {
        question.style.display = 'none';
    });

    // Display the first question.
    const firstQuestion = document.getElementById(`question-${currentQuestionIndex}`);
    if (firstQuestion) {
        firstQuestion.style.display = 'block';
    } else {
        console.error(`Couldn't find the first question with ID 'question-0' in the DOM`);
    }
}

// Initialize the quiz by displaying the first question.
document.addEventListener("DOMContentLoaded", function() {
    initializeQuiz();
});
