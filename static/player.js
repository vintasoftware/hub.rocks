function get_next() {
    $.ajax({
        url: API_URL + '/tracks/next/',
        type: 'GET'
    }).done(function (json) {
        if (json.next) {
            set_now_playing(json.next.deezer_id).then(function () {
                delete_next(json.next.deezer_id);
            });

            DZ.player.playTracks([json.next.deezer_id]);
        } else {
            console.log('no next, will try again...');
            fail();
        }
    }).fail(fail);

    function fail() {
        setTimeout(function () {
            get_next();
        }, 3000);
    }
}

function delete_next(deezer_id) {
    $.ajax({
        url: API_URL + '/tracks/' + deezer_id + '/',
        type: 'DELETE'
    }).done(function () {
        console.log('deleted next');
    });
}

function set_now_playing(deezer_id) {
    return $.ajax({
        url: API_URL + '/tracks/' + deezer_id + '/now-playing/',
        type: 'PUT'
    }).done(function () {
        console.log('set now-playing');
    });
}

function delete_now_playing(deezer_id) {
    $.ajax({
        url: API_URL + '/tracks/' + deezer_id + '/now-playing/',
        type: 'DELETE'
    }).done(function () {
        console.log('deleted now-playing');
    });
}

function onPlayerLoaded() {
    DZ.Event.subscribe('track_end', function (currentIndex) {
        var track = DZ.player.getCurrentTrack();
        delete_now_playing(track.id);
        get_next();
    });
    get_next();
}

DZ.init({
    appId  : '8',
    channelUrl : 'http://developers.deezer.com/examples/channel.php',
    player : {
        container : 'player',
        cover : true,
        playlist : true,
        width : 650,
        height : 300,
        onload : onPlayerLoaded
    }
});
