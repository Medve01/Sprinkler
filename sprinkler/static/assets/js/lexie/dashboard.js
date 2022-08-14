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
load_devices();

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



// var socket = io.connect('ws://' + document.domain + ':' + location.port, {transports: ['websocket']});
// var socket = io.connect('ws://' + document.domain + ':' + location.port);
// socket.on('event', function(msg) {
// 	console.log('Event received', msg);
// 	if (msg.event.event_type == 'status'){
// 		if (msg.event.event_data == 'on' || msg.event.event_data == 'off'){
// 			devices.forEach(function crawl_rooms(room, index){
// 				room.room_devices.forEach(function update_device(device, index){
// 					if (device.device_id == msg.device_id){
// 						if (msg.event.event_data == 'on'){
// 							device.device_ison = true;
// 						} else {
// 							device.device_ison = false;
// 						}
// 					}
// 				});
// 			});
// 		}
// 	}
// });
