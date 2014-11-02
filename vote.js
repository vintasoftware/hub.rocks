var app = angular.module('hubrocks', ['firebase']);

app.controller("HubrocksCtrl", ["$scope", "$firebase",
  function($scope, $firebase) {
    var ref = new Firebase("https://hubrocksdb.firebaseio.com/tracks");
    var sync = $firebase(ref);
    
    $scope.tracks = sync.$asArray();
  }
]);
