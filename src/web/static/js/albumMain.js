var change_list = function() {
	$("#comment_list").hide('slow');
	$("#comment_list").html('<img id="indicator" src="../../../static/img/ajax-loader.gif" alt="Loading..." />');
	$("#comment_list").show('slow');
	
};


var add_new_comment = function(album_name) {

	var track_id = 0;
	var text = $('#comment_text').val();
	
	change_list();
	
	$.post('/photos/add_new_album_comment/?xhr',
			{
				'text': text,
				'album_name': album_name,
				'csrfmiddlewaretoken': current_token,
			},
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
					load_list(album_name);
				}
	    }, 'json');
};


var draw_list = function(where, list_in_json, is_my) {
	where.html("");
	$.each(list_in_json, function(index) {
		var row = $("<tr>");
		var comment = list_in_json[index];
		row.append("<td>" + comment.user + "</td>");
		row.append("<td>" + comment.comment + "</td>");
		where.append(row);
	});
};


var load_list = function(album_name){
	var list = $("#comment_list");

	$.getJSON('/photos/get_album_comments/'+ album_name +'?xhr',
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

$(document).ready(function(){
	load_list(album_name);
});