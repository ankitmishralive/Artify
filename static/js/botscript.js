

// function toggleChatbot() {
//     const chatbotWindow = document.getElementById('chatbot-window');
//     chatbotWindow.classList.toggle('hidden');
// }



document.addEventListener('DOMContentLoaded', function () {
    var chatbotFormBtn = document.getElementById('chatbot-form-btn');
    var chatbotForm = document.getElementById('chatbot-form');
    var messageText = document.getElementById('messageText');

    const chatPanel = document.getElementById("chatPanel");
    const chatToggleBtn = document.getElementById("chatToggleBtn");

    chatToggleBtn.addEventListener("click", function () {
        chatPanel.classList.toggle("hidden");
    });

    chatbotFormBtn.addEventListener('click', function (e) {
        e.preventDefault();
        sendMessage();
    });

    chatbotForm.addEventListener('submit', function (e) {
        e.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var message = messageText.value;
        var mediaList = document.querySelector('.media-list');

        var userMessageElement = document.createElement('li');
        userMessageElement.className = 'media';
        userMessageElement.innerHTML = '<div class="media-body"><div class="media"><div style="text-align:right; color:white" class="media-body">' +
            message + '<hr/></div></div></div>';

        mediaList.appendChild(userMessageElement);

        // Make a Fetch API POST request to the Flask endpoint
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'messageText': message,
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Clear the input text after sending the message
            document.getElementById('messageText').value = '';

            var answerMessageElement = document.createElement('li');
            answerMessageElement.className = 'media';
            answerMessageElement.innerHTML = '<div class="media-body"><div class="media"><div style="color:white" class="media-body">' +
                data.answer + '<hr/></div></div></div>';

            mediaList.appendChild(answerMessageElement);

            var chatPanel = document.getElementById('chatPanel');
            chatPanel.scrollTop = chatPanel.scrollHeight;
        })
        .catch(error => {
            console.log(error);
        });
    }
});
