(function () {
  var app = angular.module('hubrocks', [
    'LocalStorageModule', 'uuid4', 'hubrocks.const', 'faye']);

  app.config(
    ['$httpProvider',
      function ($httpProvider, RestangularProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.withCredentials = true;
      }
    ]);

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

  app.factory('HubrocksAPI', ['API_URL', 'ESTABLISHMENT', 'my_uuid', '$http', 'Faye',
    function (API_URL, ESTABLISHMENT, my_uuid, $http, Faye) {
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

      var fetchPlayerStatus = function () {
        $http.get(API_URL + '/tracks/change-player-status/')
          .success(function (playerStatus) {
            angular.extend(data, playerStatus);
          });
      };
      fetchPlayerStatus();

      if (Faye) {
        Faye.subscribe('/tracks-' + ESTABLISHMENT, function (newData) {
          angular.extend(data, newData);
        });
        Faye.subscribe('/player-status-' + ESTABLISHMENT, function (playerStatus) {
          angular.extend(data, playerStatus);
        });
      } else {
        console.log("Running without Faye");
      }

      var insertTrack = function (identifier) {
        var service = identifier.split(';')[0];
        var service_id = identifier.split(';')[1];
        return $http.post(API_URL + '/tracks/' + service + '/' + service_id + '/');
      };

      var insertVote = function (track_id) {
        $http.post(API_URL + '/tracks/' + track_id + '/vote/');
      };

      var deleteVote = function (track_id) {
        $http.delete(API_URL + '/tracks/' + track_id + '/vote/');
      };

      var voteSkip = function(track_id) {
        $http.post(API_URL + '/tracks/now-playing/voteskip/',
                   {'track_id': track_id});
      };

      var changePlayerStatus = function (status) {
        $http.put(API_URL + '/tracks/change-player-status/',
                  {'playing': status});
      };

      return {
        data: data,
        insertVote: insertVote,
        insertTrack: insertTrack,
        deleteVote: deleteVote,
        voteSkip: voteSkip,
        changePlayerStatus: changePlayerStatus,
      };
    }
  ]);

  app.controller('HubrocksCtrl', ['HubrocksAPI', '$scope', '$timeout',
    function(HubrocksAPI, $scope, $timeout) {
      $scope.data = HubrocksAPI.data;
      $scope.insertVote = HubrocksAPI.insertVote;
      $scope.deleteVote = HubrocksAPI.deleteVote;
      $scope.voteSkip = HubrocksAPI.voteSkip;
      $scope.changePlayerStatus = HubrocksAPI.changePlayerStatus;
      $scope.CAN_PLAY_PAUSE = CAN_PLAY_PAUSE;
      $scope.$watch('newTrack', function (newTrack){
        if (newTrack) {
          HubrocksAPI.insertTrack(newTrack);
          
          $timeout(function() {
            selectizedInput[0].selectize.clear();
            $('.selectize-input').css('background-color', 'green');
            setTimeout(function(){
              $('.selectize-input').css('background-color', 'white');
            }, 300);
          });
        }
      });

      $scope.insertTrack = function () {
        if ($scope.newTrack) {
          HubrocksAPI.insertTrack($scope.newTrack);
        }
      };
    }
  ]);
}());
