$(document).ready(function () {
  function transformTracksJson(tracks) {
    return $.map(tracks, function (t) {
      return {
        id: t.id,
        title: t.title,
        artist: t.artist.name
      };
    });
  }

  $('.select-track').selectize({
    valueField: 'id',
    labelField: 'title',
    searchField: ['title', 'artist'],
    options: [],
    create: false,
    load: function(query, callback) {
      if (!query.length) return callback();

      $.ajax({
        url: 'http://api.deezer.com/search/track?output=jsonp&q=' +
          encodeURIComponent(query),
        dataType: 'jsonp',
        error: function() {
          callback();
        },
        success: function (json) {
          callback(
            transformTracksJson(json.data.slice(0, 15)));
        }
      });
    },
    render: {
      option: function(track, escape) {
        return '<div>' +
          '<span class="title">' +
            '<span class="name">' + escape(track.title) + '</span>' +
            '<span class="by">' + escape(track.artist) + '</span>' +
          '</span>' +
        '</div>';
      }
    },
  });
});
