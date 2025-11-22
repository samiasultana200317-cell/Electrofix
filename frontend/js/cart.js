document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('cart-container');
    // technician select removed from cart page; preferred technician is selected on repair page
    function render() {
        const raw = localStorage.getItem('cart');
        const cart = raw ? JSON.parse(raw) : [];
        if (!cart.length) {
            container.innerHTML = '<div class="alert alert-secondary">Your cart is empty.</div>';
            return;
        }

        const rows = cart.map(item => `
            <div class="card mb-3">
                <div class="card-body d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${item.title}</h6>
                        <div class="small text-muted">Price: $${item.price} &times; ${item.quantity}</div>
                    </div>
                    <div>
                        <span class="h5 text-primary">$${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `).join('');

        const total = cart.reduce((s, it) => s + (it.price * it.quantity), 0);
        container.innerHTML = rows + `
            <div class="mt-3 text-end">
                <h4>Total: $${total.toFixed(2)}</h4>
            </div>
        `;
    }

    document.getElementById('checkout-btn').addEventListener('click', () => {
        const raw = localStorage.getItem('cart');
        const cart = raw ? JSON.parse(raw) : [];
        if (!cart.length) {
            alert('Cart is empty');
            return;
        }

        // If user is logged in and API is available, call backend order endpoint
        if (window.apiService && window.apiService.token) {
            const payload = { items: cart };
            // call API
            window.apiService.createOrder(payload).then(res => {
                try {
                    localStorage.removeItem('cart');
                    if (window.updateCartCount) window.updateCartCount();
                } catch (_) {}
                alert('Checkout successful. Order id: ' + (res.data && res.data.id ? res.data.id : 'unknown'));
                render();
            }).catch(err => {
                console.error('Order API failed', err);
                alert('Checkout failed via API. See console for details.');
            });
            return;
        }

        // Fallback: simulated checkout
        try {
            localStorage.removeItem('cart');
            if (window.updateCartCount) window.updateCartCount();
            alert('Checkout successful (simulated). Thank you!');
            render();
        } catch (e) {
            console.error(e);
            alert('Checkout failed');
        }
    });

    document.getElementById('clear-cart').addEventListener('click', () => {
        if (!confirm('Clear cart?')) return;
        localStorage.removeItem('cart');
        if (window.updateCartCount) window.updateCartCount();
        render();
    });

    render();
    // No technician select on cart page anymore
});
