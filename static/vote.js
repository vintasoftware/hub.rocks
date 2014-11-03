(function () {
  var app = angular.module('hubrocks', [
    'LocalStorageModule', 'uuid4', 'pusher-angular', 'hubrocks.const']);

  app.factory('my_uuid', ['localStorageService', 'uuid4',
    function (localStorageService, uuid4) {
      var my_uuid = localStorageService.get('my_uuid');
      if (!my_uuid) {
        my_uuid = uuid4.generate();
        localStorageService.set('my_uuid', my_uuid);
      }

      return my_uuid;
    }
  ]);

  app.factory('HubrocksAPI', ['API_URL', 'PUSHER_API_KEY', 'my_uuid', '$http', '$pusher',
    function (API_URL, PUSHER_API_KEY, my_uuid, $http, $pusher) {
      $http.defaults.headers.common.Authorization = 'Token ' + my_uuid;
      var data = {
        'my_uuid': my_uuid
      };

      var fetchTracks = function () {
        $http.get(API_URL + '/tracks/')
          .success(function (newData) {
            angular.extend(data, newData);
          });
      };
      fetchTracks();

      var pusher = $pusher(new Pusher(PUSHER_API_KEY));
      pusher.subscribe('tracks');
      pusher.bind('updated', function () {
        fetchTracks();
      });

      var insertVote = function (deezer_id) {
        $http.put(API_URL + '/tracks/' + deezer_id + '/vote/');
      };

      var deleteVote = function (deezer_id) {
        $http.delete(API_URL + '/tracks/' + deezer_id + '/vote/');
      };

      return {
        data: data,
        insertVote: insertVote,
        deleteVote: deleteVote,
      };
    }
  ]);

  app.controller('HubrocksCtrl', ['HubrocksAPI', '$scope',
    function(HubrocksAPI, $scope) {
      $scope.data = HubrocksAPI.data;
      $scope.insertVote = HubrocksAPI.insertVote;
      $scope.deleteVote = HubrocksAPI.deleteVote;

      $scope.insertTrack = function () {
        HubrocksAPI.insertVote($scope.newTrack);
      };
    }
  ]);
}());
