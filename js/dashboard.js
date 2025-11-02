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
    
    loadUserData() {
        // Mock user data
        this.userData = {
            name: "John Doe",
            email: "john.doe@example.com",
            joinDate: "January 2024",
            stats: {
                listings: 12,
                purchases: 8,
                rating: 4.8
            }
        };
    }
    
    setupEventListeners() {
        // Logout button
        document.getElementById('logout-btn').addEventListener('click', (e) => {
            e.preventDefault();
            this.logout();
        });
        
        // Settings form
        document.getElementById('settings-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveSettings();
        });
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
        
        setTimeout(() => {
            this.showNotification('Settings saved successfully!', 'success');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 1500);
    }
    
    logout() {
        if (confirm('Are you sure you want to logout?')) {
            this.showNotification('Logging out...', 'info');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1000);
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

const dashboard = new Dashboard();