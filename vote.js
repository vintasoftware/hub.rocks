var app = angular.module('hubrocks', ['firebase']);

app.controller("HubrocksCtrl", ["$scope", "$firebase",
  function($scope, $firebase) {
    var ref = new Firebase("https://hubrocksdb.firebaseio.com/tracks");
    var sync = $firebase(ref);
    
    $scope.tracks = sync.$asArray();
  }
]);

$(document).ready(function () {
  $('.select-track').selectize({
    valueField: 'id',
    labelField: 'title',
    searchField: ['title'],
    options: [],
    create: false,
    load: function(query, callback) {
      if (!query.length) return callback();

      $.ajax({
        url: 'http://api.deezer.com/search/track?output=jsonp&q=' + encodeURIComponent(query),
        dataType: "jsonp",
        error: function() {
          callback();
        },
        success: function (json) {
          callback(json.data.slice(0, 10));
        }
      });
    },
    render: {
      option: function(track, escape) {
        return '<div>' +
          '<span class="title">' +
            '<span class="name">' + escape(track.title) + '</span>' +
            '<span class="by">' + escape(track.artist.name) + '</span>' +
          '</span>' +
        '</div>';
      }
    },
  });
});
