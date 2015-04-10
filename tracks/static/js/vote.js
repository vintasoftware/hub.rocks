(function () {
  var app = angular.module('hubrocks', [
    'LocalStorageModule', 'uuid4', 'hubrocks.const', 'faye']);

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

  app.factory('Faye', ['$faye', 'FANOUT_REALM',
    function($faye, FANOUT_REALM) {
      if (!FANOUT_REALM)
        return null;
      return $faye('http://' + FANOUT_REALM + '.fanoutcdn.com/bayeux');
    }
  ]);

  app.factory('HubrocksAPI', ['API_URL', 'my_uuid', '$http', 'Faye',
    function (API_URL, my_uuid, $http, Faye) {
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

      if (Faye) {
        Faye.subscribe('/tracks', function (newData) {
          angular.extend(data, newData);
        });
      } else {
        console.log("Running without Faye");
      }

      var insertVote = function (service_id) {
        return $http.post(API_URL + '/tracks/' + service_id + '/vote/');
      };

      var deleteVote = function (service_id) {
        $http.delete(API_URL + '/tracks/' + service_id + '/vote/');
      };

      var voteSkip = function() {
        $http.post(API_URL + '/tracks/now-playing/voteskip/');
      };

      return {
        data: data,
        insertVote: insertVote,
        deleteVote: deleteVote,
        voteSkip: voteSkip,
      };
    }
  ]);

  app.controller('HubrocksCtrl', ['HubrocksAPI', '$scope',
    function(HubrocksAPI, $scope) {
      $scope.data = HubrocksAPI.data;
      $scope.insertVote = HubrocksAPI.insertVote;
      $scope.deleteVote = HubrocksAPI.deleteVote;
      $scope.voteSkip = HubrocksAPI.voteSkip;

      $scope.insertTrack = function () {
        if ($scope.newTrack) {
          HubrocksAPI.insertVote($scope.newTrack);
        }
      };
    }
  ]);
}());
