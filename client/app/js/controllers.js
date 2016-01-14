
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
  $scope.errorAction = false;



  //$scope.myDynamicClass = 'plan-name-error';

  $scope.getOptions = function() {
    Restangular.oneUrl('/rasps/options').get().then(function(response){
      //Actions that we can achieve on rasps ressource
      $scope.actions = response.actions;
    });
  };


  $scope.getRasps = function() {
    Restangular.oneUrl('/rasps').get().then(function(response){
      //Actions that we can achieve on rasps ressource
      $scope.raspberry = response.rasps;
    }, function(response){
      $scope.textErrorAction = "A problem occured on the Network, the list of Raspberry Pis can not be fetched yet";
    });  
  };

  $scope.submitAction = function(action) {
          action_on_rasp = {
            'ip':'coucou',
            'Port':1026,
            'action': action
          }
      Restangular.oneUrl('/rasps').post("execute",action_on_rasp).then(function(response){
        $scope.getRasps(); 
        $scope.$apply();
      },
      function(response){
          $scope.errorAction = true;
          $scope.textErrorAction = response.data;
          $scope.getRasps(); 
          $scope.$apply();
      });    
  };

  $scope.getOptions();
  $scope.getRasps();

  $scope.stacks = [
      {
          'id': 1,
          'rid': [1,3,7,9],
          'power': 'On',
          'x': '2',
          'y': '2'
      },
     {
          'id': 2,
          'rid': [2, 12, 10, 6],
          'power': 'Off',
          'x': '2',
          'y': '2'
      },
     {
          'id': 3,
          'rid': [4, 5, 11, 8],
          'power': 'Off',
          'x': '2',
          'y': '2'
      },    
     {
          'id': 4,
          'rid': [13, 14, 15, 16],
          'power': 'Off',
          'x': '2',
          'y': '2'
      },   
     {
          'id': 5,
          'rid': [17, 18],
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

pirackControllers.controller('installCtrl', ['$scope', '$http', '$uibModal', function($scope, $http, $uibModal) {

  $scope.progressBarShow = false;
  $scope.messageFirstInstallation = false;
  $scope.stacks = null;

  $scope.installPirack = function(){
    $scope.progressBarShow = true;
    $scope.messageFirstInstallation = false;
    $scope.close();
  }  

  $scope.phase1 = function() {
  };

  $scope.phase2 = function() {
  };    

  $scope.stacks = [
    {
        'id': 1,
        'rid': [1,3,7,9,13,14],
        'power': 'On',
        'Sstatus': 'okStatus',
        'x': '2',
        'y': '2'
    },
   {
        'id': 2,
        'rid': [2, 12, 10, 6,15,16],
        'power': 'Off',
        'Sstatus': 'koStatus',
        'x': '2',
        'y': '2'
    },
   {
        'id': 3,
        'rid': [4, 5, 11, 8,17,18],
        'power': 'Off',
        'Sstatus': 'okWarning',
        'x': '2',
        'y': '2'
    }    
]

  if($scope.stacks == null){
      $scope.messageFirstInstallation = true;
  }
 
$scope.openModal=function(){
    $scope.modalInstance=$uibModal.open({
      templateUrl: 'myTestModal.tmpl.html',
      scope:$scope
    });
}

$scope.close=function(){
    $scope.modalInstance.dismiss();//$scope.modalInstance.close() also works I think
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
