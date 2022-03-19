const scroll = $('div.scroll')

$("#text").keypress(function (e) {
    if(e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        $(this).closest("form").submit();
    }
});

socket.on('connect', function () {
    socket.emit('get_messages', {
        event: 'request messages'
    })
    let form = $('form').on('submit', function (e) {
        e.preventDefault()
        let user_name = $('input.username').val()
        let user_input = $('textarea.message').val().trim()
        if (user_input.length > 0) {
            socket.emit('message', {
                sender: user_name,
                text: user_input
            })
        }
        $('textarea.message').val('').focus()
    })
})

socket.on('message_response', function (msg) {
    add_message(msg.sender, msg.text, normalize_date(msg.created_at))
    scroll_down()
})

socket.on('refresh', function () {
    location.reload()
})

socket.on('messages_list_response', function (response) {
    let msg_list = response.data
    for (let msg of msg_list) {
        add_message(msg.sender, msg.text, normalize_date(msg.created_at))
    }
    scroll.append('<div class="text-center"><span class="between">Подключен к чату</span></div>')
    scroll_down()
})

function add_message(user_name, message, time) {
    scroll.append('<div class="d-flex align-items-center">' +
        '<div class="pr-2 pl-1"><span class="name fw-bold">' + user_name + '</span>' +
        '<span class="name">  ' + time + '</span>' +
        '<p class="msg">' + message + '</p></div></div>')
}

function scroll_down() {
    scroll.animate({scrollTop: 20000000}, 'fast')
}

function delete_messages() {
    socket.emit('delete_messages', {
        event: 'delete_messages'
    })
}
