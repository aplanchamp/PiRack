
// http://jsfiddle.net/qks8p28g/

var pirackControllers = angular.module('pirackControllers', ['ui.bootstrap']);

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

  $scope.dynamicPopover = {
    title: 'Additional information'
  };


  $scope.query = {}
  $scope.queryBy = '$';

  $scope.raspberry = [

  {
    'id': '1',
    'address': {
        'ip': '172.0.0.1',
        'mac': '00:EF:4G:00:45:AA'
    },
    'status': {
        'cpu': '22',
        'power': 'On',
        'Lping': "24/65/2015 22h50"
    },
    'position': {
        'stack': '2',
        'level': '4'
     },
     'uri': ''
  },
  {
    'id': '2',
    'address': {
        'ip': '172.0.0.1',
        'mac': '00:EF:4G:00:45:BB'
    },
    'status': {
        'cpu': '22',
        'power': 'On',
        'Lping': "24/65/2015 22h50"
    },
    'position': {
        'stack': '2',
        'level': '4'
     },
     'uri': ''
  },
  {
    'id': '3',
    'address': {
        'ip': '172.0.0.1',
        'mac': '00:EF:4G:00:45:CC'
    },
    'status': {
        'cpu': '22',
        'power': 'On',
        'Lping': "24/65/2015 22h50"
    },
    'position': {
        'stack': '2',
        'level': '4'
     },
     'uri': ''
  },
  {
    'id': '4',
    'address': {
        'ip': '172.0.0.1',
        'mac': '00:EF:4G:00:45:DD'
    },
    'status': {
        'cpu': '22',
        'power': 'On',
        'Lping': "24/65/2015 22h50"
    },
    'position': {
        'stack': '2',
        'level': '4'
     },
     'uri': ''
  }  
  

 ];     

}]);

pirackControllers.controller('installCtrl', ['$scope', '$http', function($scope, $http) {
    

}]);

pirackControllers.controller('aboutCtrl', ['$scope', '$http', function($scope, $http) {
    
     $scope.members = [
    {'name': 'Héloise Rostan',
     'role': 'Project Leader - GLRT',
     'picture': 'img/hrostan.png'},
    {'name': 'Philippe Diep',
     'role': 'Developer - GLRT',
     'picture': 'img/phdiep.jpg'},
    {'name': 'Akram El Fadil',
     'role': 'Developer - GLRT',
     'picture': 'img/akram.jpg'},
    {'name': 'Alexandre Meslet',
     'role': 'Developer - RSC',
     'picture': 'img/jc.jpg'},
    {'name': 'Arian Sénior',
     'role': 'Developer - RSC',
     'picture': 'img/arian.jpg'},               
    {'name': 'Aude Planchamp',
     'role': 'Developer - GLRT',
     'picture': 'img/aude.jpg'}     
  ];


}]);


// pirackControllers.controller('modalCtrl', ['$scope', '$http', function($scope, $http) {
    

// }]);