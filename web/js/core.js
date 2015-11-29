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

app.service('remoteData', function () {
  var query = '';
  var result = '';
  return {
    getQuery: function () {
      return query;
    },
    setQuery: function(value) {
      query = value;
    },
    getResult: function() {
      return result;
    },
    setResult: function(value) {
      result = value;
    }
  };
});

app.service('pageData', function () {
  var pagenum = 0;
  var pagesize = 5;
  return {
    getPageNum: function () {
      return pagenum;
    },
    setPageNum: function(value) {
      pagenum = value;
    },
    getPageSize: function() {
      return pagesize;
    },
    clear: function() {
      pagenum = 0;
    },
    inc: function() {
      pagenum = pagenum + 1;
    },
    decr: function() {
      if (pagenum <= 0)
        return;
      pagenum = pagenum - 1;
    }
  };
});

function paging(pageData) {
  var paging = "?pagenum=" + pageData.getPageNum() + "&pagesize=" + pageData.getPageSize();
  return paging;
}

app.controller('queryController', function($q, $scope, $location, $http, remoteData, pageData) {
  $scope.message = 'query';

  $scope.rank = function() {
    pageData.clear();
    var queryText = $scope.queryText;
    var postObject = new Object();
    postObject.query = queryText;
    remoteData.setQuery(queryText)
    $http.post("/api/query" + paging(pageData), postObject).success(function(data, status) {
      var allData = [];
      var promieses = [];
      data.forEach(function(entry) {
        promieses.push($http.get("/api/data/document/" + entry));
      });
      $q.all(promieses).then(function(response) {
        for (var i = 0; i < response.length; i++) {
          allData.push({
            id: response[i].data.identifier,
            content: response[i].data.content
          });
        }
        remoteData.setResult(allData);
        $location.path('/list');
      });
    });
  }
});

app.controller('listController', function($q, $scope, $http, remoteData, pageData) {
  var pageNum = 0;
  $scope.queryText = remoteData.getQuery();
  $scope.queryResult = remoteData.getResult();

  var execute = function() {
    var queryText = $scope.queryText;
    var postObject = new Object();
    postObject.query = queryText;
    remoteData.setQuery(queryText)
    $http.post("/api/query" + paging(pageData), postObject).success(function(data, status) {
      // TODO: write utility function
      var allData = [];
      var promieses = [];
      data.forEach(function(entry) {
        promieses.push($http.get("/api/data/document/" + entry));
      });
      $q.all(promieses).then(function(response) {
        for (var i = 0; i < response.length; i++) {
          allData.push({
            id: response[i].data.identifier,
            content: response[i].data.content
          });
        }
        $scope.queryResult = allData;
        remoteData.setResult(allData);
      });
    });
  }

  $scope.rank = function() {
    pageData.clear();
    execute();
  }

  $scope.prevpage = function() {
    pageData.decr();
    execute();
  }

  $scope.nextpage = function() {
    pageData.inc();
    execute();
  }
});

// hide spinner
app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
}]);
