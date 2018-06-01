const elementIsVisible = el => el && el.style.maxHeight//el && el.style && el.style.display !== 'none'; 

const hideElement = el => el.style.maxHeight=null;//el.style.display = 'none';

const showElement = el => el.style.maxHeight = el.scrollHeight + "px";//el.style.removeProperty('display');

const toggleVisibility = el => elementIsVisible(el) ? hideElement(el) : showElement(el);

const initialise_gift_details = () => {
    const giftDetails = document.querySelector('.martini-gift__gift-details');
    const toggleLink = document.querySelector('.martini-gift__toggle-details');

    hideElement(giftDetails);
    toggleLink.addEventListener('click', () => toggleVisibility(giftDetails));
};

document.addEventListener('DOMContentLoaded', initialise_gift_details);