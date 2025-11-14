const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
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
        return this.request('/bookings/user/');
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