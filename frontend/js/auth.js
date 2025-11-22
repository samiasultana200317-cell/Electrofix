class Auth {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupPasswordStrength();
    }
    
    setupEventListeners() {
        // Login form
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }
        
        // Register form
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });
        }
        
        // Forgot password form
        const forgotForm = document.getElementById('forgot-password-form');
        if (forgotForm) {
            forgotForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleForgotPassword();
            });
        }
        
        // Toggle password visibility
        document.querySelectorAll('.toggle-password').forEach(button => {
            button.addEventListener('click', (e) => {
                this.togglePasswordVisibility(e.target.closest('.toggle-password'));
            });
        });
    }
    
    togglePasswordVisibility(button) {
        const passwordInput = button.parentElement.querySelector('input');
        const icon = button.querySelector('i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.className = 'bi bi-eye-slash';
        } else {
            passwordInput.type = 'password';
            icon.className = 'bi bi-eye';
        }
    }
    
    setupPasswordStrength() {
        const passwordInput = document.getElementById('register-password');
        if (passwordInput) {
            passwordInput.addEventListener('input', () => {
                this.updatePasswordStrength();
            });
        }
    }
    
    updatePasswordStrength() {
        const password = document.getElementById('register-password')?.value;
        const strengthFill = document.querySelector('.strength-fill');
        const strengthText = document.querySelector('.strength-text');
        
        if (!strengthFill || !strengthText || !password) return;
        
        let strength = 0;
        
        if (password.length >= 8) strength += 25;
        if (/[a-z]/.test(password)) strength += 25;
        if (/[A-Z]/.test(password)) strength += 25;
        if (/[0-9]/.test(password) || /[^A-Za-z0-9]/.test(password)) strength += 25;
        
        strengthFill.style.width = `${strength}%`;
        
        if (strength < 50) {
            strengthFill.className = 'strength-fill strength-weak';
            strengthText.textContent = 'Weak';
        } else if (strength < 75) {
            strengthFill.className = 'strength-fill strength-medium';
            strengthText.textContent = 'Medium';
        } else {
            strengthFill.className = 'strength-fill strength-strong';
            strengthText.textContent = 'Strong';
        }
    }
    
    async handleLogin() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (!this.validateEmail(email)) {
            this.showNotification('Please enter a valid email address.', 'danger');
            return;
        }
        
        this.showLoading('Signing In...');
        try {
            const res = await window.apiService.login({ email, password });
            window.apiService.setToken(res.token);
            this.showNotification('Login successful! Redirecting...', 'success');
            setTimeout(() => window.location.href = 'dashboard.html', 1200);
        } catch (err) {
            this.showNotification(err.message || 'Invalid email or password.', 'danger');
        }
    }
    
    async handleRegister() {
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const firstName = document.getElementById('first-name')?.value || '';
        const lastName = document.getElementById('last-name')?.value || '';
        const phone = document.getElementById('phone')?.value || '';
        
        if (!this.validateEmail(email)) {
            this.showNotification('Please enter a valid email address.', 'danger');
            return;
        }
        if (password !== confirmPassword) {
            this.showNotification('Passwords do not match.', 'danger');
            return;
        }
        
        this.showLoading('Creating Account...');
        try {
            const res = await window.apiService.register({
                name: `${firstName} ${lastName}`.trim() || email.split('@')[0],
                email,
                password,
                phone
            });
            window.apiService.setToken(res.token);
            this.showNotification('Account created successfully!', 'success');
            setTimeout(() => window.location.href = 'dashboard.html', 1200);
        } catch (err) {
            this.showNotification(err.message || 'Registration failed.', 'danger');
        }
    }
    
    handleForgotPassword() {
        const email = document.getElementById('reset-email').value;
        
        if (!this.validateEmail(email)) {
            this.showNotification('Please enter a valid email address.', 'danger');
            return;
        }
        this.showLoading('Sending Reset Link...');

        (async () => {
            try {
                const res = await window.apiService.request('/auth/forgot-password/', {
                    method: 'POST',
                    body: { email }
                });
                // In dev the API returns a token for testing. Don't expose in production.
                console.info('Reset token (dev):', res.token || '---');
                this.showNotification(res.message || 'If an account with that email exists, a reset link has been sent.', 'success');
                // If a dev token is returned, redirect user to the reset page with token in querystring for testing.
                if (res && res.token) {
                    const url = `pages/reset-password.html?token=${encodeURIComponent(res.token)}`;
                    setTimeout(() => window.location.href = url, 1200);
                } else {
                    setTimeout(() => window.location.href = 'login.html', 2500);
                }
            } catch (err) {
                console.error(err);
                this.showNotification(err.message || 'Failed to send reset link.', 'danger');
            }
        })();
    }
    
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    showLoading(message) {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = `<i class="bi bi-arrow-repeat spinner"></i> ${message}`;
            submitBtn.disabled = true;
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
        
        // Reset button
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.getAttribute('data-original-text') || 'Submit';
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
}

// Store original button text
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.setAttribute('data-original-text', submitBtn.innerHTML);
    }
    
    new Auth();
});