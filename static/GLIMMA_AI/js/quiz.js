// Variable to track the current question index.
let currentQuestionIndex = -1;

// Obtain the total number of question containers.
const totalQuestions = document.querySelectorAll('.question-container').length;

// Function to update the progress bar based on the current question index.
function updateProgressBar() {
    const progressPercentage = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    document.querySelector('.progress-bar').style.width = `${progressPercentage}%`;
}

// Function to display the next question.
function displayNextQuestion() {
    // Hide the current question.
    const currentQuestion = document.getElementById(`question-${currentQuestionIndex}`);
    if (currentQuestion) {
        currentQuestion.style.display = 'none';
    }

    // Increment the current question index.
    currentQuestionIndex++;

    // Show the next question.
    const nextQuestion = document.getElementById(`question-${currentQuestionIndex}`);
    if (nextQuestion) {
        nextQuestion.style.display = 'block';
    } else {
        console.warn("No more questions to display.");
    }

    // Update the progress bar.
    updateProgressBar();
}

// Function to submit the answer and make an API call.
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

// Initialize the quiz by displaying the first question.
document.addEventListener("DOMContentLoaded", function() {
    displayNextQuestion();
});
