
$(document).ready(function() {	

	//select all the a tag with name equal to modal
	$('a[name=modal]').click(function(e) {
		//Cancel the link behavior
		e.preventDefault();
		
		//Get the A tag
		var id = $(this).attr('href');
	
		//Get the screen height and width
		var maskHeight = $(document).height();
		var maskWidth = $(window).width();
	
		//Set heigth and width to mask to fill up the whole screen
		$('#mask').css({'width':maskWidth,'height':maskHeight});
		
		//transition effect		
		$('#mask').fadeIn(400);	
		$('#mask').fadeTo("slow",0.8);	
	
		//Get the window height and width
		var winH = $(window).height();
		var winW = $(window).width();
              
		//Set the popup window to center
		$(id).css('top',  winH/2-$(id).height()/2);
		$(id).css('left', -(winW/2-$(id).width()/4));
//		$(id).css('top',  winH/2-$(id).height()/2);
//		$(id).css('left', winW/2-$(id).width()/2);
	
		//transition effect
		$(id).fadeIn(200); 
	
	});
	
	//if close button is clicked
	$('.window .close').click(function (e) {
		//Cancel the link behavior
		e.preventDefault();
		
		$('#mask').hide();
		$('.window').hide();
	});		
	
	//if mask is clicked
	$('#mask').click(function () {
		$(this).hide();
		$('.window').hide();
	});			
	
});

$(document).ready(function() {
	$('.error').hide();
	$('.userid').blur(function() {
		data = $('.userid').val();
		var len = data.length;
		if (len < 1) {
			$('.userid').next().show();
			$('.password').attr('disabled',true);
			$('.confpass').attr('disabled',true);
		}
		else {
			$('.userid').next().hide();
			$('.password').removeAttr('disabled');
			$('.confpass').removeAttr('disabled');
		}
	});

	$('.password').blur(function() {
		data = $('.password').val();
		var len = data.length;
		if (len < 1) {
			$('.password').next().show();
			$('.confpass').attr('disabled', true);
		}
		else {
			$('.password').next().hide();
			$('.confpass').removeAttr('disabled');
		}
	});

	$('.confpass').blur(function() {
		if ($('.password').val() != $('.confpass').val()) {
			$('.confpass').next().show();
		}
		else {
			$('.confpass').next().hide();
		}
	});

	$('.submit').click(function(event) {
		var uid = $('.userid').val();
		if (validate_userid(uid)) {
			$('.error').hide();
		}
		var eml = $('.email').val();
		if (validate_email(eml)) {
			$('.error').hide();
		}
		else {
			$('.error').show();
			event.preventDefault();
		}
	});
});

function validate_userid(uid) {
	var pattern = new RegExp(/^[a-z0-9_]+$/);
	return pattern.test(uid);
}

function validate_email(email) {
	var pattern = new RegExp(/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]+$/);
	return pattern.test(email);
}