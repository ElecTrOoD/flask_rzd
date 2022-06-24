ymaps.ready(init);

function init() {
    let initialCoords = [52.033428, 113.500911];
    if (users) {
        if (users.length === 1) {
            initialCoords = [users[0].geo_lat, users[0].geo_long];
        }
    }

    $("#placeholder").remove()

    let map = new ymaps.Map("map", {
        center: initialCoords,
        zoom: 13
    });

    for (let user of users) {
        let newUserPlacemark = new ymaps.Placemark([user.geo_lat, user.geo_long], {
            balloonContentHeader: user.first_name + ' ' + user.last_name,
            balloonContentBody: normalize_date(user.geo_updated_at),
            hintContent: user.username
        }, {
            preset: 'islands#redPersonIcon'
        });

        map.geoObjects.add(newUserPlacemark);

    }
}