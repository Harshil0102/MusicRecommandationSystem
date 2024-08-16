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

function logout()
{
    Swal.fire({
        title: "Are you sure want to logout?",
        showCancelButton: true,
        confirmButtonText: "Yes",
        denyButtonText: `No`
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            window.location.href = "/";
        } 
      });
}