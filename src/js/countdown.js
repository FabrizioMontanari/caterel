var countDownDate = new Date("Sep 22, 2018 12:00:00").getTime();

var getClassName = function (name) { return '.martini-countdown__banner-element__central__clock' + name; }

var updateCountdown = function (counters) {
	var distance = countDownDate - new Date().getTime();

	if (distance < 0) {
		return counters.clock.innerHTML = 'Si sono sposati!';
	}

	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

	counters.days.innerHTML = days + 'D&nbsp;';
	counters.hours.innerHTML = '&nbsp;' + hours + 'H&nbsp;';
	counters.minutes.innerHTML = '&nbsp;' + minutes + 'M';

	setTimeout(function () { updateCountdown(counters) }, 60000);
};

var initialise = function () {
	var counterElements = {
		days: document.querySelector(getClassName('-days')),
		hours: document.querySelector(getClassName('-hours')),
		minutes: document.querySelector(getClassName('-minutes')),
		clock: document.querySelector(getClassName(''))
	}

	updateCountdown(counterElements);
}

document.addEventListener('DOMContentLoaded', initialise);
