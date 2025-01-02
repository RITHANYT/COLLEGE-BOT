const chatLog = document.getElementById("chat-log");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const microphoneBtn = document.getElementById("microphone-btn");
const outputDiv = document.getElementById("output");

sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

microphoneBtn.addEventListener("click", startVoiceInput);

function sendMessage() {
    const userMessage = chatInput.value;
    if (userMessage.trim() === "") {
        return;
    }

    const userMessageElem = document.createElement("div");
    userMessageElem.className = "user-message";
    userMessageElem.innerHTML = `<p class="message-text">${userMessage}</p>`;
    chatLog.appendChild(userMessageElem);
    chatInput.value = "";

    const typingIndicatorElem = document.createElement("div");
    typingIndicatorElem.className = "typing-indicator";
    typingIndicatorElem.innerHTML = "Processing your response...";
    chatLog.appendChild(typingIndicatorElem);

    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botMessageElem = document.createElement("div");
        const botMessage = data.message;
        chatLog.removeChild(typingIndicatorElem);
        botMessageElem.className = "bot-message";
        botMessageElem.innerHTML = `<p class="message-text">${botMessage}</p>`;
        chatLog.appendChild(botMessageElem);
        chatLog.scrollTop = chatLog.scrollHeight;
    })
    .catch(error => console.error(error));    
}

function startVoiceInput() {
    microphoneBtn.disabled = true;

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const voiceInput = event.results[0][0].transcript;
        const userMessageElem = document.createElement("div");
        userMessageElem.className = "user-message";
        userMessageElem.innerHTML = `<p class="message-text">${voiceInput}</p>`;
        chatLog.appendChild(userMessageElem);

        const typingIndicatorElem = document.createElement("div");
        typingIndicatorElem.className = "typing-indicator";
        typingIndicatorElem.innerHTML = "Processing your response...";
        chatLog.appendChild(typingIndicatorElem);

        fetch("/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: voiceInput })
        })
        .then(response => response.json())
        .then(data => {
            const botMessageElem = document.createElement("div");
            const botMessage = data.message;
            chatLog.removeChild(typingIndicatorElem);
            botMessageElem.className = "bot-message";
            botMessageElem.innerHTML = `<p class="message-text">${botMessage}</p>`;
            chatLog.appendChild(botMessageElem);
            chatLog.scrollTop = chatLog.scrollHeight;
            microphoneBtn.disabled = false;
        })
        .catch(error => console.error(error));
    };
}
