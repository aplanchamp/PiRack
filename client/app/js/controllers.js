
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

  $scope.detailStack = null;


  $scope.stacks = [

  {
    'idStack': '1',
    'statusStack': 'ok',
    'rasp': [

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
  }]
  },
  {
    'idStack': '2',
    'statusStack': 'off',
    'rasp': [

  {
    'id': '5',
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
    'id': '6',
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
    'id': '7',
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
    'id': '8',
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
  }]
  }

  ];

  $scope.showDetail = function(idStack) {

    var levelArray;
    //console.log(idStack);

    if($scope.detailStack == null)
      $scope.detailStack = true;
    else
      $scope.detailStack = null;

    for(var n = 0; n < $scope.stacks.length; n++){
          if ($scope.stacks[n].idStack == idStack)
            levelArray = n;
    }
      //console.log(levelArray);

      console.log($scope.stacks[levelArray]);
    var raspberry = $scope.stacks[levelArray].rasp;

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


  };

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
