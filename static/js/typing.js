var commentTextarea = document.getElementById('comment');
var isTyping = false;
var typingTimer;

commentTextarea.addEventListener('input', function () {
    if (!isTyping) {
        console.log('Пользователь начал печатать');
        isTyping = true;
        chatSocket.send(JSON.stringify({
            'action': 'user_typing',
            'state': 'start'
        }));
    }

    clearTimeout(typingTimer);
    typingTimer = setTimeout(function () {
        console.log('Пользователь перестал печатать');
        isTyping = false;
        chatSocket.send(JSON.stringify({
            'action': 'user_typing',
            'state': 'stop'
        }));
    }, 2000);
});
