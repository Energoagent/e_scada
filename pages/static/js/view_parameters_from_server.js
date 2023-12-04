

function floorChart() {
	setInterval(
		function() {
			var req = new XMLHttpRequest();
			req.open("POST", "http://192.168.22.252:8686/parameter/?page=2");
			req.onreadystatechange = function() {
				if(this.readyState === 4 && this.status === 200) {
					parameters = JSON.parse(this.response);
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
};
