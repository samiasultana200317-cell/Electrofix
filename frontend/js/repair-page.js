class RepairPage {
    constructor() {
        this.repairData = {
            deviceType: '',
            brand: '',
            model: '',
            issues: [],
            description: '',
            contactInfo: {}
        };
        
        this.init();
    }
    
    init() {
        this.setupServiceSelection();
        this.setupRepairForm();
    }
    
    setupServiceSelection() {
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const deviceType = card.getAttribute('data-device');
                this.selectDeviceType(deviceType);
            });
        });
    }
    
    selectDeviceType(deviceType) {
        // Update active service card
        document.querySelectorAll('.service-card').forEach(card => {
            card.classList.remove('border-primary');
        });
        document.querySelector(`[data-device="${deviceType}"]`).classList.add('border-primary');
        
        // Update form and show it
        document.getElementById('repair-device-type').value = deviceType;
        this.updateBrandOptions(deviceType);
        
        const form = document.getElementById('repair-form');
        form.style.display = 'block';
        form.scrollIntoView({ behavior: 'smooth' });
        
        this.updateCostEstimation();
    }
    
    updateBrandOptions(deviceType) {
        const brandSelect = document.getElementById('repair-brand');
        brandSelect.innerHTML = '<option value="">Select Brand</option>';
        
        const brands = this.getBrandsByType(deviceType);
        brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand.value;
            option.textContent = brand.label;
            brandSelect.appendChild(option);
        });
    }
    
    getBrandsByType(deviceType) {
        const brands = {
            phone: [
                { value: 'apple', label: 'Apple' },
                { value: 'samsung', label: 'Samsung' },
                { value: 'google', label: 'Google' },
                { value: 'oneplus', label: 'OnePlus' },
                { value: 'xiaomi', label: 'Xiaomi' },
                { value: 'other', label: 'Other' }
            ],
            laptop: [
                { value: 'apple', label: 'Apple' },
                { value: 'dell', label: 'Dell' },
                { value: 'hp', label: 'HP' },
                { value: 'lenovo', label: 'Lenovo' },
                { value: 'asus', label: 'ASUS' },
                { value: 'other', label: 'Other' }
            ],
            tablet: [
                { value: 'apple', label: 'Apple' },
                { value: 'samsung', label: 'Samsung' },
                { value: 'amazon', label: 'Amazon' },
                { value: 'microsoft', label: 'Microsoft' },
                { value: 'other', label: 'Other' }
            ]
        };
        
        return brands[deviceType] || [];
    }
    
    setupRepairForm() {
        console.debug('[RepairPage] setupRepairForm: attaching listeners');
        // Form element changes
        document.getElementById('repair-device-type').addEventListener('change', (e) => {
            this.updateBrandOptions(e.target.value);
            this.updateCostEstimation();
        });
        
        document.getElementById('repair-brand').addEventListener('change', () => {
            this.updateCostEstimation();
        });
        
        document.getElementById('repair-model').addEventListener('input', () => {
            this.updateCostEstimation();
        });
        
        // Issues checkboxes
        document.querySelectorAll('input[name="issues"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateSelectedIssues();
                this.updateCostEstimation();
            });
        });
        
        // Form submission
        const formEl = document.querySelector('.repair-form');
        if (formEl) {
            formEl.addEventListener('submit', (e) => {
                e.preventDefault();
                console.debug('[RepairPage] form submit event');
                this.submitRepairRequest();
            });
            // Show visual indicator that handlers are attached
            try {
                const status = document.getElementById('handler-status');
                if (status) {
                    status.classList.remove('d-none');
                    status.setAttribute('title', 'JavaScript handlers attached');
                }
            } catch (err) {
                console.warn('[RepairPage] failed to show handler-status badge', err);
            }
        } else {
            console.warn('[RepairPage] .repair-form not found when attaching submit handler');
        }

        // Load technicians into repair page select (if present)
        const techSelect = document.getElementById('preferred-technician');
        if (techSelect && window.apiService) {
            try {
                window.apiService.getTechnicians().then(r => {
                    const list = r.data || [];
                    list.forEach(t => {
                        const opt = document.createElement('option');
                        opt.value = t.id;
                        opt.textContent = t.name || t.full_name || t.email || ('Tech ' + t.id);
                        techSelect.appendChild(opt);
                    });
                }).catch(e => {
                    console.warn('Could not load technicians', e);
                });
            } catch (e) {
                console.warn('Technician load failed', e);
            }
        }
    }
    
    updateSelectedIssues() {
        const selectedIssues = Array.from(document.querySelectorAll('input[name="issues"]:checked'))
            .map(cb => cb.value);
        this.repairData.issues = selectedIssues;
    }
    
    updateCostEstimation() {
        const deviceType = document.getElementById('repair-device-type').value;
        const brand = document.getElementById('repair-brand').value;
        const issues = Array.from(document.querySelectorAll('input[name="issues"]:checked'))
            .map(cb => cb.value);
        
        if (!deviceType) return;
        
        const estimatedCost = this.calculateRepairCost(deviceType, brand, issues);
        this.displayCostEstimation(estimatedCost);
    }
    
    calculateRepairCost(deviceType, brand, issues) {
        const baseCosts = { phone: 50, laptop: 80, tablet: 60 };
        let baseCost = baseCosts[deviceType] || 50;
        
        if (brand === 'apple') baseCost *= 1.3;
        
        const issueCosts = {
            screen: 80, battery: 40, charging: 30, 
            water: 100, software: 25, performance: 35
        };
        
        let additionalCost = issues.reduce((total, issue) => {
            return total + (issueCosts[issue] || 0);
        }, 0);
        
        const minCost = Math.round(baseCost + additionalCost * 0.8);
        const maxCost = Math.round(baseCost + additionalCost * 1.2);
        
        return { min: minCost, max: maxCost };
    }
    
    displayCostEstimation(cost) {
        const priceElement = document.querySelector('.text-primary.h3');
        if (priceElement && cost.min && cost.max) {
            priceElement.textContent = `$${cost.min} - $${cost.max}`;
        }
    }
    
    submitRepairRequest() {
        console.debug('[RepairPage] submitRepairRequest called');
        if (!this.validateForm()) return;
        
        this.collectFormData();
        
        const submitBtn = document.querySelector('.repair-form button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Submitting...';
        submitBtn.disabled = true;
        
        // Send booking to backend API
        (async () => {
            try {
                if (!window.apiService || !window.apiService.createBooking) {
                    throw new Error('API client unavailable. Ensure you are running the backend.');
                }

                // Ensure user is logged in
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('You must be logged in to submit a repair request.');
                }

                // Try to find a matching service for the selected device type
                let serviceId = null;
                try {
                    const svcResp = await window.apiService.getServices();
                    const services = svcResp && svcResp.data ? svcResp.data : [];
                    const device = this.repairData.deviceType;
                    // match by category or name containing device type
                    const match = services.find(s => (s.category && s.category.toLowerCase() === device) || (s.name && s.name.toLowerCase().includes(device)));
                    if (match) serviceId = match.id;
                } catch (e) {
                    console.warn('Could not fetch services to auto-match:', e);
                }

                // Build booking payload expected by backend
                const bookingPayload = {
                    appliance_type: this.repairData.deviceType,
                    brand: this.repairData.brand,
                    model: this.repairData.model,
                    problem_description: this.repairData.description || this.repairData.issues.join(', '),
                    // scheduled_date: use selected value or ISO now as fallback
                    scheduled_date: this.repairData.scheduled_date || new Date().toISOString(),
                    time_slot: this.repairData.time_slot || 'Any',
                    address: this.repairData.contactInfo.address || this.repairData.contactInfo.location || ''
                };

                // include service id only when we found a matching service
                if (serviceId) {
                    bookingPayload.service = serviceId;
                }

                // include preferred technician if selected on repair page
                const preferredTechEl = document.getElementById('preferred-technician');
                if (preferredTechEl && preferredTechEl.value) {
                    bookingPayload.preferred_technician = preferredTechEl.value;
                }

                const resp = await window.apiService.createBooking(bookingPayload);
                if (resp && resp.success) {
                    this.showSuccessMessage();
                } else {
                    throw new Error((resp && resp.message) || 'Booking failed');
                }
            } catch (err) {
                console.error('Booking error:', err);
                this.showNotification(err.message || 'Failed to submit repair request', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        })();
    }
    
    validateForm() {
        const required = ['repair-device-type', 'repair-brand', 'repair-model', 'customer-name', 'customer-email', 'customer-phone'];
        for (let field of required) {
            if (!document.getElementById(field).value) {
                this.showNotification('Please fill in all required fields.', 'error');
                return false;
            }
        }
        return true;
    }
    
    collectFormData() {
        this.repairData = {
            deviceType: document.getElementById('repair-device-type').value,
            brand: document.getElementById('repair-brand').value,
            model: document.getElementById('repair-model').value,
            issues: Array.from(document.querySelectorAll('input[name="issues"]:checked')).map(cb => cb.value),
            description: document.getElementById('issue-description').value,
            contactInfo: {
                name: document.getElementById('customer-name').value,
                email: document.getElementById('customer-email').value,
                phone: document.getElementById('customer-phone').value,
                location: document.getElementById('service-location').value,
                address: document.getElementById('service-address') ? document.getElementById('service-address').value : ''
            }
        };
        // Scheduled date/time
        const sched = document.getElementById('scheduled-date');
        this.repairData.scheduled_date = sched && sched.value ? (new Date(sched.value)).toISOString() : new Date().toISOString();
        this.repairData.time_slot = document.getElementById('time-slot') ? document.getElementById('time-slot').value : 'Any';
    }
    
    showSuccessMessage() {
        const form = document.querySelector('.repair-form');
        form.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-check-circle-fill text-success display-1 mb-3"></i>
                <h3 class="text-success mb-3">Repair Request Submitted!</h3>
                <p class="text-muted mb-4">We've received your repair request. Our team will contact you within 24 hours.</p>
                <div class="d-grid gap-2 d-md-block">
                    <a href="dashboard.html" class="btn btn-primary me-md-2">View Dashboard</a>
                    <a href="repair.html" class="btn btn-outline-primary">New Repair Request</a>
                </div>
            </div>
        `;
    }
    
    showNotification(message, type) {
        // Create and show Bootstrap toast notification
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type === 'error' ? 'danger' : 'success'} border-0`;
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

// Initialize RepairPage reliably whether DOMContentLoaded already fired or not
function initRepairPage() {
    try {
        window.repairPage = new RepairPage();
        console.debug('[RepairPage] initialized');
    } catch (e) {
        console.error('[RepairPage] init error', e);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRepairPage);
} else {
    initRepairPage();
}