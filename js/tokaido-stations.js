// Tokaido Stations Page JavaScript
// Handles filtering, search, and navigation functionality

document.addEventListener('DOMContentLoaded', () => {
  console.log('Tokaido Stations JS Loaded');

  // Initialize all features
  initializeFiltering();
  initializeSearch();
  initializeMobileMenu();
  initializeScrollEffects();
});

// ========================================
// Filtering System
// ========================================
function initializeFiltering() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const stationCards = document.querySelectorAll('.station-card');

  if (filterButtons.length === 0 || stationCards.length === 0) {
    console.log('Filter elements not found');
    return;
  }

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;

      // Update active button
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');

      // Apply filter
      stationCards.forEach(card => {
        if (filter === 'all') {
          card.style.display = '';
        } else {
          // Check if card has the filter class
          if (card.classList.contains(filter)) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        }
      });

      // Auto-scroll to the selected area section (except for "all")
      if (filter !== 'all') {
        const targetSection = document.querySelector(`#${filter}-area`);
        if (targetSection) {
          const headerOffset = 80;
          const elementPosition = targetSection.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      }

      console.log(`Filter applied: ${filter}`);
    });
  });

  console.log('Filtering initialized');
}

// ========================================
// Search Functionality
// ========================================
function initializeSearch() {
  const searchBox = document.getElementById('search-box');
  const stationCards = document.querySelectorAll('.station-card');

  if (!searchBox || stationCards.length === 0) {
    console.log('Search elements not found');
    return;
  }

  searchBox.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();

    stationCards.forEach(card => {
      const stationName = card.querySelector('h3')?.textContent.toLowerCase() || '';
      const stationReading = card.querySelector('.station-reading')?.textContent.toLowerCase() || '';
      const stationDescription = card.querySelector('.station-description')?.textContent.toLowerCase() || '';

      const matches =
        stationName.includes(searchTerm) ||
        stationReading.includes(searchTerm) ||
        stationDescription.includes(searchTerm);

      card.style.display = matches || searchTerm === '' ? '' : 'none';
    });

    console.log(`Search: ${searchTerm}`);
  });

  console.log('Search initialized');
}

// ========================================
// Mobile Menu
// ========================================
function initializeMobileMenu() {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (!hamburger || !mobileMenu) {
    console.log('Mobile menu elements not found');
    return;
  }

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
  });

  // Close menu when clicking on a link
  const mobileLinks = mobileMenu.querySelectorAll('a');
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('active');
    });
  });

  console.log('Mobile menu initialized');
}

// ========================================
// Scroll Effects
// ========================================
function initializeScrollEffects() {
  const areaNavBtns = document.querySelectorAll('.area-nav-btn');

  areaNavBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('href');
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        const headerOffset = 80;
        const elementPosition = targetSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  console.log('Scroll effects initialized');
}
