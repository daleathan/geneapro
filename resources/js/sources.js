app.
config(function($stateProvider) {
   $stateProvider.
   state('sources', {
      url: '/sources/list',
      templateUrl: 'geneaprove/sources.html',
      controller: 'sourcesCtrl'
   }).
   state('source_new', {
      url: '/sources/new',
      templateUrl: 'geneaprove/source.html',
      controller: 'sourceCtrl'
   }).
   state('source', {
      url: '/sources/:id',
      templateUrl: 'geneaprove/source.html',
      controller: 'sourceCtrl'
   });
}).

controller('sourcesCtrl', function($scope, Paginated) {
   Paginated.instrument($scope, '/data/sources/list', 'settings.sources.rows');
}).

controller('sourceCtrl', function($scope, $http, $stateParams) {
   var id = $stateParams.id;
   if (id === undefined) {
      id = -1;
   }
   var re_part = /\{\{([^}]+)\}\}/g;
   var cached_parts = {};

   if (id === undefined) {
      $scope.source = {
         title: 'unknown'
      };

   } else {
      $http.get('/data/sources/' + id).then(function(resp) {
         $scope.source = resp.data.source;
         $scope.source_types = resp.data.source_types;
         $scope.parts = resp.data.parts;

         angular.forEach($scope.parts, function(p) {
            cached_parts[p.name] = p.value;
         });
      });
   }

   $scope.$watch('source.medium', function(val) {
      if (val) {
         $http.get('/data/citationModel/' + val).then(function(resp) {
            var full = resp.data.full;
            var m;
            var required = [];

            while ((m = re_part.exec(full)) != null) {
               required.push(m[1]);
            }
            $scope.required_parts = required;
         });
      }
   });
});
