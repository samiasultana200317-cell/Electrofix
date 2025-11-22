document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('reset-form');
    const tokenInput = document.getElementById('reset-token');
    const newPassword = document.getElementById('new-password');
    const confirmPassword = document.getElementById('confirm-password');

    // read token from query string ?token=...
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token') || '';
    if (token) tokenInput.value = token;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const p = newPassword.value || '';
        const c = confirmPassword.value || '';
        if (p.length < 8) {
            alert('Password must be at least 8 characters');
            return;
        }
        if (p !== c) {
            alert('Passwords do not match');
            return;
        }

        const payload = { token: tokenInput.value, password: p };
        try {
            if (!window.apiService) throw new Error('API client unavailable');
            const res = await window.apiService.request('/auth/reset-password/', { method: 'POST', body: payload });
            if (res && res.success) {
                alert(res.message || 'Password reset successful');
                window.location.href = 'login.html';
            } else {
                alert((res && res.message) || 'Failed to reset password');
            }
        } catch (err) {
            console.error(err);
            alert(err.message || 'Error sending reset request');
        }
    });
});
