class SellPage {
    constructor() {
        this.currentStep = 1;
        this.formData = {
            deviceInfo: {},
            condition: {},
            photos: [],
            description: '',
            price: 0
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupConditionAssessment();
        this.setupPhotoUpload();
        this.setupPriceEstimation();
    }
    
    setupEventListeners() {
        // Next step buttons
        document.querySelectorAll('.next-step').forEach(button => {
            button.addEventListener('click', (e) => {
                const nextStep = e.target.getAttribute('data-next');
                this.goToStep(nextStep);
            });
        });
        
        // Previous step buttons
        document.querySelectorAll('.prev-step').forEach(button => {
            button.addEventListener('click', (e) => {
                const prevStep = e.target.getAttribute('data-prev');
                this.goToStep(prevStep);
            });
        });
        
        // Form submission
        document.getElementById('submit-listing').addEventListener('click', (e) => {
            e.preventDefault();
            this.submitListing();
        });
        
        // Real-time form validation
        this.setupFormValidation();
    }
    
    setupFormValidation() {
        // Device type change
        document.getElementById('device-type').addEventListener('change', (e) => {
            this.updateBrandOptions(e.target.value);
            this.saveDeviceInfo();
        });
        
        // All device info fields
        ['device-type', 'device-brand', 'device-model', 'purchase-year'].forEach(fieldId => {
            document.getElementById(fieldId).addEventListener('change', () => this.saveDeviceInfo());
        });
    }
    
    updateBrandOptions(deviceType) {
        const brandSelect = document.getElementById('device-brand');
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
    
    setupConditionAssessment() {
        // Battery health slider
        const batterySlider = document.getElementById('battery-health');
        const batteryValue = document.getElementById('battery-value');
        
        batterySlider.addEventListener('input', (e) => {
            batteryValue.textContent = `${e.target.value}%`;
            this.saveConditionInfo();
        });
        
        // Condition radio buttons
        document.querySelectorAll('input[name="condition"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.saveConditionInfo();
                // Update visual state
                document.querySelectorAll('.condition-option').forEach(option => {
                    option.classList.remove('border-primary', 'bg-light');
                });
                const selectedOption = document.querySelector('input[name="condition"]:checked');
                if (selectedOption) {
                    selectedOption.closest('.condition-option').classList.add('border-primary', 'bg-light');
                }
            });
        });
        
        // Accessories checkboxes
        document.querySelectorAll('input[name="accessories"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => this.saveConditionInfo());
        });
        
        // Screen condition
        document.getElementById('screen-condition').addEventListener('change', () => this.saveConditionInfo());
    }
    
    setupPhotoUpload() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('photo-upload');
        const preview = document.getElementById('upload-preview');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-primary', 'bg-light');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('border-primary', 'bg-light');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-primary', 'bg-light');
            
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });
        
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }
    
    handleFiles(files) {
        const preview = document.getElementById('upload-preview');
        
        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-4 col-md-3';
                colDiv.innerHTML = `
                    <div class="position-relative">
                        <img src="${e.target.result}" class="img-thumbnail w-100" style="height: 100px; object-fit: cover;">
                        <button type="button" class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1 remove-image">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                `;
                
                colDiv.querySelector('.remove-image').addEventListener('click', () => {
                    colDiv.remove();
                    this.updatePhotos();
                });
                
                preview.appendChild(colDiv);
                this.formData.photos.push({
                    file: file,
                    preview: e.target.result
                });
            };
            reader.readAsDataURL(file);
        });
    }
    
    updatePhotos() {
        const previewItems = document.querySelectorAll('#upload-preview .col-4');
        this.formData.photos = Array.from(previewItems).map(item => {
            return {
                preview: item.querySelector('img').src
            };
        });
    }
    
    setupPriceEstimation() {
        const priceInput = document.getElementById('asking-price');
        priceInput.addEventListener('input', (e) => {
            this.formData.price = parseFloat(e.target.value) || 0;
            this.updateAISuggestion();
        });
        
        // Update AI suggestion when device info changes
        document.getElementById('device-type').addEventListener('change', () => this.updateAISuggestion());
        document.getElementById('device-brand').addEventListener('change', () => this.updateAISuggestion());
        document.getElementById('device-model').addEventListener('input', () => this.updateAISuggestion());
    }
    
    updateAISuggestion() {
        const suggestionElement = document.getElementById('ai-suggestion');
        
        const basePrice = this.calculateBasePrice();
        if (basePrice) {
            const minPrice = Math.round(basePrice * 0.8);
            const maxPrice = Math.round(basePrice * 1.2);
            suggestionElement.innerHTML = `
                <i class="bi bi-robot me-2"></i>
                Our AI suggests: <strong>$${minPrice} - $${maxPrice}</strong> based on similar devices
            `;
            suggestionElement.style.display = 'block';
        } else {
            suggestionElement.style.display = 'none';
        }
    }
    
    calculateBasePrice() {
        const deviceType = document.getElementById('device-type').value;
        const brand = document.getElementById('device-brand').value;
        const model = document.getElementById('device-model').value;
        
        if (!deviceType || !brand || !model) return null;
        
        const basePrices = {
            phone: {
                apple: 800,
                samsung: 600,
                google: 500,
                oneplus: 450,
                xiaomi: 300,
                other: 350
            },
            laptop: {
                apple: 1200,
                dell: 800,
                hp: 700,
                lenovo: 750,
                asus: 650,
                other: 600
            },
            tablet: {
                apple: 600,
                samsung: 400,
                amazon: 200,
                microsoft: 500,
                other: 300
            }
        };
        
        return basePrices[deviceType]?.[brand] || 500;
    }
    
    saveDeviceInfo() {
        this.formData.deviceInfo = {
            type: document.getElementById('device-type').value,
            brand: document.getElementById('device-brand').value,
            model: document.getElementById('device-model').value,
            purchaseYear: document.getElementById('purchase-year').value
        };
    }
    
    saveConditionInfo() {
        const condition = document.querySelector('input[name="condition"]:checked');
        
        this.formData.condition = {
            overall: condition ? condition.value : '',
            screen: document.getElementById('screen-condition').value,
            battery: document.getElementById('battery-health').value,
            accessories: Array.from(document.querySelectorAll('input[name="accessories"]:checked'))
                .map(cb => cb.value)
        };
    }
    
    goToStep(stepNumber) {
        if (!this.validateStep(this.currentStep)) {
            return;
        }
        
        // Hide current step
        document.getElementById(`step-${this.currentStep}`).classList.add('d-none');
        document.getElementById(`step-${this.currentStep}-indicator`).classList.remove('active', 'completed');
        
        // Show new step
        document.getElementById(stepNumber).classList.remove('d-none');
        document.getElementById(`${stepNumber}-indicator`).classList.add('active');
        
        // Mark previous step as completed
        document.getElementById(`step-${this.currentStep}-indicator`).classList.add('completed');
        
        // Update current step
        this.currentStep = parseInt(stepNumber.split('-')[1]);
        
        // Scroll to top of form
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    validateStep(step) {
        switch(step) {
            case 1:
                return this.validateDeviceInfo();
            case 2:
                return this.validateConditionInfo();
            case 3:
                return this.validatePhotos();
            default:
                return true;
        }
    }
    
    validateDeviceInfo() {
        const type = document.getElementById('device-type').value;
        const brand = document.getElementById('device-brand').value;
        const model = document.getElementById('device-model').value;
        
        if (!type || !brand || !model) {
            this.showNotification('Please fill in all required device information.', 'danger');
            return false;
        }
        return true;
    }
    
    validateConditionInfo() {
        const condition = document.querySelector('input[name="condition"]:checked');
        if (!condition) {
            this.showNotification('Please select the overall condition of your device.', 'danger');
            return false;
        }
        return true;
    }
    
    validatePhotos() {
        if (this.formData.photos.length === 0) {
            this.showNotification('Please upload at least one photo of your device.', 'danger');
            return false;
        }
        return true;
    }
    
    submitListing() {
        if (!this.validateStep(3)) return;
        
        // Save final form data
        this.formData.description = document.getElementById('device-description').value;
        this.formData.price = parseFloat(document.getElementById('asking-price').value) || 0;
        
        // Show loading state
        const submitBtn = document.getElementById('submit-listing');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Listing Device...';
        submitBtn.disabled = true;
        
        // Attempt to submit listing to backend if API available
        (async () => {
            try {
                if (window.apiService && typeof window.apiService.createListing === 'function') {
                    // If API supports multipart/form-data, build FormData
                    const fd = new FormData();
                    fd.append('title', this.formData.deviceInfo.model || 'Listing');
                    fd.append('price', this.formData.price || 0);
                    fd.append('description', this.formData.description || '');
                    fd.append('condition', JSON.stringify(this.formData.condition || {}));
                    fd.append('device_info', JSON.stringify(this.formData.deviceInfo || {}));
                    // Attach photos as files if available
                    this.formData.photos.forEach((p, idx) => {
                        if (p.file) fd.append('photos', p.file, p.file.name || `photo_${idx}.jpg`);
                    });

                    await window.apiService.request('/listings/', { method: 'POST', body: fd });
                    this.showSuccessMessage();
                } else {
                    // No backend endpoint: fallback to local simulation
                    console.log('Submitting listing (simulated):', this.formData);
                    this.showSuccessMessage();
                }
            } catch (err) {
                console.error('Listing submission failed:', err);
                this.showNotification('Failed to submit listing: ' + (err.message || err), 'danger');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        })();
    }
    
    showSuccessMessage() {
        const formContainer = document.querySelector('.col-lg-8');
        formContainer.innerHTML = `
            <div class="card shadow-sm">
                <div class="card-body text-center py-5">
                    <i class="bi bi-check-circle-fill text-success display-1 mb-3"></i>
                    <h3 class="text-success mb-3">Listing Submitted Successfully!</h3>
                    <p class="text-muted mb-4">Your device has been listed for sale. You can manage your listing from your dashboard.</p>
                    <div class="d-grid gap-2 d-md-block">
                        <a href="dashboard.html" class="btn btn-primary me-md-2">Go to Dashboard</a>
                        <a href="sell.html" class="btn btn-outline-primary">List Another Device</a>
                    </div>
                </div>
            </div>
        `;
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

// Initialize sell page
document.addEventListener('DOMContentLoaded', () => {
    new SellPage();
});