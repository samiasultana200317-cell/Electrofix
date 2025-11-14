class ElectroFixApp {
    constructor() {
        this.init();
    }
    
    init() {
        // Only run these if we're on the homepage
        if (this.isHomePage()) {
            this.setupCategoryCards();
            this.setupAIAssistant();
        }
        
        this.setupMobileNavigation();
        this.setupSmoothScrolling();
        this.setupAnimations();
        this.setupBackToTop();
    }
    
    isHomePage() {
        return window.location.pathname.endsWith('index.html') || 
               window.location.pathname.endsWith('/') ||
               window.location.pathname === '';
    }
    
    setupMobileNavigation() {
        // Close mobile menu when clicking on links
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('nav-link')) {
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
    }
    
    setupCategoryCards() {
        // Only setup category cards on homepage
        document.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', () => {
                const category = card.getAttribute('data-category');
                window.location.href = `pages/buy.html?category=${category}`;
            });
        });
    }
    
    setupAIAssistant() {
        // Initialize AI Assistant only on homepage
        if (document.getElementById('ai-assistant')) {
            window.aiAssistant = new AIAssistant();
        }
    }
    
    setupSmoothScrolling() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    setupCategoryCards() {
        // Category card interactions
        document.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', () => {
                const category = card.getAttribute('data-category');
                window.location.href = `pages/buy.html?category=${category}`;
            });
            
            // Add hover effects
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.transition = 'transform 0.3s ease';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }
    
    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        document.addEventListener('DOMContentLoaded', () => {
            const animateElements = document.querySelectorAll('.feature-card, .category-card');
            animateElements.forEach(el => observer.observe(el));
        });
    }
    
    setupBackToTop() {
        // Create back to top button
        const backToTopButton = document.createElement('button');
        backToTopButton.innerHTML = '<i class="bi bi-chevron-up"></i>';
        backToTopButton.className = 'btn btn-primary btn-back-to-top';
        backToTopButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: none;
            align-items: center;
            justify-content: center;
        `;
        
        document.body.appendChild(backToTopButton);
        
        // Show/hide button based on scroll position
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        // Scroll to top when clicked
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Utility method to show notifications
    showNotification(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0 position-fixed top-0 end-0 m-3`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    // Form validation helper
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Price formatting helper
    formatPrice(price) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    }
    
    // Loading state helper
    setLoadingState(button, isLoading, loadingText = 'Loading...') {
        if (isLoading) {
            button.disabled = true;
            button.innerHTML = `<i class="bi bi-arrow-repeat spinner"></i> ${loadingText}`;
        } else {
            button.disabled = false;
            button.innerHTML = button.getAttribute('data-original-text') || 'Submit';
        }
    }
}

// Initialize main app
document.addEventListener('DOMContentLoaded', () => {
    window.electroFixApp = new ElectroFixApp();
});

// Utility functions for the whole application
const ElectroFixUtils = {
    // Debounce function for search inputs
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Local storage helpers
    storage: {
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.error('Error saving to localStorage:', e);
            }
        },
        
        get(key) {
            try {
                return JSON.parse(localStorage.getItem(key));
            } catch (e) {
                console.error('Error reading from localStorage:', e);
                return null;
            }
        },
        
        remove(key) {
            try {
                localStorage.removeItem(key);
            } catch (e) {
                console.error('Error removing from localStorage:', e);
            }
        }
    },
    
    // API simulation
    async simulateAPI(callback, delay = 1000) {
        return new Promise(resolve => {
            setTimeout(() => {
                const result = callback();
                resolve(result);
            }, delay);
        });
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ElectroFixApp, ElectroFixUtils };
}