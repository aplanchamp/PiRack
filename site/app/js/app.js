// 'use strict';

/* App Module */

var pirackApp = angular.module('pirackApp', [
  'ngRoute',
  'pirackControllers',
  'ui.bootstrap'
]);

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
      // when('/myModal', {
      //   templateUrl: 'partials/modal.html',
      //   controller: 'modalCtrl'
      // }).    
      otherwise({
        redirectTo: '/login'
      });
  }]);
