let options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 10000
};

setInterval(function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPosition, error, options);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}, 10000)


function sendPosition(pos) {
    socket.emit('location', {
        user_id: user_id,
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
    })
}

function error(err) {
    console.warn('ERROR(' + err.code + '): ' + err.message);
}
