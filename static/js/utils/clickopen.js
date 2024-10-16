// Notification Panel Toggle
const notificationButton = document.getElementById('notificationButton');
const notificationPanel = document.getElementById('notificationPanel');

notificationButton.addEventListener('click', () => {
    notificationPanel.classList.toggle('hidden');
    userMenuDropdown.classList.add('hidden');
});

// User Menu Dropdown Toggle
const userMenuButton = document.getElementById('userMenuButton');
const userMenuDropdown = document.getElementById('userMenuDropdown');

userMenuButton.addEventListener('click', () => {
    userMenuDropdown.classList.toggle('hidden');
    notificationPanel.classList.add('hidden');
});

// Close dropdowns when clicking outside
document.addEventListener('click', (event) => {
    if (!notificationButton.contains(event.target) && !notificationPanel.contains(event.target)) {
        notificationPanel.classList.add('hidden');
    }
    if (!userMenuButton.contains(event.target) && !userMenuDropdown.contains(event.target)) {
        userMenuDropdown.classList.add('hidden');
    }
});