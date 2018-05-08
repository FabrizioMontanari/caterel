const countDownDate = new Date("Sep 18, 2018 12:00:00").getTime();

const getClassName = name => `.martini-countdown__${name}`;

const updateCountdown = counters => {
	const distance = countDownDate - new Date().getTime();

	if (distance < 0) {
		return counters.clock.innerHTML = 'Si sono sposati!';
	}

	const days = Math.floor(distance / (1000 * 60 * 60 * 24));
	const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	/*const seconds = Math.floor((distance % (1000 * 60)) / 1000);*/

	counters.days.innerHTML = `${days}D&nbsp;`;
	counters.hours.innerHTML = `&nbsp;${hours}H&nbsp;`;
	counters.minutes.innerHTML = `&nbsp;${minutes}M`;
	/*counters.seconds.innerHTML = `${seconds}S`;*/

	setTimeout(() => updateCountdown(counters), 60000);
};

const initialise = () => {
	const counterElements = {
		days: document.querySelector(getClassName('clock-days')),
		hours: document.querySelector(getClassName('clock-hours')),
		minutes: document.querySelector(getClassName('clock-minutes')),
		seconds: document.querySelector(getClassName('clock-seconds')),
		clock: document.querySelector(getClassName('clock'))
	}

	updateCountdown(counterElements);
}

document.addEventListener('DOMContentLoaded', initialise);