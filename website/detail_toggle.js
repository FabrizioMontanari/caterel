const elementIsVisible = el => el && el.style && el.style.display !== 'none'; 

const hideElement = el => el.style.display = 'none';

const showElement = el => el.style.removeProperty('display');

const toggleVisibility = el => elementIsVisible(el) ? hideElement(el) : showElement(el);

const initialise = () => {
    const giftDetails = document.querySelector('.martini-gift__gift-details');
    const toggleLink = document.querySelector('.martini-gift__toggle-details');

    hideElement(giftDetails);
    toggleLink.addEventListener('click', () => toggleVisibility(giftDetails));
};

document.addEventListener('DOMContentLoaded', initialise);