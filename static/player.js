function get_next() {
    $.ajax({
        url: API_URL + '/tracks/next/',
        type: 'GET'
    }).done(function (json) {
        if (json.next) {
            console.log('got next ' + JSON.stringify(json.next));
            //DZ.player.addToQueue([json.next.deezer_id]);
            delete_next(json.next.deezer_id);

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


$(document).ready(function(){
    $("#controlers input").attr('disabled', true);
    $("#slider_seek").click(function(evt,arg){
        var left = evt.offsetX;
        DZ.player.seek((evt.offsetX/$(this).width()) * 100);
    });
});
function event_listener_append() {
    var pre = document.getElementById('event_listener');
    var line = [];
    for (var i = 0; i < arguments.length; i++) {
        line.push(arguments[i]);
    }
    pre.innerHTML += line.join(' ') + "\n";
}
function onPlayerLoaded() {
    $("#controlers input").attr('disabled', false);
    event_listener_append('player_loaded');
    
    DZ.Event.subscribe('track_end', function(currentIndex) {
        console.log(currentIndex);
        if (DZ.player.getCurrentIndex() === DZ.player.getTrackList().length - 1) {
            get_next();
        }
    });
    get_next();
    
    DZ.Event.subscribe('player_position', function(arg){
        event_listener_append('position', arg[0], arg[1]);
        $("#slider_seek").find('.bar').css('width', (100*arg[0]/arg[1]) + '%');
    });
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
