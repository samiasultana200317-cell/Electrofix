// Prefer same-origin API if served through Django (port 8000). When serving
// the frontend from a static server (port 3000) we default to the backend
// running on `127.0.0.1:8000` so API calls reach the Django dev server.
const inferredBase = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
const API_BASE_URL = (window.location.port === '8000') ? `${inferredBase}/api` : `http://127.0.0.1:8000/api`;

class ApiService {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                // Only set JSON content-type when sending a plain object body
                ...(options.body && !(options.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
                ...(this.token && { 'Authorization': `Bearer ${this.token}` })
            },
            ...options
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Something went wrong');
            }

            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Auth methods
    async register(userData) {
        return this.request('/auth/register/', {
            method: 'POST',
            body: userData
        });
    }

    async login(credentials) {
        return this.request('/auth/login/', {
            method: 'POST',
            body: credentials
        });
    }

    async getProfile() {
        return this.request('/auth/profile/');
    }

    async updateProfile(profileData) {
        return this.request('/auth/profile/', {
            method: 'PUT',
            body: profileData
        });
    }

    // Services methods
    async getServices() {
        return this.request('/services/');
    }

    async getService(id) {
        return this.request(`/services/${id}/`);
    }

    // Bookings methods
    async createBooking(bookingData) {
        return this.request('/bookings/', {
            method: 'POST',
            body: bookingData
        });
    }

    async getUserBookings() {
        return this.request('/bookings/my-bookings/');
    }

    // Orders / Checkout
    async createOrder(orderData) {
        return this.request('/orders/', {
            method: 'POST',
            body: orderData
        });
    }

    async getUserOrders() {
        return this.request('/orders/my-orders/');
    }

    // Technicians
    async getTechnicians() {
        return this.request('/technicians/');
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    }
}

// Create global API instance
window.apiService = new ApiService();