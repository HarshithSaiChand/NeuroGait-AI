// Main JavaScript File

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.2)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        }
    }
});

// Auto-hide alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        // Use Bootstrap 5 alert close method if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        } else {
            alert.style.display = 'none';
        }
    });
}, 5000);

console.log('NeuroGait AI - Website loaded successfully!');