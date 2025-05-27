// Select elements
const sidebar = document.getElementById('sidebar');
const toggleButton = document.getElementById('toggle-button');

// Function to toggle sidebar visibility
function toggleSidebar() {
    if (sidebar.classList.contains('open')) {
        sidebar.classList.remove('open'); // Close the sidebar
        sidebar.classList.add('close');   // Add closing animation
    } else {
        sidebar.classList.remove('close'); // Remove closing animation
        sidebar.classList.add('open');      // Open the sidebar
    }
}

// Event listener for the toggle button
toggleButton.addEventListener('click', toggleSidebar);