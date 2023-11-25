

function floorChart() {
	setInterval(
		function() {
			var req = new XMLHttpRequest();
			req.open("GET", "processor?");
			req.onreadystatechange = function() {
				if(this.readyState === 4 && this.status === 200) {
					resp = JSON.parse(this.response);
					parameters = resp.parameters;
					for(let i=0; i < parameters.length; i++) {
						let elem = document.getElementById(parameters[i].ID);
						if(elem != null) {
							elem.innerHTML = parameters[i].Value;
							elem.style.fill = parameters[i].color;
						};
					};
				};
			};
			req.send();
		}, 
		5000
	);
}
