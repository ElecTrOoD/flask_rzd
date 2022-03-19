setTimeout( function initMap() {
    window.initial_coords = {lat: 52.033428, lng: 113.500911};
    if (users) {
        if (users.length === 1) {
            window.initial_coords = {lat: users[0].geo_lat, lng: users[0].geo_long};
        }
    }


    window.map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: initial_coords,
        pixelRatio: window.devicePixelRatio || 1
    });

    for (let user of users) {
        const content = '<h6>' + user.first_name + ' ' + user.last_name + '</h6>' +
            '<div class="text-center">' + normalize_date(user.geo_updated_at) + '</div>'

        let infowindow = new google.maps.InfoWindow({
            content: content,
            maxWidth: 200,
        });

        let marker = new google.maps.Marker({
            position: {lat: user.geo_lat, lng: user.geo_long},
            map,
            title: user.username
        });

        marker.addListener("click", () => {
            infowindow.open({
                anchor: marker,
                map,
                shouldFocus: true,
            });
        });
    }
}, 1000)