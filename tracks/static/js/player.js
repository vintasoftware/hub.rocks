(function () {
  var HubrocksAPI = (function () {

    var skipTrack = function () {
      return $.ajax({
        url: API_URL + '/tracks/now-playing/skip/',
        type: 'POST',
      });
    };

    var getNowPlaying = function () {
      return $.ajax({
        url: API_URL + '/tracks/now-playing/',
        type: 'GET'
      });
    };

    return {
      skipTrack: skipTrack,
      getNowPlaying: getNowPlaying,
    };
  }());

  var popNextAndPlay = function () {

    HubrocksAPI.skipTrack().done(function () {
      console.log('skipping');
      tryNowPlaying();
    }).fail(getFailFunction(popNextAndPlay));

    function tryNowPlaying() {
      HubrocksAPI.getNowPlaying().done(function (now_playing) {
        DZ.player.playTracks([now_playing.service_id]);
      }).fail(function(error) {
        if (error.status === 404) {
          // no track to play next try popping again
          console.log('no next, will try again...');
          getFailFunction(popNextAndPlay)();
        } else {
          // something went wrong with nowPlaying try it again
          console.log(error);
          getFailFunction(tryNowPlaying)();
        }
      });
    }

    function getFailFunction(func) {
      function fail() {
        setTimeout(function () {
          console.log('retrying');
          func();
        }, 3000);
      }
      return fail;
    }
  };


  var tryToContinuePlaying = function () {
    HubrocksAPI.getNowPlaying().done(function (now_playing) {
      DZ.player.playTracks([now_playing.service_id]);
    }).fail(function () {
      popNextAndPlay();
    });
  };

  var skipTrack = function () {
    return HubrocksAPI.skipTrack();
  };

  var faye_client = null;
  if (FANOUT_REALM) {
    faye_client = new Faye.Client(
      'http://' + FANOUT_REALM + '.fanoutcdn.com/bayeux'
    );
  }

  if (FANOUT_REALM) {
    faye_client.subscribe('/player-' + ESTABLISHMENT, function (data) {
      console.log('got data: ', data);
      if (data.service_id) {
        DZ.player.playTracks([data.service_id]);
      } else {
        popNextAndPlay();
      }
    });
  } else {
    console.log("Running without Faye");
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
          onload : function () {
            tryToContinuePlaying();

            DZ.Event.subscribe('track_end', function (currentIndex) {
              skipTrack();
            });
          }
      }
  });  
}());
