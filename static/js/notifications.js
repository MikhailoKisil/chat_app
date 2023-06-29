var username = document.querySelector('.Data').getAttribute('data-username');

const notificationSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/notifications/' +
    username +
    '/'
);

notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    var numberUnreadMsgs = document.getElementById(data["from"]);

    const currentUnreadMsgs = parseInt(numberUnreadMsgs.textContent);

    if (isNaN(currentUnreadMsgs) || currentUnreadMsgs === 0) {
        numberUnreadMsgs.textContent = '1';
    } else {
        numberUnreadMsgs.textContent = (currentUnreadMsgs + 1).toString();
    }
};


