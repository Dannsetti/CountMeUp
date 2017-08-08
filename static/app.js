(function () {
	var app = angular.module('chartApp', ['ng-fusioncharts']);
	app.factory('api', function ($http) {
		var hostname = window.location.origin;
		var getComputedVotes = function () {
			return $http.get(hostname + '/api/vote/calculate');
		};
		
		var postVote = function () {
			return $http.post(hostname + '/api/vote', {
				user: "Daniel",
				votedFor: 1
			});
			
		};
		
		var deleteVotes = function () {
			return $http.delete(hostname + '/api/vote');
		}
		
		// return all functions
		return {
			countMeUp: getComputedVotes,
			postVote: postVote,
			deleteVotes: deleteVotes
		};
	});
	app.controller ('MyController', function($scope, $interval, api) {
		// chart data source
		
		$scope.dataSource = {
			"chart": {
				"caption": "Counting of votes!",
				"captionFontSize": "50",
				"baseChartMessageFont": "* In thousands",
				"baseChartMessageFontSize": "30",
				"showBorder": "0",
				"bgColor": "#FFFFFF",
				"yAxisName": "(* Vote units)",
				"yAxisNameWidth": "100",
				"xAxisMinValue": "100",
				"yAxisValueDecimals": "0-100"
			},
			"data": []
		};
		
		var loading = false;
		var countMeUp = function () {
			loading = true;
			api.countMeUp().then(function (response) { // if it is success - 200
				// clean up
				var data = [];
				// var _data = JSON.parse(response.data);
				var _data = response.data;
				var i = 0;
				for (i = 0; i < _data.candidates.length; ++i) {
					var candidate = _data.candidates[i];
					data.push({
						"label": candidate._id,
						"value": candidate.votes
					});
				}
				$scope.dataSource.data = data;
				loading = false;
			}).catch(function (error) { // otherwise
				console.log("error", error);
				loading = false;
			});
		};
		
		// Set the interval
		var timer = $interval(function () {
			if (!loading) {
				countMeUp (); 
			}
		}, 1000);
		
		// Remove the interval once the app leaves the state
		$scope.$on('$destroy', function () { $interval.cancel(timer); });
	});
	
})();