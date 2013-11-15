var change_in_my_list = function() {
	$("#save_btn").html('Czekaj...');
};

var save_flavour = function() {
	change_in_my_list();
	var track_id = 0;
	var menu_id = $(".menu_pos:checked").val();
	
	$.post('/flavour/set/' + menu_id + '?xhr',
			{
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
					$("#save_btn").html('Zapisz');
				}
	    }, 'json');
};

