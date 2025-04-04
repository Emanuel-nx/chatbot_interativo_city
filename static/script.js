const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

function addMessage(message, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight; // Rolagem automática
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Adicionar mensagem do usuário
    addMessage(message, "user");
    userInput.value = "";

    // Enviar mensagem para o servidor
    const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, session_id: "usuario1" })
    });

    const data = await response.json();
    addMessage(data.response, "bot");
}

// Enviar mensagem ao pressionar Enter
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});