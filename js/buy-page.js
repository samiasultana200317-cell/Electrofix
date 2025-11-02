class BuyPage {
    constructor() {
        this.products = [];
        this.filteredProducts = [];
        this.currentPage = 1;
        this.productsPerPage = 9;
        
        this.init();
    }
    
    init() {
        this.loadProducts();
        this.setupEventListeners();
    }
    
    loadProducts() {
        // Mock data
        this.products = [
            {
                id: 1,
                title: "iPhone 14 Pro",
                category: "phone",
                brand: "apple",
                price: 899,
                originalPrice: 1099,
                condition: "excellent",
                specs: "256GB, Deep Purple, 96% Battery",
                image: "../images/iphone-14-pro.jpg",
                rating: 4.5,
                reviews: 128
            },
            {
                id: 2,
                title: "Samsung Galaxy S23",
                category: "phone",
                brand: "samsung",
                price: 699,
                originalPrice: 799,
                condition: "good",
                specs: "128GB, Phantom Black, 88% Battery",
                image: "../images/galaxy-s23.jpg",
                rating: 4.3,
                reviews: 89
            },
            {
                id: 3,
                title: "MacBook Pro 14\"",
                category: "laptop",
                brand: "apple",
                price: 1599,
                originalPrice: 1999,
                condition: "excellent",
                specs: "M2 Pro, 16GB RAM, 512GB SSD",
                image: "../images/macbook-pro.jpg",
                rating: 4.7,
                reviews: 67
            },
            {
                id: 4,
                title: "Dell XPS 13",
                category: "laptop",
                brand: "dell",
                price: 899,
                originalPrice: 1199,
                condition: "good",
                specs: "i7, 16GB RAM, 512GB SSD",
                image: "../images/dell-xps.jpg",
                rating: 4.4,
                reviews: 45
            },
            {
                id: 5,
                title: "iPad Pro 12.9\"",
                category: "tablet",
                brand: "apple",
                price: 799,
                originalPrice: 1099,
                condition: "excellent",
                specs: "M1, 128GB, Wi-Fi + Cellular",
                image: "../images/ipad-pro.jpg",
                rating: 4.6,
                reviews: 92
            },
            {
                id: 6,
                title: "Samsung Galaxy Tab S8",
                category: "tablet",
                brand: "samsung",
                price: 549,
                originalPrice: 699,
                condition: "good",
                specs: "128GB, S-Pen Included",
                image: "../images/galaxy-tab.jpg",
                rating: 4.2,
                reviews: 34
            }
        ];
        
        this.filteredProducts = [...this.products];
        this.renderProducts();
        this.updateProductCount();
    }
    
    setupEventListeners() {
        // Search functionality
        document.getElementById('search-btn').addEventListener('click', () => this.handleSearch());
        document.getElementById('search-input').addEventListener('input', () => this.handleSearch());
        
        // Filter functionality
        document.getElementById('category-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('brand-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('price-slider').addEventListener('input', () => this.updatePriceRange());
        document.getElementById('condition-filter').addEventListener('change', () => this.applyFilters());
        
        // Sort functionality
        document.getElementById('sort-by').addEventListener('change', () => this.applySorting());
        
        // Load more
        document.getElementById('load-more-btn').addEventListener('click', () => this.loadMore());
    }
    
    handleSearch() {
        this.applyFilters();
    }
    
    applyFilters() {
        const category = document.getElementById('category-filter').value;
        const brand = document.getElementById('brand-filter').value;
        const condition = document.getElementById('condition-filter').value;
        const maxPrice = document.getElementById('price-slider').value;
        const searchTerm = document.getElementById('search-input').value.toLowerCase();
        
        this.filteredProducts = this.products.filter(product => {
            const matchesCategory = category === 'all' || product.category === category;
            const matchesBrand = brand === 'all' || product.brand === brand;
            const matchesCondition = condition === 'all' || product.condition === condition;
            const matchesPrice = product.price <= maxPrice;
            const matchesSearch = searchTerm === '' || 
                product.title.toLowerCase().includes(searchTerm) ||
                product.specs.toLowerCase().includes(searchTerm) ||
                product.brand.toLowerCase().includes(searchTerm);
            
            return matchesCategory && matchesBrand && matchesCondition && matchesPrice && matchesSearch;
        });
        
        this.applySorting();
        this.renderProducts();
        this.updateProductCount();
    }
    
    updatePriceRange() {
        const slider = document.getElementById('price-slider');
        const valueDisplay = document.getElementById('price-value');
        valueDisplay.textContent = `$${slider.value}`;
        this.applyFilters();
    }
    
    applySorting() {
        const sortBy = document.getElementById('sort-by').value;
        
        this.filteredProducts.sort((a, b) => {
            switch(sortBy) {
                case 'price-low':
                    return a.price - b.price;
                case 'price-high':
                    return b.price - a.price;
                case 'newest':
                    return b.id - a.id;
                default:
                    return b.rating - a.rating; // Featured
            }
        });
        
        this.renderProducts();
    }
    
    renderProducts() {
        const grid = document.getElementById('products-grid');
        const startIndex = 0;
        const endIndex = this.currentPage * this.productsPerPage;
        const productsToShow = this.filteredProducts.slice(0, endIndex);
        
        grid.innerHTML = productsToShow.map(product => this.createProductCard(product)).join('');
        
        // Show/hide load more button
        const loadMoreBtn = document.getElementById('load-more-btn');
        loadMoreBtn.style.display = endIndex >= this.filteredProducts.length ? 'none' : 'block';
    }
    
    createProductCard(product) {
        const discount = product.originalPrice ? 
            Math.round((1 - product.price / product.originalPrice) * 100) : 0;
        
        return `
            <div class="col-md-6 col-lg-4">
                <div class="card product-card h-100 shadow-sm">
                    <div class="position-relative">
                        <img src="${product.image}" class="card-img-top" alt="${product.title}" style="height: 200px; object-fit: cover;">
                        ${discount > 0 ? `
                            <span class="position-absolute top-0 start-0 m-2 badge bg-warning text-dark">
                                ${discount}% OFF
                            </span>
                        ` : ''}
                        <span class="position-absolute top-0 end-0 m-2 badge ${this.getConditionBadgeClass(product.condition)}">
                            ${product.condition.charAt(0).toUpperCase() + product.condition.slice(1)}
                        </span>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${product.title}</h5>
                        <p class="card-text text-muted small">${product.specs}</p>
                        
                        <div class="d-flex align-items-center mb-2">
                            <div class="text-warning me-2">
                                ${this.generateStarRating(product.rating)}
                            </div>
                            <small class="text-muted">(${product.reviews})</small>
                        </div>
                        
                        <div class="mt-auto">
                            <div class="d-flex align-items-center mb-3">
                                <span class="h4 text-primary mb-0">$${product.price}</span>
                                ${product.originalPrice ? `
                                    <span class="text-muted text-decoration-line-through ms-2">$${product.originalPrice}</span>
                                ` : ''}
                            </div>
                            <div class="d-grid gap-2">
                                <a href="product-detail.html?id=${product.id}" class="btn btn-primary">
                                    <i class="bi bi-eye me-2"></i>View Details
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    getConditionBadgeClass(condition) {
        const classes = {
            'excellent': 'bg-success',
            'good': 'bg-warning text-dark',
            'fair': 'bg-secondary'
        };
        return classes[condition] || 'bg-secondary';
    }
    
    generateStarRating(rating) {
        let stars = '';
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="bi bi-star-fill"></i>';
        }
        
        if (hasHalfStar) {
            stars += '<i class="bi bi-star-half"></i>';
        }
        
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="bi bi-star"></i>';
        }
        
        return stars;
    }
    
    updateProductCount() {
        const countElement = document.getElementById('product-count');
        countElement.textContent = `${this.filteredProducts.length} devices found`;
    }
    
    loadMore() {
        this.currentPage++;
        this.renderProducts();
    }
}

// Initialize buy page
document.addEventListener('DOMContentLoaded', () => {
    new BuyPage();
});