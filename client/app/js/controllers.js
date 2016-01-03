
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


pirackControllers.controller('informationCtrl', ['$scope', '$http', '$sce', 'Restangular', function($scope, $http, $sce, Restangular) {


  $scope.query = {}
  $scope.queryBy = '$';
  $scope.selectedAction = "ping";

  // $scope.stacks{
  //   {
  //       'id':'1'
  //       'status':'on'
  //   },
  //   {
  //       'id':'2'
  //       'status':'off'
  //   }  
  // }

  $scope.actions = [
    'ping',
    'reboot',
    'shutdown'
  ];

  $scope.setAction = function(action) {
    $scope.selectedAction = action;
  };

  $scope.submitAction = function(action) {
      console.log(action);
  };

  var rasps = Restangular.all('rasps');
  //var raspOptions = Restangular.all('rasps/options');
  rasps.getList().then(function(data){
    $scope.raspberry = data;
  });
  // raspOptions.getList().then(function(data){
  //   $scope.raspOptions = data;
  // });

  //console.log($scope.raspOptions);

$scope.stacks = [
    {
        'id': 1,
        'rid': [1,3,7,9,13,14],
        'power': 'On',
        'x': '2',
        'y': '2'
    },
   {
        'id': 2,
        'rid': [2, 12, 10, 6,15,16],
        'power': 'Off',
        'x': '2',
        'y': '2'
    },
   {
        'id': 3,
        'rid': [4, 5, 11, 8,17,18],
        'power': 'Off',
        'x': '2',
        'y': '2'
    }    
]


  $scope.getRaspId = function(raspId){
    for(var n = 0; n < $scope.raspberry.length; n++){
      if ($scope.raspberry[n].id == raspId)
        levelArray = n;
    }
    $scope.dynamicPopover = {
      title: 'Additional information',
      content: $sce.trustAsHtml('<li> Mac Adress : ' + $scope.raspberry[levelArray].mac + '</li><br><li>' + 'IP Adress : ' + $scope.raspberry[levelArray].ip + '</li>')
    };
  }  

}]);

pirackControllers.controller('installCtrl', ['$scope', '$http', function($scope, $http) {

  var value = Math.floor((Math.random() * 100) + 1);   
  var type;

  if (value < 100) {
    type = 'info';
  } else if (value == 100) {
    type = 'success';
  } else {
    type = 'danger';
  }

  $scope.dynamic = value;
  $scope.type = type;

  $scope.stacks = [
    {
        'id': 1,
        'rid': [1,3,7,9,13,14],
        'power': 'On',
        'x': '2',
        'y': '2'
    },
   {
        'id': 2,
        'rid': [2, 12, 10, 6,15,16],
        'power': 'Off',
        'x': '2',
        'y': '2'
    },
   {
        'id': 3,
        'rid': [4, 5, 11, 8,17,18],
        'power': 'Off',
        'x': '2',
        'y': '2'
    }    
]

 
}]);

pirackControllers.controller('masterCtrl', ['$scope', '$http', function($scope, $http) {

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
