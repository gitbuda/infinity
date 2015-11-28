var app = angular.module('infinity', ['ngRoute', 'angular-loading-bar']);

app.config(function($routeProvider) {
  $routeProvider
    .when('/', {
        templateUrl : 'pages/query.html',
        controller  : 'queryController'
    })
    .when('/list', {
        templateUrl : 'pages/list.html',
        controller  : 'listController'
    })
});

app.controller('queryController', function($scope, $location, $http) {
  $scope.message = 'query';

  $scope.rank = function() {
    var queryText = $scope.queryText;
    var postObject = new Object();
    postObject.query = queryText;
    $http.post("/api/query", postObject).success(function(data, status) {
      alert(data);
      $location.path('/list');
    });
  }
});

app.controller('listController', function($scope) {
  $scope.message = 'list';
});

// hide spinner
app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
}]);