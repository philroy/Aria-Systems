const socket = io();
const chatWindow = document.getElementById('chat-window');
const input = document.getElementById('user-input');

socket.on('response', msg => {
    chatWindow.innerHTML += '<div><b>Aria:</b> ' + msg + '</div>';
});

function sendMessage() {
    const msg = input.value;
    chatWindow.innerHTML += '<div><b>You:</b> ' + msg + '</div>';
    socket.send(msg);
    input.value = '';
}
