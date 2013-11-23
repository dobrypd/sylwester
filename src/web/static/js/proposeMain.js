var change_in_my_list = function() {
	$("#proposelist").hide('slow');
	$("#proposelist").html('<img id="indicator" src="static/img/ajax-loader.gif" alt="Loading..." />');
	$("#proposelist").show('slow');
};


var thumb_up = function(prop_id) {
	change_in_my_list();
	
	$.getJSON('/propose/thumb_up/' + prop_id + '?xhr',
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
				load_list();
			}
    });
};

var thumb_down = function(prop_id) {
	change_in_my_list();
	
	$.getJSON('/propose/thumb_down/' + prop_id + '?xhr',
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
				load_list();
			}
    });
};

var add_new_prop = function() {
	change_in_my_list();
	var track_id = 0;
	var prop_text = $('#prop_text').val();
	
	$.post('/propose/add_new_proposition/?xhr',
			{
				'text': prop_text,
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
					load_list();
				}
	    }, 'json');
};


var comment_on = function(prop_id) {
	var track_id = 0;
	var comment_text = $('#comment_text' + prop_id).val();
	
	change_in_my_list();
	
	$.post('/propose/add_new_comment/?xhr',
			{
				'proposition_id': prop_id,
				'text': comment_text || '',
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
					load_list();
				}
	    }, 'json');
};


var show_comment_box = function(prop_id) {
	$("#comment_btn_" + prop_id).addClass("disabled");
	document.getElementById("comment_btn_" + prop_id).onclick = function (){return false;};
	var text_col = $("#comment_box_" + prop_id);
	text_col.append("<br /> "
	+ "<form class=\"form-inline\">"
	+ "     <div class=\"col-xs-3\">"
	+ "       <input id=\"comment_text" + prop_id + "\" type=\"text\" class=\"form-control\"> <hr>"
	+ "       <button class=\"btn\" type=\"button\" onclick=\"comment_on(" + prop_id + "); return false;\"> <i class=\"glyphicon glyphicon-comment\"></i> dodaj</button>"
	+ "     </div>"
	+ "</form>"
	);
	
};


var draw_list = function(where, list_in_json) {
	where.html("");
	$.each(list_in_json, function(index) {
		var row = $("<tr>");
		var propose = list_in_json[index];

		row.append("<td>" + propose.user + "</td>");
		var text_col = $("<td>" + propose.text + "</td>");
		
		/*load comments*/
		var comment_table = $("<table>");
		$.each(propose.comments, function(index) {
			var comment_row = $("<tr>");
			var comment = propose.comments[index];
			
			comment_row.append("<td><small>" + comment.user + "</small></td>");
			comment_row.append("<td><small>" + comment.comment + "</small></td>");
			
			comment_table.append(comment_row);
		});
		
		text_col.append(comment_table);
		text_col.append("<div id=\"comment_box_"
				+ propose.id + "\" />");

		row.append(text_col);

		row.append("<td>"
				+ "<button class=\"btn btn-small btn-success mybtnthumb\" onclick=\""
				+ "thumb_up(" + propose.id + "); return false;"
				+ "\"><i class=\"glyphicon glyphicon-thumbs-up\"></i> <small>"
				+ propose.thumbs_up
				+ "</small></button> "
				+ "<button class=\"btn btn-small btn-danger mybtnthumb\" onclick=\""
				+ "thumb_down(" + propose.id + "); return false;"
				+ "\"><i class=\"glyphicon glyphicon-thumbs-down\"></i> <small>"
				+ propose.thumbs_down
				+ "</small></button>"
				+ "<button class=\"btn btn-small btn-info mybtnthumb\" "
				+ "id=\"comment_btn_" + propose.id + "\" onclick=\""
				+ "show_comment_box(" + propose.id + "); return false;"
				+ "\"><i class=\"glyphicon glyphicon-comment\"></i> <small>"
				+ "Skomentuj"
				+ "</small></button>"
				+"</td>");
		
		where.append(row);
	});
};


var load_list = function(){
	var list = $("#proposelist");

	$.getJSON('/propose/get_list?xhr',
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
	load_list();
});