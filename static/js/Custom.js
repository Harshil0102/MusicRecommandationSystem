function displayLoader() {
    const overlay = document.getElementById('overlay');
    const loader = document.getElementById('loader');

    // Show the overlay and loader
    overlay.style.display = 'flex';
    loader.style.display = 'block';
}

function stopLoader() {
    const overlay = document.getElementById('overlay');
    const loader = document.getElementById('loader');

    // Hide the overlay and loader
    overlay.style.display = 'none';
    loader.style.display = 'none';
}
