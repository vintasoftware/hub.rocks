(function () {
  var HubrocksAPI = (function () {
    var getNext = function () {
      return $.ajax({
        url: API_URL + '/tracks/next/',
        type: 'GET'
      });
    };

    var deleteNext = function (service_id) {
      return $.ajax({
        url: API_URL + '/tracks/' + service_id + '/',
        type: 'DELETE'
      });
    };

    var setNowPlaying = function (service_id) {
      return $.ajax({
        url: API_URL + '/tracks/' + service_id + '/now-playing/',
        type: 'POST'
      });
    };

    var deleteNowPlaying = function (service_id) {
      $.ajax({
        url: API_URL + '/tracks/' + service_id + '/now-playing/',
        type: 'DELETE'
      });
    };

    return {
      getNext: getNext,
      deleteNext: deleteNext,
      setNowPlaying: setNowPlaying,
      deleteNowPlaying: deleteNowPlaying
    };
  }());

  var popNextAndPlay = function () {
    HubrocksAPI.getNext().done(function (json) {
      if (json.next) {
        HubrocksAPI.setNowPlaying(json.next.service_id)
          .then(function () {
            HubrocksAPI.deleteNext(json.next.service_id);
          });

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
            DZ.Event.subscribe('track_end', function (currentIndex) {
              var track = DZ.player.getCurrentTrack();
              HubrocksAPI.deleteNowPlaying(track.id);
              popNextAndPlay();
            });
            
            popNextAndPlay();
          }
      }
  });  
}());
