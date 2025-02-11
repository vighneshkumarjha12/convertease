 // Dark Mode Toggle Script
 function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }

    document.addEventListener('DOMContentLoaded', () => {
        const dropdownBtn = document.querySelector('.dropdown-btn');
        const dropdownMenu = document.querySelector('.dropdown-menu');
    
        dropdownBtn.addEventListener('click', () => {
            dropdownMenu.style.display =
                dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
    
        // Close the dropdown if clicked outside
        document.addEventListener('click', (event) => {
            if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
    });
    
});
