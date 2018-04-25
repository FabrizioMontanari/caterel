// Set the date we're counting down to
var countDownDate = new Date("Sep 18, 2018 12:00:00").getTime();

function updateTimer(){
	// Get todays date and time
	var now = new Date().getTime();

	// Find the distance between now an the count down date
	var distance = countDownDate - now;

	// Time calculations for days, hours, minutes and seconds
	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	// Display the result in the element
	$(".martini-timer__title__timer").html( days + "d " + hours + "h " + minutes + "m " + seconds + "s ");

	// If the count down is finished, write some text 
	if (distance < 0) {
	$(".martini-timer__title__timer").html("EXPIRED");
	return false;
	}
	return true;
}

$(document).ready(function () {
	updateTimer();
	// Update the count down every 1 second
	var x = setInterval(function() {
		if (!updateTimer()) clearInterval(x);
	}, 1000);
});