// 'use strict';

/* App Module */

var pirackApp = angular.module('pirackApp', [
  'ngRoute',
  'pirackControllers',
  'ui.bootstrap',
  'restangular'
]);

pirackApp.config(function(RestangularProvider) {
//set the base url for api calls on our RESTful services
 var newBaseUrl = "";
 if (window.location.hostname == "localhost") {
 newBaseUrl = "http://192.168.23.11:5000/api/v1.0/";
 console.log(window.location.href);
 } else {
 var deployedAt = window.location.href.substring(0, window.location.href);
 newBaseUrl = deployedAt + "/api/v1.0";
 }
 RestangularProvider.setBaseUrl(newBaseUrl);
 RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
     var extractedData;
     // .. to look for getList operations
     if (operation === "getList") {
       // .. and handle the data and meta data
       extractedData = data.rasps;
       console.log(data);
       console.log(extractedData);
     } else {
       extractedData = data;
     }
     return extractedData;
   });

 });

pirackApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/login', {
        templateUrl: 'partials/login.html',
        controller: 'LoginCtrl'
      }).
      when('/information', {
        templateUrl: 'partials/information.html',
        controller: 'informationCtrl'
      }).
      when('/install', {
        templateUrl: 'partials/install.html',
        controller: 'installCtrl'
      }).
      when('/about', {
        templateUrl: 'partials/about.html',
        controller: 'aboutCtrl'
      }).
      when('/master', {
        templateUrl: 'partials/master.html',
        controller: 'masterCtrl'
      }).
      otherwise({
        redirectTo: '/login'
      });
  }]);
