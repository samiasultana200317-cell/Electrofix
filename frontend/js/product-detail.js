class ProductDetailPage {
    constructor() {
        this.product = null;
        this.quantity = 1;
        this.init();
    }
    
    init() {
        this.loadProductData();
        this.setupEventListeners();
        this.setupImageGallery();
        this.loadRelatedProducts();
    }
    
    loadProductData() {
        // Mock product data
        this.product = {
            id: 1,
            title: "Apple iPhone 14 Pro",
            price: 899,
            originalPrice: 1099,
            condition: "excellent",
            specs: {
                storage: "256GB",
                color: "Deep Purple",
                batteryHealth: "96%",
                includes: "Original Charger, Box"
            },
            description: "This iPhone 14 Pro is in excellent condition with minimal signs of use.",
            features: [
                "Dynamic Island for alerts and activities",
                "Always-On display",
                "Pro camera system with 48MP Main camera"
            ],
            rating: 4.5,
            reviewCount: 128,
            inStock: true
        };
    }
    
    setupEventListeners() {
        // Quantity controls
        document.getElementById('increase-qty').addEventListener('click', () => {
            this.updateQuantity(this.quantity + 1);
        });
        
        document.getElementById('decrease-qty').addEventListener('click', () => {
            if (this.quantity > 1) {
                this.updateQuantity(this.quantity - 1);
            }
        });
        
        document.getElementById('quantity').addEventListener('change', (e) => {
            this.updateQuantity(parseInt(e.target.value) || 1);
        });
        
        // Add to cart
        document.getElementById('add-to-cart').addEventListener('click', () => {
            this.addToCart();
        });
        
        // Buy now
        document.getElementById('buy-now').addEventListener('click', () => {
            this.buyNow();
        });
    }
    
    setupImageGallery() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('thumbnail')) {
                const mainImage = document.getElementById('main-image');
                mainImage.src = e.target.getAttribute('data-image');
                
                document.querySelectorAll('.thumbnail').forEach(thumb => {
                    thumb.classList.remove('active');
                });
                e.target.classList.add('active');
            }
        });
    }
    
    updateQuantity(newQuantity) {
        this.quantity = Math.max(1, Math.min(5, newQuantity));
        document.getElementById('quantity').value = this.quantity;
    }
    
    addToCart() {
        if (!this.product.inStock) {
            this.showNotification('This product is currently out of stock.', 'warning');
            return;
        }
        
        const cartItem = {
            productId: this.product.id,
            title: this.product.title,
            price: this.product.price,
            quantity: this.quantity
        };
        
        this.showNotification('Product added to cart successfully!', 'success');
        console.log('Added to cart:', cartItem);
    }
    
    buyNow() {
        if (!this.product.inStock) {
            this.showNotification('This product is currently out of stock.', 'warning');
            return;
        }
        
        this.showNotification('Redirecting to checkout...', 'info');
        // In real app: window.location.href = `checkout.html?id=${this.product.id}&quantity=${this.quantity}`;
    }
    
    loadRelatedProducts() {
        const relatedProducts = [
            {
                id: 2,
                title: "iPhone 13 Pro",
                price: 699,
                originalPrice: 999,
                image: "../images/iphone-13-pro.jpg",
                condition: "excellent"
            },
            {
                id: 3,
                title: "Samsung Galaxy S23",
                price: 799,
                originalPrice: 899,
                image: "../images/galaxy-s23.jpg",
                condition: "good"
            }
        ];
        
        const container = document.getElementById('related-products');
        container.innerHTML = relatedProducts.map(product => `
            <div class="col-md-6 col-lg-3">
                <div class="card product-card h-100">
                    <img src="${product.image}" class="card-img-top" alt="${product.title}" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h6 class="card-title">${product.title}</h6>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="h6 text-primary mb-0">$${product.price}</span>
                            <span class="text-muted text-decoration-line-through small">$${product.originalPrice}</span>
                        </div>
                        <button class="btn btn-outline-primary btn-sm w-100 mt-2" onclick="window.location.href='product-detail.html?id=${product.id}'">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    showNotification(message, type) {
        // Create Bootstrap toast
        const toastContainer = document.createElement('div');
        toastContainer.innerHTML = `
            <div class="toast align-items-center text-bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        document.body.appendChild(toastContainer);
        const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
        toast.show();
        
        toastContainer.addEventListener('hidden.bs.toast', () => {
            toastContainer.remove();
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ProductDetailPage();
});