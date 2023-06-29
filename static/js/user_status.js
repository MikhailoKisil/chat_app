const headingOnline = document.querySelector('.heading-online');
const url = headingOnline.getAttribute('data-url');
let friend_pk = parseInt(headingOnline.getAttribute('data-friend_pk'));

fetch(url)
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Сталась помилка');
        }
    })
    .then(data => {
        headingOnline.textContent = data.status;
    })
    .catch(error => {
        console.error(error);
    });

let userStatusSocket;
function connectUserStatusSocket () {
    userStatusSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + 'userstatus'
            + '/'
        );

    userStatusSocket.onopen = function (e) {
        userStatusSocket.send(JSON.stringify({
            'status': 'Online'
        }));
    };

    userStatusSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data['user_status']['user_pk'] === friend_pk) {
            headingOnline.textContent = data['user_status']['status'];
        }
    };
}

connectUserStatusSocket();

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        connectUserStatusSocket();
    } else if (document.visibilityState === 'hidden') {
        userStatusSocket.close();
    }
});

window.addEventListener('focus', function() {
    connectUserStatusSocket();
});

window.addEventListener('blur', function() {
    userStatusSocket.close();
});



