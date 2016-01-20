
// http://jsfiddle.net/qks8p28g/

var pirackControllers = angular.module('pirackControllers', ['ui.bootstrap']);

pirackControllers.controller('LoginCtrl', ['$scope', '$http', function($scope, $http) {

 	$scope.model = {};
 	$scope.ImageUrl = 'img/1914-01.jpg';
    $scope.ImageUrlFond = 'img/fond.png';
 	$scope.invalide = false;

// Mot de passe écrit en dur selon les spécifications
	$scope.login = function() {
	  if (($scope.model.username == 'admin') && ($scope.model.password == 'admin')){
			window.location = "#/information"
	  }
	  else {
	  	$scope.invalide = true;
	  }
  };

}]);


pirackControllers.controller('informationCtrl', ['$scope', '$http', '$sce', '$filter', 'Restangular', function($scope, $http, $sce, $filter, Restangular) {

// Variales à initialiser pour la recherche
  $scope.query = {}
  $scope.queryBy = '$';

// variable pour ng-show sur la div qui affiche un message d'erreur en cas de problème sur une action (ping, temperature...)
  $scope.errorAction = false;

// variables pour le bouton switch view (ng-show, ng-hide et le texte du bouton)  
  $scope.switchView = true;
  $scope.switchButton = "View Pirack";



// Fonction pour la vue 2D, elle permet de transformer le tableau stack sous cette forme 
// [{ index: 0, 
//    cells: [ 
//        { index: 0, data: {...} }, 
//        { index: 0, data: {...} }] 
//   }, 
//   { index: 1, 
//     cells: [ 
//        { index: 0, data: {...} }] 
//     },
//     ...
// ]
//On peut ensuite afficher dans le html les stacks en fonction de leurs positions

 function transformToRows(stacks) {
      var ordered = $filter('orderBy')(stacks, '\'x\'');
      var rows = [];

      var maxRows = ordered[ordered.length-1].x;
      var maxCells = 0;
      angular.forEach(ordered, function(item) {
        if (item.y > maxCells)
          maxCells = item.y;
      });    


      for (var i = 0; i < maxRows; ++i) {
        var row = { index: i, cells: [] };
        rows.push(row);
         for (var j = 0; j < maxCells; ++j)
           row.cells.push({ index: j, data: undefined });
      }

      angular.forEach(ordered, function(item) {
         var row = rows[item.x-1];
         row.cells[item.y-1].data = item;
      });         

      for(var k = 0; k < rows.length; k++){
        for(var n = 0; n < rows[k].cells.length; n++){
          if (rows[k].cells[n].data == undefined){
            var tab = rows[k].cells;
            tab.splice(k,n);
          }
        }
      }
      return rows;
  }  


// fonction lorsqu'on clique sur le bouton pour afficher la vue 2d du Pirack et pour revenir à la page de base
  $scope.viewPirack = function(){
    if($scope.switchView == true){
      $scope.switchView = false;
      $scope.switchButton = "Back to page";
    }else{
      $scope.switchView = true;
      $scope.switchButton = "View Pirack";
    }
  }

// Fonction pour récupérer la liste des options que l'on peut effectuer sur le Pirack
  $scope.getOptions = function() {
    Restangular.oneUrl('/rasps/options').get().then(function(response){
      //Actions that we can achieve on rasps ressource
      $scope.actions = response.actions;
    });
  };

// Fonction qui recupère la totalité des rasp dans le Pirack avec leur détails
  $scope.getRasps = function() {
    Restangular.oneUrl('/rasps').get().then(function(response){
      //Actions that we can achieve on rasps ressource
      $scope.raspberry = response.rasps;
    }, function(response){
      $scope.textErrorAction = "A problem occured on the Network, the list of Raspberry Pis can not be fetched yet";
    });  
  };

// Fonction pour réaliser une action soit sur le rasp, une stack ou le Pirack dans son ensemble.
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

// Fonction pour afficher dynamiquement des informations sur le bouton 'i' sur chaque rasp
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



  $scope.stacks = [
      {
          'id': 1,
          'rid': [1,3,7,9],
          'power': 'On',
          'Sstatus': 'okStatus', 
          'x': '1',
          'y': '1'
      },
     {
          'id': 2,
          'rid': [2, 12, 10, 6],
          'power': 'Off',
          'Sstatus': 'okStatus',
          'x': '1',
          'y': '2'
      },
     {
          'id': 3,
          'rid': [4, 5, 11, 8],
          'power': 'Off',
          'Sstatus': 'koStatus',
          'x': '1',
          'y': '3'
      },    
     {
          'id': 4,
          'rid': [13, 14, 15, 16],
          'power': 'Off',
          'Sstatus': 'warningStatus',
          'x': '1',
          'y': '4'
      },   
     {
          'id': 5,
          'rid': [17, 18],
          'power': 'Off',
          'Sstatus': 'warningStatus',
          'x': '2',
          'y': '1'
      }           

  ]

  $scope.getOptions();
  $scope.getRasps();
  $scope.myRows = transformToRows($scope.stacks);


}]);

pirackControllers.controller('installCtrl', ['$scope', '$http', '$uibModal', function($scope, $http, $uibModal) {


// Variables pour afficher des informations en fonction de l'état du Pirack
  $scope.progressBarShow = false;
  $scope.messageFirstInstallation = false;
  $scope.stacks = null;


// Lance l'installation du Pirack
  $scope.installPirack = function(){
    $scope.progressBarShow = true;
    $scope.messageFirstInstallation = false;
    $scope.close();
  }  

//   $scope.stacks = [
//     {
//         'id': 1,
//         'rid': [1,3,7,9,13,14],
//         'power': 'On',
//         'Sstatus': 'okStatus',
//         'x': '2',
//         'y': '2'
//     },
//    {
//         'id': 2,
//         'rid': [2, 12, 10, 6,15,16],
//         'power': 'Off',
//         'Sstatus': 'koStatus',
//         'x': '2',
//         'y': '2'
//     },
//    {
//         'id': 3,
//         'rid': [4, 5, 11, 8,17,18],
//         'power': 'Off',
//         'Sstatus': 'warningStatus',
//         'x': '2',
//         'y': '2'
//     }    
// ]

// Affiche un message si c'est la première installation
  if($scope.stacks == null){
      $scope.messageFirstInstallation = true;
  }
 
// Ouvre un modal pour confirmer le lancement de l'installation 
$scope.openModal=function(){
    $scope.modalInstance=$uibModal.open({
      templateUrl: 'myTestModal.tmpl.html',
      scope:$scope
    });
}

// Bouton annule l'installation depuis le modal
$scope.close=function(){
    $scope.modalInstance.dismiss();//$scope.modalInstance.close() also works I think
};



}]);

pirackControllers.controller('masterCtrl', ['$scope', '$http', function($scope, $http) {

  $scope.master = {
        'ip': '172.0.0.2',
        'mac': '00:EF:4B:00:43:OP',
        'power': 'On',
        'cpu': '46',
        'Lping': '25/20/1992',
        'Rstatus': 'okStatus', 
    };

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
