const elementIsVisible = function (el) { return el && el.style.maxHeight; }

const hideElement = function (el) { el.style.maxHeight = null; }

const showElement = function (el) { el.style.maxHeight = el.scrollHeight + "px"; }

const toggleVisibility = function (el) { elementIsVisible(el) ? hideElement(el) : showElement(el); }

const initGiftToggle = function () {
    const giftDetails = document.querySelector('.martini-gift__gift-details');
    const toggleLink = document.querySelector('.martini-gift__toggle-details');

    hideElement(giftDetails);
    toggleLink.addEventListener('click', function () { toggleVisibility(giftDetails) });
};

document.addEventListener('DOMContentLoaded', initGiftToggle);