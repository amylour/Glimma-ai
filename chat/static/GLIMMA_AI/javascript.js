function chat_ajax() {
    let text = document.querySelector('#userText').value;

    // Display loading spinner
    let loading = document.querySelector('#loading');
    loading.innerHTML = `
    <strong>Loading...</strong>
    <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
    `;

    $.ajax({
        type: 'POST',
        url: '/ajax/',
        data: {
            'text': text
        },
        success: function(res) {
            let response = res.data; // GPT response (hook)
            let postResponse = res.post_data; // Social media post

            let chatCard = document.querySelector('#chatCard');

            // Clear previous chat
            chatCard.innerHTML = '';

            // Display GPT response (hook)
            chatCard.innerHTML += `
            <div class="card-body bg bg-light text-dark">
                <h5 class="card-title">Hook: ${response}</h5>
            </div>
            `;

            // Display Social media post
            chatCard.innerHTML += `
            <div class="card-body bg bg-light text-dark">
                <h5 class="card-title">Post: ${postResponse}</h5>
            </div>
            `;

            // Hide loading spinner
            loading.innerHTML = '';
        },
        error: function(err) {
            console.log("There was an error!", err);
        }
    });

    // Clear input
    document.querySelector('#userText').value = '';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#submitBtn').addEventListener('click', chat_ajax);
});
