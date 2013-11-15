var change_in_my_list = function() {
	$("#mylist").hide('slow');
	$("#mylist").html('<img id="indicator" src="static/img/ajax-loader.gif" alt="Loading..." />');
	$("#mylist").show('slow');
	
};

var add_new_track = function() {
	change_in_my_list();
	var track_id = 0;
	var track_name = $('#track_name').val();
	var track_link = $('#track_link').val();
	
	$.post('/playlist/add_new_track/?xhr',
			{
				'track_name': track_name,
				'track_link': track_link,
				'csrfmiddlewaretoken': current_token,
			},
			function(json, status, xhr) {
				if (status == "error") {
					var msg = "K%%%a coś nie działa :/ sory ";
					msg += xhr.status + " " + xhr.statusText;
					my_alert(msg, null, true);
	  			}
				if (status == "success") {
					if (json[0] != "OK") {
						my_alert(null, json);
						load_my_list();
					} else {;
						track_id = json[1]
						add_track(track_id);
					}
				}
	    }, 'json');
};

var add_track = function(track_id) {
	change_in_my_list();
	
	$.getJSON('/playlist/add_track/' + track_id + '?xhr',
		{}, 
		function(json, status, xhr) {
			if (status == "error") {
				var msg = "K%%%a coś nie działa :/ sory ";
				msg += xhr.status + " " + xhr.statusText;
				my_alert(msg, null, true);
  			}
			if (status == "success") {
				if (json != "OK") {
					my_alert(null, json);
				};
				load_my_list();
			}
    });
};

var remove_track = function(track_id) {
	change_in_my_list();
	
	$.getJSON('/playlist/remove_track/' + track_id + '?xhr',
		{}, 
		function(json, status, xhr) {
			if (status == "error") {
				var msg = "K%%%a coś nie działa :/ sory ";
				msg += xhr.status + " " + xhr.statusText;
				my_alert(msg, null, true);
  			}
			if (status == "success") {
				if (json != "OK") {
					my_alert(null, json);
				};
				load_my_list();
			}
    });
};

var draw_list = function(where, list_in_json, is_my) {
	var this_already_is_new_year = false;
	if (list_in_json[0].position != undefined) {
		this_already_is_new_year = true;
	} 
	where.html("");
	$.each(list_in_json, function(index) {
		var row = $("<tr>");
		var track = list_in_json[index];
		if (this_already_is_new_year)
		{
			if (track.link) {
				row.append("<td><a href=\"" + track.link + "\">"
						+ track.name + "</a></td>");
			} else {
				row.append("<td>" + track.name + "</td>");
			}
		} else {
			if (track.link) {
				row.append("<td><a href=\"" + track.link + "\">"
						+ track.name + "</a></td>");
			} else {
				row.append("<td>" + track.name + "</td>");
			}
			if (is_my) {
				row.append("<td><button class=\"btn btn-small\" onclick=\""
						+ "remove_track("
						+ track.id
						+ "); return false;"
						+ "\"><i class=\"icon-minus-sign\"></i></button></td>");
			} else {
				row.append("<td><button class=\"btn btn-small\" onclick=\""
						+ "add_track("
						+ track.id
						+ "); return false;"
						+ "\"><i class=\"icon-plus-sign\"></i></button></td>");
			}
		}
		where.append(row);
	});
};


var load_my_list = function(){
	var my_list = $("#mylist");

	//my_list.hide('slow');

	$.getJSON('/playlist/get_my_list?xhr',
		{}, 
		function(json, status, xhr) {
			if (status == "error") {
				var msg = "K%%%a coś nie działa :/ sory ";
				msg += xhr.status + " " + xhr.statusText;
				my_alert(msg, null, true);
  			}
			if (status == "success") {
				draw_list(my_list, json, true);
			}
    });
	
	my_list.show('slow');
};


var load_list = function(){
	var list = $("#list");

	$.getJSON('/playlist/get_list/50?xhr',
		{}, 
		function(json, status, xhr) {
			if (status == "error") {
				var msg = "K%%%a coś nie działa :/ sory ";
				msg += xhr.status + " " + xhr.statusText;
				my_alert(msg, null, true);
  			}
			if (status == "success") {
				list.hide('slow');
				draw_list(list, json, false);
				list.show('slow');
			}
    });
};


var reload_playlist = function() {
	load_list();
}



$(document).ready(function(){
	load_my_list();
	load_list();
});