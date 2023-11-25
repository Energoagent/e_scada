    function drawCoreChart() {
        var data_mbdT = google.visualization.arrayToDataTable([
          ['Время', 'T min', 'T изм', 'T max'],
          ['17:00', 18, 18,	25],
          ['17:30', 18, 20,	25],
          ['18:00', 18, 25,	25],
          ['18:30', 18, 22,	25]
        ]);
        var data_mbdP = google.visualization.arrayToDataTable([
          ['Время', 'P min', 'P изм', 'P max'],
          ['17:00', 18, 18,	25],
          ['17:30', 18, 20,	25],
          ['18:00', 18, 25,	25],
          ['18:30', 18, 22,	25]
        ]);
        var data_mbdV = google.visualization.arrayToDataTable([
          ['Время', 'V min', 'V изм', 'V max'],
          ['17:00', 40, 77,	80],
          ['17:30', 40, 67,	80],
          ['18:00', 40, 80,	80],
          ['18:30', 40, 85,	80]
        ]);

        var options_mbdT = {
			title: 'ТЕМПЕРАТУРА',
			curveType: 'function',
			legend: { position: 'bottom' },
        };
        var options_mbdP = {
			title: 'ДАВЛЕНИЕ',
			curveType: 'function',
			legend: { position: 'bottom' },
        };
        var options_mbdV = {
			title: 'ВЛАЖНОСТЬ',
			curveType: 'function',
			legend: { position: 'bottom' },
        };

        var chart_mbdT = new google.visualization.LineChart(document.getElementById('chart_mbdT'));
        var chart_mbdP = new google.visualization.LineChart(document.getElementById('chart_mbdP'));
        var chart_mbdV = new google.visualization.LineChart(document.getElementById('chart_mbdV'));

        chart_mbdT.draw(data_mbdT, options_mbdT);
        chart_mbdP.draw(data_mbdP, options_mbdP);
        chart_mbdV.draw(data_mbdV, options_mbdV);

		var parameters;
		setInterval(
			function() {
				var request = new XMLHttpRequest();
				request.open("GET", "processor?");
				request.onreadystatechange = 
				function() {
					if(this.readyState === 4 && this.status === 200) {
						resp = JSON.parse(this.response);
						parameters = resp.parameters;
					}
				};
				request.send();
			}, 
			1000
		);
	};

