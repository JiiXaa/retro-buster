// Navigation:

// Toggle Nav
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');
const navLinks = document.querySelectorAll('.nav-links li');

// Toggle Nav
burger.addEventListener('click', () => {
  nav.classList.toggle('nav-active');
  // Toggle Scroll Bar on/off when nav is open
  document.body.classList.toggle('no-scroll');

  // Animate Links
  navLinks.forEach((link, index) => {
    if (link.style.animation) {
      link.style.animation = '';
    } else {
      link.style.animation = `navLinkFade 0.5s ease forwards ${
        index / 7 + 0.3
      }s`;
    }
  });

  // Burger Animation
  burger.classList.toggle('toggle');
});

// Setting timeout for the alert message to disappear after 5 seconds
setTimeout(() => {
  const flashMessage = document.querySelector('.alert');

  if (flashMessage) flashMessage.style.display = 'none';
}, 5000);
