// this has to be accessed by the youtube script
var onYouTubeIframeAPIReady = null;

(function () {
  var HubrocksAPI = (function () {

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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


  var FayeInit = (function () {
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
          playTrack(data);
        } else {
          popNextAndPlay();
        }
      });
    } else {
      console.log("Running without Faye");
    }
  })();


  var YoutubeBackend = (function () {
    var ready = false;
    var player = null;

    // this needs to be exposed
    onYouTubeIframeAPIReady = function() {
      player = new YT.Player('youtube-player', {
        height: '390',
        width: '640',
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
        }
      });
      function onPlayerReady(event) {
        ready = true;
      }

      function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.ENDED) {
          skipTrack().fail(popNextAndPlay);
        }
      }
    };

    var playTrack = function (track) {
      player.loadVideoById(track.service_id);
    };

    var stopNowPlaying = function () {
      player.stopVideo();
    };

    var isReady = function () {
      return ready;
    };

    return {
      playTrack: playTrack,
      stopNowPlaying: stopNowPlaying,
      isReady: isReady
    };
  }());


  var DeezerBackend = (function() {
    var ready = false;

    DZ.init({
        appId  : '8',
        channelUrl : 'http://developers.deezer.com/examples/channel.php',
        player : {
            container : 'deezer-player',
            cover : true,
            playlist : true,
            width : 650,
            height : 300,
            onload : function () {
              ready = true;

              DZ.Event.subscribe('track_end', function (currentIndex) {
                skipTrack().fail(popNextAndPlay);
              });
            }
        }
    });


    var playTrack = function (track) {
      DZ.player.playTracks([track.service_id]);
    };

    var stopNowPlaying = function () {
      DZ.player.pause();
    };

    var isReady = function () {
      return ready;
    };

    return {
      playTrack: playTrack,
      stopNowPlaying: stopNowPlaying,
      isReady: isReady
    };
  }());

  function playTrack(track) {
    if (track.service == 'deezer') {
      YoutubeBackend.stopNowPlaying();
      DeezerBackend.playTrack(track);
    } else {
      DeezerBackend.stopNowPlaying();
      YoutubeBackend.playTrack(track);
    }
  }

  var popNextAndPlay = function () {

    HubrocksAPI.skipTrack().done(function () {
      console.log('skipping');
      tryNowPlaying();
    }).fail(getFailFunction(popNextAndPlay));

    function tryNowPlaying() {
      HubrocksAPI.getNowPlaying().done(function (now_playing) {
        playTrack(now_playing);
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
      playTrack(now_playing);
    }).fail(function () {
      popNextAndPlay();
    });
  };

  var skipTrack = function () {
    return HubrocksAPI.skipTrack();
  };


  // ENTRY POINT
  $(document).ready(function(){
    // wait for players to be ready
    (function waitForPlayersReady() {
      setTimeout(function () {
        console.log('waiting for all players to be ready');
        if (DeezerBackend.isReady()) {
          console.log("deezer ready!");
        }
        if (YoutubeBackend.isReady()) {
          console.log("youtube ready!");
        }
        if (!DeezerBackend.isReady() || !YoutubeBackend.isReady()) {
          waitForPlayersReady();
        } else {
          tryToContinuePlaying();
        }
      }, 3000);
    })();
  });

}());
