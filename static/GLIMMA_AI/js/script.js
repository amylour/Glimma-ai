document.addEventListener("DOMContentLoaded", function() {

    // Utility function: hides the content from one div and shows another.
    function switchContent(hideID, showID) {
        document.getElementById(hideID).style.display = "none";
        document.getElementById(showID).style.display = "block";
        document.getElementById("back-arrow").style.display = "block";
    }


    // This function sends the selected answer to the server to save it.
    function saveAnswer(question, answer) {
        fetch('/save_answer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token for security.
            },
            body: `question=${question}&answer=${answer}`
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
    }

    // Helper function to get a cookie's value, used above to retrieve the CSRF token.
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Starting the quiz
    document.getElementById("get-started").addEventListener("click", function() {
        switchContent("initial-content", "question-1-content");
    });

    for (let i = 1; i <= 6; i++) {
        let questionContent = document.getElementById(`question-${i}-content`);

        questionContent.querySelectorAll(".options button").forEach(btn => {
            btn.addEventListener("click", function() {
                saveAnswer(`Question ${i}`, this.innerText);

                if (i < 6) {
                    switchContent(`question-${i}-content`, `question-${i+1}-content`);
                } else {
                    switchContent(`question-${i}-content`, "gpt-content");
                }
            });
        });
    }

    // The 'Generate' button sends user input to the server and displays GPT's response.
    document.getElementById("generate").addEventListener("click", function() {
        const userInput = document.getElementById("user_input").value;

        fetch('/gpt/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token for security.
            },
            body: `user_input=${userInput}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("gpt-output").innerText = data.output;
            document.getElementById("editable-output").value = data.output;
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
    });

    // When the back arrow is clicked, hide all question divs and show the initial content.
    document.getElementById("back-arrow").addEventListener("click", function() {
        this.style.display = "none";
        document.getElementById("initial-content").style.display = "block";
        for (let i = 1; i <= 6; i++) {
            document.getElementById(`question-${i}-content`).style.display = "none";
        }
        document.getElementById("gpt-content").style.display = "none";
    });

});
