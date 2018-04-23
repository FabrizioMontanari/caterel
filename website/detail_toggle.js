const giftDetails = document.querySelector('.martini-gift__gift-details');
const toggleLink = document.querySelector('.martini-gift__toggle-details');

const elementIsVisible = el => el && el.style && el.style.display === 'block'; 

const hideElement = el => el.style.display = 'none';

const showElement = el => el.style.display = 'block';

const toggleVisibility = () => elementIsVisible(giftDetails) ? hideElement(giftDetails) : showElement(giftDetails);

toggleLink.addEventListener('click',toggleVisibility);