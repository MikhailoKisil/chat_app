var roomName = document.querySelector('.Data-rn').getAttribute('data-room_name');
var from_user_id = parseInt(document.querySelector('.Data-fui').getAttribute('data-from_user_id'));
var to_user_id = parseInt(document.querySelector('.Data-tui').getAttribute('data-to_user_id'));
var userStatusSpan = document.querySelector('.heading-online')
var conversationDiv = document.getElementById('conversation');
var messages;

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onopen = function (e) {
    getMessages();
    chatSocket.send(JSON.stringify({
        'action': 'read',
    }));
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data['message']['command'] === 'messages') {
        messages = data['message']['messages'].slice(20);
        for (let i = 0; i < 20; i++) {
            showMessage(data['message']['messages'][i], true);
        }
    } else if (data['message']['command'] === 'read') {
        if (data['message']['reader_pk'] === to_user_id) {
            var senderDivs = document.querySelectorAll('.sender');

            senderDivs.forEach(function (senderDiv) {
                var messageInfoDiv = senderDiv.querySelector('.message-info');

                if (messageInfoDiv && messageInfoDiv.textContent.trim() === '') {
                    messageInfoDiv.textContent = '✔';
                }
            });
        }
    } else if (data['message']['command'] === 'user_typing') {
        if (data['message']['from_user_pk'] === to_user_id) {
            console.log('typing...')
            userStatusSpan.textContent = data['message']['state']
        }
    } else {
        showMessage(data['message'], false);
    }
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#comment').focus();
document.querySelector('#comment').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#comment');
    const message = messageInputDom.value.trim();
    if (message !== '') {
        chatSocket.send(JSON.stringify({
            'action': 'new_message',
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
            'message': message
        }));
        notificationSocket.send(JSON.stringify({
            'to_user_id': to_user_id,
        }));
        messageInputDom.value = '';
    }
};

function getMessages() {
    chatSocket.send(JSON.stringify({'action': 'get_messages'}));
}

function showMessage(message, prepend) {
    var rowDiv = document.createElement('div');
    rowDiv.className = 'row message-body';

    var colDiv = document.createElement('div');
    if (message.from_user_id === from_user_id) {
        colDiv.className = 'col-sm-12 message-main-sender';
    } else {
        colDiv.className = 'col-sm-12 message-main-receiver';
    }

    var senderDiv = document.createElement('div');
    if (message.from_user_id === from_user_id) {
        senderDiv.className = 'sender';
    } else {
        senderDiv.className = 'receiver';
    }

    var messageInfoDiv = document.createElement('div');
    messageInfoDiv.className = 'message-info';
    if (message.read && message.from_user_id === from_user_id) {
        messageInfoDiv.textContent = '✔';
    } else {
        messageInfoDiv.textContent = '';
    }

    var messageTextDiv = document.createElement('div');
    messageTextDiv.className = 'message-text';
    messageTextDiv.textContent = message.content;

    var messageTimeSpan = document.createElement('span');
    messageTimeSpan.className = 'message-time pull-right';
    messageTimeSpan.textContent = message.timestamp;

    senderDiv.appendChild(messageTextDiv);
    senderDiv.appendChild(messageTimeSpan);
    senderDiv.appendChild(messageInfoDiv);
    colDiv.appendChild(senderDiv);
    rowDiv.appendChild(colDiv);

    if (prepend) {
        conversationDiv.prepend(rowDiv);
    } else {
        conversationDiv.appendChild(rowDiv);
    }


}

function loadMessages(){
    var previousScrollHeight = conversationDiv.scrollHeight;

    for (let i = 0; i < 20; i++) {
        showMessage(messages[i], true);
    }
    messages = messages.slice(20);
    var newScrollHeight = conversationDiv.scrollHeight;
    conversationDiv.scrollTop = newScrollHeight - previousScrollHeight;
}

conversationDiv.addEventListener('scroll', function () {
    if (conversationDiv.scrollTop === 0) {
        loadMessages();
    }
});

window.addEventListener('beforeunload', function () {
    chatSocket.close();
});

