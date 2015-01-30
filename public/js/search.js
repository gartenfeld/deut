angular.module('myApp', [])
	.controller('myController', ['$scope', '$http', 
		function($scope, $http) {

			$scope.query = null;
  			$scope.init = function(value,count) {
  				if (count && count > 0) {
	    			$scope.query = value;
	    			if ($scope.query !== "") {
				        $http.get('http://deut-rosson.rhcloud.com/json/' + $scope.query)
				        .success(function(data) {
							$scope.quotes = data;
				  		});
	  				}
	  			}
  			};

}]);

