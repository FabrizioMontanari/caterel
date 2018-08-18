var elementIsVisible = function (el) { return el && el.style.maxHeight; }

var hideElement = function (el) { el.style.maxHeight = null; }

var showElement = function (el) { el.style.maxHeight = el.scrollHeight + "px"; }

var toggleVisibility = function (el) { elementIsVisible(el) ? hideElement(el) : showElement(el); }

var initGiftToggle = function () {
    var giftDetails = document.querySelector('.martini-gift__gift-details');
    var toggleLink = document.querySelector('.martini-gift__toggle-details');

    hideElement(giftDetails);
    toggleLink.addEventListener('click', function () { toggleVisibility(giftDetails) });
};

document.addEventListener('DOMContentLoaded', initGiftToggle);