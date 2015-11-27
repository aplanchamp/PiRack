
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


pirackControllers.controller('informationCtrl', ['$scope', '$http', 'Restangular', function($scope, $http, Restangular) {

  $scope.dynamicPopover = {
    title: 'Additional information'
  };


  $scope.query = {}
  $scope.queryBy = '$';

  var rasps = Restangular.all('rasps');

  rasps.getList().then(function(data){
    $scope.raspberry = data;
    console.log(data);
  });

  newRasp =  {
      'address':
          {
              'ip': '172.0.0.1',
              'mac': '00:EF:4G:00:45:OP'
          },
      'status':
          {
              'cpu': 22,
              'power': 'Salut'
          },
      'position':
          {
              'stack': 2,
              'level': 4
          }
  };

  rasps.post(newRasp).then(function(newRasp) {
    console.log(newRasp.get());
  }, function error(reason) {
    // An error has occurred
  });

  // $scope.raspberry = [

  // {
  //   'id': '1',
  //   'address': {
  //       'ip': '172.0.0.1',
  //       'mac': '00:EF:4G:00:45:AA'
  //   },
  //   'status': {
  //       'cpu': '22',
  //       'power': 'On',
  //       'Lping': "24/65/2015 22h50"
  //   },
  //   'position': {
  //       'stack': '2',
  //       'level': '4'
  //    },
  //    'uri': ''
  // },
  // {
  //   'id': '2',
  //   'address': {
  //       'ip': '172.0.0.1',
  //       'mac': '00:EF:4G:00:45:BB'
  //   },
  //   'status': {
  //       'cpu': '22',
  //       'power': 'On',
  //       'Lping': "24/65/2015 22h50"
  //   },
  //   'position': {
  //       'stack': '2',
  //       'level': '4'
  //    },
  //    'uri': ''
  // },
  // {
  //   'id': '3',
  //   'address': {
  //       'ip': '172.0.0.1',
  //       'mac': '00:EF:4G:00:45:CC'
  //   },
  //   'status': {
  //       'cpu': '22',
  //       'power': 'On',
  //       'Lping': "24/65/2015 22h50"
  //   },
  //   'position': {
  //       'stack': '2',
  //       'level': '4'
  //    },
  //    'uri': ''
  // },
  // {
  //   'id': '4',
  //   'address': {
  //       'ip': '172.0.0.1',
  //       'mac': '00:EF:4G:00:45:DD'
  //   },
  //   'status': {
  //       'cpu': '22',
  //       'power': 'On',
  //       'Lping': "24/65/2015 22h50"
  //   },
  //   'position': {
  //       'stack': '2',
  //       'level': '4'
  //    },
  //    'uri': ''
  // }  
  

 ];     

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

  $scope.detailStack = null;

  $scope.showDetail = function() {
    if($scope.detailStack == null)
      $scope.detailStack = true;
    else
      $scope.detailStack = null;
  };


  $scope.stacks = [

  {
    'idStack': '1',
    'statusStack': 'ok',
    'rasp': raspberry
  },
  {
    'idStack': '1',
    'statusStack': 'ok',
    'rasp': raspberry
  }

  ];

  var raspberry = [

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
  }];    

  var iteration = raspberry.length/3;
    if (raspberry.length % 3 !== 0) {
      iteration += 1;
  }

  var compiledRaspberry = [];
  for (var i = 0 ; i < iteration; i++) {
    if(i == iteration - 1) {
      compiledRaspberry.push(raspberry);
      
    } else {
      compiledRaspberry.push(raspberry.splice(0,3))
      
    }
    
    $scope.raspberry = compiledRaspberry;
  }

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