// navigation.js - Consistent navigation across all pages
class NavigationManager {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    init() {
        this.injectNavigation();
        this.setActiveNavItem();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('buy.html')) return 'buy';
        if (path.includes('sell.html')) return 'sell';
        if (path.includes('repair.html')) return 'repair';
        if (path.includes('dashboard.html')) return 'dashboard';
        if (path.includes('login.html')) return 'login';
        if (path.includes('register.html')) return 'register';
        if (path.includes('forgot-password.html')) return 'forgot-password';
        if (path.includes('product-detail.html')) return 'product-detail';
        return 'home';
    }

    injectNavigation() {
        const navigationHTML = `
            <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
                <div class="container">
                    <a class="navbar-brand fw-bold text-primary" href="../index.html">
                        <i class="bi bi-tools me-2"></i>ElectroFix
                    </a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item">
                                <a class="nav-link ${this.currentPage === 'home' ? 'active' : ''}" href="../index.html">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link ${this.currentPage === 'buy' ? 'active' : ''}" href="buy.html">Buy</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link ${this.currentPage === 'sell' ? 'active' : ''}" href="sell.html">Sell</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link ${this.currentPage === 'repair' ? 'active' : ''}" href="repair.html">Repair</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link ${this.currentPage === 'dashboard' ? 'active' : ''}" href="dashboard.html">Dashboard</a>
                            </li>
                        </ul>
                        <div class="d-flex">
                            ${this.getAuthButtons()}
                        </div>
                    </div>
                </div>
            </nav>
        `;

        // Insert navigation at the beginning of body
        document.body.insertAdjacentHTML('afterbegin', navigationHTML);
        
        // Add padding to body to account for fixed navbar
        document.body.style.paddingTop = '76px';
    }

    getAuthButtons() {
        if (this.currentPage === 'login' || this.currentPage === 'register') {
            return '';
        }

        if (this.currentPage === 'dashboard') {
            return '<button class="btn btn-outline-danger" id="logout-btn">Logout</button>';
        }

        return `
            <a href="login.html" class="btn btn-outline-primary me-2">Login</a>
            <a href="register.html" class="btn btn-primary">Sign Up</a>
        `;
    }

    setActiveNavItem() {
        // Active state is set during injection
    }
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    new NavigationManager();
});