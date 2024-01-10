document.getElementById('user-input').addEventListener('keypress', function (e) {
    // Check if the pressed key is Enter
    if (e.key === 'Enter') {
        // Call the sendMessage function
        sendMessage();
    }
});

function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatBox = document.getElementById('chat-box');

    // Append user message to the chat box
    chatBox.innerHTML += '<div class = "user-message-body"><div class = "user-message-container"><div class="user-message">' + userInput + '</div></div></div>';

    // Make an AJAX request to the server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ask', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Parse the JSON response from the server
            var response = JSON.parse(xhr.responseText);

            // Append bot's response to the chat box
            chatBox.innerHTML += '<div class = "bot-message-container"><div class="bot-message">' + response.response + '</div></div>';

            // Clear the user input field
            document.getElementById('user-input').value = '';

            // Scroll the chat box to the bottom to show the latest messages
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    };
    xhr.send('user_input=' + userInput);
}

