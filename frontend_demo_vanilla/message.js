function sendMessage() {
    var message = document.getElementById("user-message").value;
    var chatbox = document.querySelector(".chatbot-messages");
    if (message.trim() == "") {
        return false;
    }

    var messageElement = document.createElement("div");
    messageElement.innerHTML = "<p>" + message + "</p>";
    messageElement.classList.add("sent"); // Add class for outgoing messages
    chatbox.appendChild(messageElement);

    //waits for message to render, then scroll to bottom of convo
    setTimeout(function() {
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 100);

    // Clear message input field
    document.getElementById("user-message").value = "";

    return false;
}

window.onload = function() {
    // Get a reference to the form element
    var form = document.querySelector("form");
  
    // Add an event listener function to the form
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // prevent the form from submitting

        sendMessage(); // call the sendMessage function
    });
};