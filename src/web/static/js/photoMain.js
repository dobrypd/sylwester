var current_width = 0;
var current_height = 0;
var play_interval_id;
var played = false;

var change_list = function() {
	$("#comment_list").hide('slow');
	$("#comment_list").html('<img id="indicator" src="../../../static/img/ajax-loader.gif" alt="Loading..." />');
	$("#comment_list").show('slow');
	
};

var change_image = function() {
	$(".photo_content").html('<div style="width: '
			+ current_width
			+ 'px; height: '
			+ current_height
			+ 'px; background-image: url(\'../../static/img/ajax-loader-black.gif\');'
			+ 'background-repeat:no-repeat;'
			+ 'background-position:center center;'
			+ '">'
			+'</div>');
};

resize_img = function()
{
	var new_width = current_width;
	var new_height = current_height;
	var scale = 1;
	if (new_width > ($(window).width() - 50)) {
		scale = ($(window).width() - 50) / new_width;
	};
	if (new_height > ($(window).height() - 70)) {
		scale = Math.min(($(window).height() - 70) / new_height, scale);
	};
	if (scale < 1) {
		new_width = new_width * scale;
		new_height = new_height * scale;
	}
	
	$(".main-img").width(new_width).height(new_height);
}


draw_img = function(img) {
	image = $("<img />");
	image.addClass("main-img").addClass("rounded")
	.attr('src', img.url);
	current_width = img.width;
	current_height = img.height;
	$(".photo_content").append(image);
	resize_img();
}

image_loaded = function(image){
	$(".photo_content").html("");
	$("#galery").attr('href', '/photos/album/' + image.album);
	$("#prev_img").attr('href', '#' + image.previous);
	$("#next_img").attr('href', '#' + image.next);
	$("#play_img").attr('href', '#' + image.photoid);
	var best_content = image.content[0];
	$.each(image.content, function(index) {
		if (best_content.width < image.content[index]) {
			best_content = image.content[index];
		}
	});
	draw_img(best_content);
	$(".photo_content").fadeIn("slow");
} 

load_image = function(ident) {
	$(".photo_content").fadeOut('slow', function() {
		change_image();
		$.getJSON('/photos/get_photo/' + ident + '/?xhr',
			{},
			function(json, status, xhr) {
				if (status == "error") {
					var msg = "K%%%a coś nie działa :/ sory ";
					msg += xhr.status + " " + xhr.statusText;
					my_alert(msg, null, true);
	  			}
				if (status == "success") {
					image_loaded(json);
				}
	    });
	});
};



var add_new_comment = function() {

	var photo_id = window.location.hash.substring(1);
	var text = $('#comment_text').val();
	if(window.location.hash) {
		change_list();
		
		$.post('/photos/add_new_photo_comment/?xhr',
				{
					'text': text,
					'photoid': photo_id,
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
	}
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


var load_list = function(){
	var list = $("#comment_list");

	if(window.location.hash) {
		var photo_id = window.location.hash.substring(1);
		$.getJSON('/photos/get_photo_comments/'+ photo_id +'?xhr',
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
	}
};



$(window).resize(function() {
	resize_img();
});

$(window).bind('hashchange', function() {
	var hash = "5776246352182732562"
	if(window.location.hash) {
		var hash = window.location.hash.substring(1);
		load_image(hash);
		load_list();
	};
	
});


play = function() {
	if (played) {
		document.location.hash = $("#next_img").attr('href');
	};
}

$(document).keydown(function(e){
    if (e.keyCode == 39) { 
       document.location.hash = $("#prev_img").attr('href');
       return false;
    }
    else if (e.keyCode == 37) {
    	document.location.hash = $("#next_img").attr('href');
    	return false;
    }
});

$(document).ready(function(){
	var hash = "5776246352182732562"
	if(window.location.hash) {
		var hash = window.location.hash.substring(1);
		load_image(hash);
		load_list();
	};
	
	$("#play_img").click(function(event) {
		played = !played;
		if (played) {
			$("#play_icon").removeClass("icon-play");
			$("#play_icon").addClass("icon-pause");
			play_interval_id = setInterval(play, 5000);
		} else {
			$("#play_icon").removeClass("icon-pause");
			$("#play_icon").addClass("icon-play");
			clearInterval(play_interval_id);
		}
	});
});