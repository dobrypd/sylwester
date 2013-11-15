var my_alert = function(msg, json, is_fatal) {
	if (is_fatal == undefined) {
		is_fatal = false;
	}
	if (is_fatal) {
		$('#fatal_error').modal();
		$('.error_msg').append("<br /> Błąd: " + msg);
	} else {
		$('#normal_error').modal();
		if (json == "ToMuch"){
			$('.error_msg').html("Wyczerpałeś swój limit, musisz coś usunąć ze swojej listy");
		} else if (json == "TrackDoesNotExist"){
			$('.error_msg').html("Coś poszło nie tak, taki utwór nie istnieje.");
		} else if (json == "VoteDoesNotExist"){
			$('.error_msg').html("Coś poszło nie tak, utwór nie istnieje na Twojej liście.");
		} else if (json == "DoesNotExist"){
			$('.error_msg').html("Coś poszło nie tak, taki utwór nie istnieje.");
		} else if (json == "AlreadyVoted"){
			$('.error_msg').html("Sory ale już wcześniej zagłosowałeś.");
		} else if (json == "MenuDoesNotExist"){
			$('.error_msg').html("Nie ma takiej pozycji w menu.");
		} else {
			$('.error_msg').html("Coś poszło nie tak, jakiś kijowy błąd, "
					+"spróbuj za chwilę ponownie. ( albo wyślij mi: " + json + ").");
		}
	};
}