function ajaxSend(url, params) {
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

const forms = document.querySelector('form[name=search_friend]');

forms.addEventListener('submit', function (e) {
    e.preventDefault();
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function render(data) {
    let template = Hogan.compile(html);
    // let output = template.render(data);

    let output = '';

    if (data.users.length > 0) {
        output = template.render(data);
    } else {
        output = '<h4>Нікого не знайдено :(</h4>';
    }

    const div = document.querySelector('.row.sideBar');
    div.innerHTML = output;
}

let html = '\
{{#users}}\
    <a href="{{ chat_room }}" class="LinkFriend">\
        <div class="row sideBar-body">\
            <div class="col-sm-3 col-xs-3 sideBar-avatar">\
                <div class="avatar-icon">\
                    <img src="{{ avatar }}">\
                </div>\
            </div>\
            <div class="col-sm-9 col-xs-9 sideBar-main">\
                <div class="row">\
                    <div class="col-sm-8 col-xs-8 sideBar-name">\
                        <span class="name-meta">{{ username }}</span>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </a>\
{{/users}}'