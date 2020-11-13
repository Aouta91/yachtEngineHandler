$(document).ready(function(){
    // initialize Leaflet
    var map = L.map('map').setView({lon: 0, lat: 0}, 2);
    // add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);
    L.control.scale().addTo(map);
    var home_icon = L.icon({
        iconUrl: '/static/pic/home.svg',
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, 0],
        shadowUrl: 'home-shadow.svg',
        shadowSize: [0, 0],
        shadowAnchor: [0, 0]
    });
    var current_icon = L.icon({
        iconUrl: '/static/pic/current.svg',
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, 0],
        shadowUrl: 'current-shadow.svg',
        shadowSize: [0, 0],
        shadowAnchor: [0, 0]
    });
    // show a marker on the map
    current_marker = L.marker([55.83995, 37.4883], {title: 'Current', icon: current_icon, opacity: 1.0}).bindPopup('Current');
    current_marker.addTo(map);
    home_marker = L.marker([55.82995, 37.4783], {title: 'Home', icon: home_icon, opacity: 0.8}).bindPopup('Home');
    home_marker.addTo(map);
    // create a red polyline from an array of LatLng points
    var route_points = [
        [55.82995, 37.4783],
        [55.83995, 37.4883],
    ];
    var route = L.polyline(route_points, {color: 'black'});
    route.addTo(map);
    // zoom the map to the polyline
    map.fitBounds(route.getBounds());

    var control_speed = $("#controlSpeed")
    var control_speed_num = $("#controlSpeedNum")
    var control_angle = $("#controlAngle")
    var control_angle_num = $("#controlAngleNum")
    var control_led1 = $("#controlLed1")
    var control_led2 = $("#controlLed2")
    var control_stop = $("#controlStop")
    var telemetry_speed = $("#telemetrySpeed")
    var telemetry_angle = $("#telemetryAngle")
    var telemetry_led1 = $("#telemetryLed1")
    var telemetry_led2 = $("#telemetryLed2")
    var telemetry_dist_to_home = $("#telemetryDistToHome")
    var telemetry_dist_total = $("#telemetryDistTotal")
    var alert_container = $("#alert-container")
    var image = $("#image")
    var map_set_home = $("#mapSetHome")
    var map_clear_track = $("#mapClearTrack")
    var get_control_speed = function(){return parseFloat(control_speed.val());};
    var get_control_speed_num = function(){return parseFloat(control_speed_num.html());};
    var get_control_angle = function(){return parseFloat(control_angle.val());};
    var get_control_angle_num = function(){return parseFloat(control_angle_num.html());};
    var get_control_led1 = function(){return control_led1.is(":checked");};
    var get_control_led2 = function(){return control_led2.is(":checked");};
    var set_control_speed = function(val){control_speed.val(String(val));set_control_speed_num(val);};
    var set_control_speed_num = function(val){control_speed_num.html(String(val));};
    var set_control_angle = function(val){control_angle.val(String(val));set_control_angle_num(val);};
    var set_control_angle_num = function(val){control_angle_num.html(String(val));};
    var set_control_led1 = function(val){control_led1.prop("checked", val);};
    var set_control_led2 = function(val){control_led2.prop("checked", val);};
    var get_telemetry_speed = function(){return parseFloat(telemetry_speed.html());};
    var get_telemetry_angle = function(){return parseFloat(telemetry_angle.html());};
    var get_telemetry_led1 = function(){return telemetry_led1.html() == "on";};
    var get_telemetry_led2 = function(){return telemetry_led2.html() == "on";};
    var get_telemetry_dist_to_home = function(){return parseFloat(telemetry_dist_to_home.html());};
    var get_telemetry_dist_total = function(){return parseFloat(telemetry_dist_total.html());};
    var set_telemetry_speed = function(val){telemetry_speed.html(String(val));};
    var set_telemetry_angle = function(val){telemetry_angle.html(String(val));};
    var set_telemetry_led1 = function(val){if(val)telemetry_led1.html("on");else telemetry_led1.html("off");};
    var set_telemetry_led2 = function(val){if(val)telemetry_led2.html("on");else telemetry_led2.html("off");};
    var set_telemetry_dist_to_home = function(val){telemetry_dist_to_home.html(String(val));};
    var set_telemetry_dist_total = function(val){telemetry_dist_total.html(String(val));};
    var set_image = function(val){image.attr('src', val);}
    var unique_id = function(prefix) {
        return prefix + Math.floor(Math.random() * 1000) + Date.now();
    };
    var bootstrap_alert = function(type, message){
//        var id = unique_id("alert")
//        alert_container.prepend(
//            '<div id="'+id+'" class="alert alert-'+type+'" role="alert" style="margin: 5px; padding: 5px; font-size: 8pt;">'+message+'</div>'
//        );
//        setTimeout(function(){$("#"+id).fadeOut(1000, function(){$(this).remove()});}, 1000);
    };
    var submit_control = function(){
        data = {
            "speed": get_control_speed(),
            "angle": get_control_angle(),
            "led1": get_control_led1(),
            "led2": get_control_led2()
        };
        str_data = JSON.stringify(data);
        $.ajax({
            type: 'post',
            url: control_url,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: str_data,
            success: function(data){bootstrap_alert('success', str_data);},
            error: function(data){bootstrap_alert('danger', str_data);}
        });
    };
    var update_control = function(data){
        set_control_speed(data["speed"]);
        set_control_angle(data["angle"]);
        set_control_led1(data["led1"]);
        set_control_led2(data["led2"]);
    };
    var update_telemetry = function(data){
        set_telemetry_speed(data['speed']);
        set_telemetry_angle(data['angle']);
        set_telemetry_led1(data['led1']);
        set_telemetry_led2(data['led2']);
        set_telemetry_dist_to_home(data['dist_to_home']);
        set_telemetry_dist_total(data['dist_total']);
        current_marker.setLatLng(data['current_lat_lng']);
        home_marker.setLatLng(data['home_lat_lng']);
        route.setLatLngs(data['route_lat_lng']);
        map.fitBounds(route.getBounds());
    };
    var zero_control = function(){
        var data = {
            'speed': 0.0,
            'angle': 0.0,
            'led1': false,
            'led2': false
        };
        update_control(data);
        submit_control();
    };
    var submit_map = function(set_home, clear_track){
        data = {
            "set_home": set_home,
            "clear_track": clear_track,
        };
        str_data = JSON.stringify(data);
        $.ajax({
            type: 'post',
            url: '/map',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: str_data,
            success: function(data){bootstrap_alert('success', str_data);},
            error: function(data){bootstrap_alert('danger', str_data);}
        });
    };
    control_speed.on('input change', function(e){
        e.preventDefault();
        set_control_speed_num(get_control_speed());
        submit_control();
    });
    control_angle.on('input change', function(e){
        e.preventDefault();
        set_control_angle_num(get_control_angle());
        submit_control();
    });
    control_led1.on('change', function(e){
        e.preventDefault();
        submit_control();
    });
    control_led2.on('change', function(e){
        e.preventDefault();
        submit_control();
    });
    control_stop.on('click', function(e){
        e.preventDefault();
        zero_control();
    });
    map_set_home.on('click', function(e){
        e.preventDefault();
        submit_map(true, true);
    });
    map_clear_track.on('click', function(e){
        e.preventDefault();
        submit_map(false, true);
    });
    (function telemetry_worker(){
        $.ajax({
            type: 'get',
            url: telemetry_url,
            success: function(data) {update_telemetry(data);},
            complete: function() {setTimeout(telemetry_worker, telemetry_period);}
        });
    })();
    zero_control();
});
