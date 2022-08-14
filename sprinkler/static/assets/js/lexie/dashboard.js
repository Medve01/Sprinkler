/* jshint esversion: 6 */
var zones;
function load_devices(){
	var request = new XMLHttpRequest();
	request.open('GET', '/api/zone', false);
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			zones = JSON.parse(request.responseText);
		} else {
			console.log('HTTP Error fetching zones');
		}
	};
	request.onerror = function(){
		console.log('Network error during fetching zones');
	}

	request.send();
}

function load_irrigation_enabled(){
	var request = new XMLHttpRequest();
	request.open('GET', '/api/switch/irrigation_enabled', false);
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			irrigation_enabled = JSON.parse(request.responseText);
			console.log(irrigation_enabled)
		} else {
			console.log('HTTP Error fetching zones');
		}
	};
	request.onerror = function(){
		console.log('Network error during fetching zones');
	}

	request.send();
}

function load_irrigation_paused(){
	var request = new XMLHttpRequest();
	request.open('GET', '/api/switch/irrigation_enabled', false);
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			irrigation_paused = JSON.parse(request.responseText);
			console.log(irrigation_paused.value)
		} else {
			console.log('HTTP Error fetching zones');
		}
	};
	request.onerror = function(){
		console.log('Network error during fetching zones');
	}

	request.send();
}

controller = {
	toggle_relay: function(e, model) {
		console.log(model.zones[model['%zone%']])
		console.log(model['%zone%'])
		var zone = model.zones[model['%zone%']];
		if (zone.on) {
			onoff = "/off"
		} else {
			onoff = "/on"
		}
		console.log('toggle device: ' + zone.id);
		URL = '/api/zone/' + zone.id + onoff
		console.log(URL)
		var request = new XMLHttpRequest();
		request.open('GET', URL, false);
		request.onload = function() {
			if (request.status >= 200 && request.status < 400) {
				console.log(request.responseText)
				result = JSON.parse(request.responseText);
			} else {
				console.log('HTTP Error fetching devices');
			}
		}
		request.send();
	},
}

irrigation_enabled_controller = {
	toggle_switch: function(e, model) {
		console.log(!model.irrigation_enabled.value)
		URL = '/api/switch/irrigation_enabled'
		var request = new XMLHttpRequest();
		request_data = JSON.stringify({'value': !model.irrigation_enabled.value})
		request.open('PUT', URL, true)

		request.setRequestHeader('Content-type','application/json; charset=utf-8');
		request.onload = function () {
			var result = JSON.parse(request.responseText);
			if (request.readyState == 4 && request.status == "200") {
				console.log(result);
			} else {
				console.error(result);
			}
		}
		request.send(request_data);
	}
}

irrigation_paused_controller = {
	toggle_switch: function(e, model) {
		console.log(!model.irrigation_paused.value)
		URL = '/api/switch/paused'
		var request = new XMLHttpRequest();
		request_data = JSON.stringify({'value': !model.irrigation_paused.value})
		request.open('PUT', URL, true)

		request.setRequestHeader('Content-type','application/json; charset=utf-8');
		request.onload = function () {
			var result = JSON.parse(request.responseText);
			if (request.readyState == 4 && request.status == "200") {
				console.log(result);
			} else {
				console.error(result);
			}
		}
		request.send(request_data);
	}
}


load_devices();
load_irrigation_enabled();
load_irrigation_paused();

rivets.formatters.hashtag = str => {
	return '#'.concat(str);
};

rivets.formatters.modal = function(value, decorator, hashtag) {
	if (hashtag){
		return '#'.concat(value).concat('_').concat(decorator);
	}
	return value.concat('_').concat(decorator);
};

room_view = rivets.bind(
	document.querySelector('#zone'),{
		zones: zones,
		controller: controller,
	}
)

irrigation_enabled_view = rivets.bind(
	document.querySelector('#irrigation_enabled'), {
		irrigation_enabled: irrigation_enabled,
		controller: irrigation_enabled_controller
	}
)

irrigation_paused_view = rivets.bind(
	document.querySelector('#irrigation_paused'), {
		irrigation_paused: irrigation_paused,
		controller: irrigation_paused_controller
	}
)