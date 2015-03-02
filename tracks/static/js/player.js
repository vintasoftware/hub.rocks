(function () {
  var HubrocksAPI = (function () {
    var getNext = function () {
      return $.ajax({
        url: API_URL + '/tracks/next/',
        type: 'GET'
      });
    };

    var getNowPlaying = function () {
      return $.ajax({
        url: API_URL + '/tracks/now-playing/',
        type: 'GET'
      });
    };

    var setNowPlaying = function (service_id) {
      return $.ajax({
        url: API_URL + '/tracks/now-playing/',
        type: 'PUT',
        data: {
          'service_id': service_id,
          'now_playing': true
        }
      });
    };

    var deleteNowPlaying = function (service_id) {
      return $.ajax({
        url: API_URL + '/tracks/now-playing/',
        type: 'DELETE'
      });
    };

    return {
      getNext: getNext,
      getNowPlaying: getNowPlaying,
      setNowPlaying: setNowPlaying,
      deleteNowPlaying: deleteNowPlaying
    };
  }());

  var popNextAndPlay = function () {
    HubrocksAPI.getNext().done(function (json) {
      if (json.next) {
        HubrocksAPI.setNowPlaying(json.next.service_id);

        DZ.player.playTracks([json.next.service_id]);
      } else {
        console.log('no next, will try again...');
        fail();
      }
    }).fail(fail);

    function fail() {
      setTimeout(function () {
        popNextAndPlay();
      }, 3000);
    }
  };

  var tryToContinuePlaying = function () {
    HubrocksAPI.getNowPlaying().done(function (now_playing) {
      DZ.player.playTracks([now_playing.service_id]);
    }).fail(function () {
      popNextAndPlay();
    });
  };

  var deleteNowPlaying = function (track_id) {
    return HubrocksAPI.deleteNowPlaying(track_id);
  };

  DZ.init({
      appId  : '8',
      channelUrl : 'http://developers.deezer.com/examples/channel.php',
      player : {
          container : 'player',
          cover : true,
          playlist : true,
          width : 650,
          height : 300,
          onload : function () {
            tryToContinuePlaying();

            DZ.Event.subscribe('track_end', function (currentIndex) {
              var track = DZ.player.getCurrentTrack();
              
              deleteNowPlaying(track.id).done(function () {
                popNextAndPlay();
              })
            });
          }
      }
  });  
}());
