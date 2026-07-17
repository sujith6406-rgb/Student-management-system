// Confirm before deleting a student
function confirmDelete(name) {
    return confirm(`Are you sure you want to delete ${name}?`);
}

// Simple client-side form validation feedback
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('studentForm');

    if (form) {
        form.addEventListener('submit', function (e) {
            const rollNo = document.getElementById('roll_no').value.trim();
            const name = document.getElementById('name').value.trim();

            if (rollNo.length === 0 || name.length === 0) {
                alert('Name and Roll Number cannot be empty.');
                e.preventDefault();
            }
        });
    }

    // Auto-hide flash messages after 4 seconds
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.transition = 'opacity 0.4s ease';
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 400);
        }, 4000);
    });

    console.log('Student Management System loaded successfully.');
});
