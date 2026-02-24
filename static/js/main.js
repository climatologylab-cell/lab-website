// Main JavaScript for Climatology Lab Website

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const contactForms = document.querySelectorAll('.contact-form');
    
    contactForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const email = form.querySelector('input[type="email"]');
            const query = form.querySelector('textarea[name="query"]');
            
            if (!email.value || !query.value) {
                e.preventDefault();
                alert('Please fill in all required fields');
                return false;
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
