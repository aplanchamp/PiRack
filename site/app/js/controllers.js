var pirackControllers = angular.module('pirackControllers', []);

pirackControllers.controller('LoginCtrl', ['$scope', '$http', function($scope, $http) {

 	$scope.model = {};
 	$scope.ImageUrl = 'img/1914-01.jpg';
  $scope.ImageUrlFond = 'img/fond.png';
 	$scope.invalide = false;

	$scope.login = function() {
	  if (($scope.model.username == 'admin') && ($scope.model.password == 'admin')){
			window.location = "#/information"
	  }
	  else {
	  	$scope.invalide = true;
	  }
  };

}]);


pirackControllers.controller('informationCtrl', ['$scope', '$http', function($scope, $http) {
  	
  $scope.raspberry = [
    {'id': '1',
     'cpu': '22%',
     'onoff': 'On',
     'pile': 'Pile 2',
     'level': 'Level 4',
     'ping': 'Last ping : 25/10/1992.'},
    {'id': '2',
     'cpu': '25%',
     'onoff': 'Off',
     'pile': 'Pile 2',
     'level': 'Level 3',
     'ping': 'Last ping : 25/12/2015.'},     
    {'id': '3',
     'cpu': '99%',
     'onoff': 'On',
     'pile': 'Pile 4',
     'level': 'Level 6',
     'ping': 'Last ping : 12/09/2014.'}
  ];

}]);

pirackControllers.controller('installCtrl', ['$scope', '$http', function($scope, $http) {
    

}]);

pirackControllers.controller('aboutCtrl', ['$scope', '$http', function($scope, $http) {
    

}]);