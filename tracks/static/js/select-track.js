$(document).ready(function () {
  function transformDeezerTracksJson(tracks) {
    return $.map(tracks, function (t) {
      return {
        id: 'deezer;' + t.id,
        title: t.title,
        artist: t.artist.name,
        cover: t.album.cover,
        service: 'deezer',
      };
    });
  }

  function transformYoutubeJson(tracks) {
    return $.map(tracks, function (t) {
      return {
        id: 'youtube;' + t.id.videoId,
        title: t.snippet.title,
        artist: t.snippet.channelTitle,
        cover: t.snippet.thumbnails.default.url,
        service: 'youtube'
      };
    });
  }

  $('.vote-form').on('submit', function () {
    // necessary to prevent submit with 
    // selectize custom submit
    return false;
  });

  selectizedInput = $('.select-track').selectize({
    plugins: ['enter_key_submit'],
    onInitialize: function (foo) {
      this.on('submit', function () {
        this.$input.closest('form').submit();
      }, this);
    },

    valueField: 'id',
    labelField: 'title',
    searchField: ['title', 'artist'],
    options: [],
    create: false,
    load: function(query, callback) {
      if (!query.length) return callback();

      var results = [];

      // if (YOUTUBE_KEY) {
      //   $.ajax({
      //     url: 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=15&key=' +
      //       YOUTUBE_KEY + '&q=' + encodeURIComponent(query),
      //     dataType: 'jsonp',
      //     error: function () {
      //     },
      //     success: function (json) {
      //       results = results.concat(transformYoutubeJson(json.items));
      //     },
      //     complete: function () {
      //       callback(results);
      //     }
      //   });
      // }

      $.ajax({
        url: 'http://api.deezer.com/search/track?output=jsonp&q=' +
          encodeURIComponent(query),
          dataType: 'jsonp',
          error: function() {
            results = [];
          },
          success: function(json) {
            results = transformDeezerTracksJson(json.data.slice(0, 15));
            callback(results);
          }
      });

    },
    render: {
      option: function(track, escape) {
        console.log(track);
        return '<div class="track-option">' +
          '<img src="' + track.cover  + '" >' +
          '<div class="title">' +
            '<span class="name">' + escape(track.title) + '</span>' +
            '<span class="by">' + escape(track.artist) + '</span>' +
            '<img class="pull-right" src="' + (track.service === 'deezer' ? DEEZER_ICON : YOUTUBE_ICON) + '" >' +
          '</div>' +
        '</div>';
      }
    },
  });
});
