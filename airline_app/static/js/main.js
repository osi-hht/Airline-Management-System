document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll behavior
    const navbar = document.getElementById('mainNav');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (navbar) {
        updateNavbarTransparency();
        window.addEventListener('scroll', updateNavbarTransparency);
    }
    
    function updateNavbarTransparency() {
        if (window.scrollY > 50) {
            navbar.classList.add('nav-scrolled');
            navbar.querySelectorAll('a:not(.btn-primary)').forEach(item => {
                item.classList.remove('text-white');
                item.classList.add('text-airline-blue-900');
            });
        } else {
            navbar.classList.remove('nav-scrolled');
            navbar.querySelectorAll('a:not(.btn-primary)').forEach(item => {
                item.classList.add('text-white');
                item.classList.remove('text-airline-blue-900');
            });
        }
    }
    
    // Mobile menu toggle
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Form validation and enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.classList.add('border-red-500');
            });
            
            input.addEventListener('input', function() {
                this.classList.remove('border-red-500');
            });
        });
    });
    
    // Add fade-in animation to elements
    const fadeElements = document.querySelectorAll('.fade-in-element');
    if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
        const fadeInObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    fadeInObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(element => {
            fadeInObserver.observe(element);
        });
    } else {
        fadeElements.forEach(element => {
            element.classList.add('fade-in');
        });
    }
});