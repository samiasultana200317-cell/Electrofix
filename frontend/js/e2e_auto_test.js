// Simple E2E test runner for dashboard (trigger manually by clicking the Run E2E button)
(async function(){
    window.runE2ETest = async function() {
        if (!window.apiService) {
            console.error('apiService not available');
            return;
        }

        try {
            console.info('E2E: starting login');
            // Use test credentials used by the backend test script
            const loginResp = await window.apiService.login({ email: 'testuser+ai@example.com', password: 'TestPass123!' });
            console.info('E2E: loginResp', loginResp);
            if (loginResp && loginResp.token) {
                window.apiService.setToken(loginResp.token);
            } else {
                console.warn('E2E: no token from login');
            }

            // Update profile
            const newName = 'E2E User ' + Math.floor(Math.random()*1000);
            const newPhone = '+1555' + Math.floor(Math.random()*9000 + 1000);
            console.info('E2E: updating profile', { name: newName, phone: newPhone });
            const upd = await window.apiService.updateProfile({ name: newName, phone: newPhone });
            console.info('E2E: updateResp', upd);

            // Fetch fresh profile
            const fresh = await window.apiService.getProfile();
            console.info('E2E: fresh profile', fresh);

            // Update UI if present
            if (fresh && fresh.success && fresh.user) {
                const profileName = document.getElementById('profile-name');
                if (profileName) profileName.textContent = fresh.user.name || '';
                const welcome = document.getElementById('welcome-heading');
                if (welcome) {
                    const first = (fresh.user.name || '').split(' ')[0] || '';
                    welcome.textContent = `Welcome back, ${first}!`;
                }
                // show toast
                if (window.dashboard && typeof window.dashboard.showNotification === 'function') {
                    window.dashboard.showNotification('E2E: Profile updated and UI refreshed', 'success');
                } else {
                    alert('E2E: Profile updated — refresh the page to see changes');
                }
            } else {
                console.error('E2E: failed to read profile after update', fresh);
                alert('E2E failed — see console for details');
            }

        } catch (err) {
            console.error('E2E error', err);
            alert('E2E script error — see console');
        }
    };
})();
