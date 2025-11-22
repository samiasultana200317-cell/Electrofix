class Dashboard {
    constructor() {
        this.userData = null;
        this.init();
    }
    
    init() {
        this.loadUserData();
        this.setupEventListeners();
        this.loadDashboardData();
    }
    
    async loadUserData() {
        // Try to fetch real profile from API if available
        try {
            if (window.apiService && typeof window.apiService.getProfile === 'function') {
                const resp = await window.apiService.getProfile();
                if (resp && resp.success && resp.user) {
                    this.userData = resp.user;
                } else {
                    this.userData = this.userData || {};
                }
            }
        } catch (err) {
            console.warn('Could not load profile from API, falling back to mock', err);
        }
        // Ensure we have an object to read safely from when populating UI
        this.userData = this.userData || {};

        // Populate UI fields if present
        try {
            const name = this.userData.name || '';
            const parts = name.split(' ');
            const first = parts.shift() || '';
            const last = parts.join(' ') || '';

            const welcome = document.getElementById('welcome-heading');
            if (welcome) welcome.textContent = `Welcome back, ${first}!`;

            const profileName = document.getElementById('profile-name');
            if (profileName) profileName.textContent = this.userData.name || '';

            const memberSince = document.getElementById('member-since');
            if (memberSince) memberSince.textContent = `Member since ${this.userData.joinDate || '—'}`;

            const firstInput = document.getElementById('first-name');
            const lastInput = document.getElementById('last-name');
            const emailInput = document.getElementById('email');
            const phoneInput = document.getElementById('phone');

            if (firstInput) firstInput.value = first;
            if (lastInput) lastInput.value = last;
            if (emailInput) emailInput.value = this.userData.email || '';
            if (phoneInput) phoneInput.value = this.userData.phone || '';
        } catch (err) {
            console.warn('Error populating profile fields', err);
        }
    }
    
    setupEventListeners() {
        // Logout button (may be injected later). Use event delegation to be robust.
        document.addEventListener('click', (e) => {
            const targetBtn = e.target && e.target.closest && e.target.closest('#logout-btn');
            if (targetBtn) {
                e.preventDefault();
                // Use global performLogout if available
                if (typeof performLogout === 'function') {
                    performLogout();
                } else {
                    this.logout();
                }
            }
        });

        // Settings form
        const settingsForm = document.getElementById('settings-form');
        if (settingsForm) {
            settingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveSettings();
            });
        }
    }
    
    loadDashboardData() {
        this.loadUserListings();
    }
    
    loadUserListings() {
        const listings = [
            {
                id: 1,
                title: "iPhone 14 Pro",
                price: 899,
                status: "active",
                image: "../images/iphone-14-pro.jpg",
                date: "2024-01-15"
            },
            {
                id: 2,
                title: "MacBook Pro 14\"",
                price: 1599,
                status: "sold",
                image: "../images/macbook-pro.jpg",
                date: "2024-01-10"
            }
        ];
        
        const container = document.getElementById('listings-grid');
        if (container) {
            container.innerHTML = listings.map(listing => `
                <div class="col-md-6 col-lg-4">
                    <div class="card h-100">
                        <img src="${listing.image}" class="card-img-top" alt="${listing.title}" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h6 class="card-title">${listing.title}</h6>
                            <p class="card-text text-primary fw-bold">$${listing.price}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge ${listing.status === 'active' ? 'bg-success' : 'bg-secondary'}">${listing.status}</span>
                                <small class="text-muted">${listing.date}</small>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="btn-group w-100">
                                <button class="btn btn-outline-primary btn-sm" onclick="dashboard.editListing(${listing.id})">Edit</button>
                                <button class="btn btn-outline-secondary btn-sm" onclick="dashboard.viewStats(${listing.id})">Stats</button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    }
    
    editListing(listingId) {
        this.showNotification('Editing listing #' + listingId, 'info');
    }
    
    viewStats(listingId) {
        this.showNotification('Viewing stats for listing #' + listingId, 'info');
    }
    
    saveSettings() {
        const submitBtn = document.querySelector('#settings-form button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Saving...';
        submitBtn.disabled = true;

        // Collect form values and call API
        (async () => {
            try {
                const first = document.getElementById('first-name')?.value || '';
                const last = document.getElementById('last-name')?.value || '';
                const email = document.getElementById('email')?.value || '';
                const phone = document.getElementById('phone')?.value || '';

                const name = [first, last].filter(Boolean).join(' ');

                if (window.apiService && typeof window.apiService.updateProfile === 'function') {
                    const payload = { name, phone };
                    const resp = await window.apiService.updateProfile(payload);
                    if (resp && resp.success && resp.user) {
                        this.userData = resp.user;
                        const profileName = document.getElementById('profile-name');
                        if (profileName) profileName.textContent = this.userData.name || '';
                        this.showNotification('Settings saved successfully!', 'success');
                    } else {
                        this.showNotification(resp.message || 'Failed to save settings', 'danger');
                    }
                } else {
                    // No API available: simulate
                    this.showNotification('Settings saved locally (offline)', 'info');
                }
            } catch (err) {
                console.error(err);
                this.showNotification('Error saving settings', 'danger');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        })();
    }
    
    logout() {
        // Fallback local logout if performLogout not defined
        if (confirm('Are you sure you want to logout?')) {
            if (window.apiService && typeof window.apiService.setToken === 'function') {
                window.apiService.setToken(null);
            }
            try { localStorage.removeItem('token'); } catch (_) {}
            this.showNotification('Logged out.', 'info');
            setTimeout(() => { window.location.href = 'login.html'; }, 300);
        }
    }
    
    showNotification(message, type) {
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
}

// Initialize after DOM is ready and expose globally for inline handlers
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});