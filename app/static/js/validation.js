// Handle flash messages
function handleFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const category = message.dataset.category;
        const text = message.textContent;
        const icon = category === 'success' ? 'success' : 
                    category === 'error' ? 'error' : 'info';
        
        Swal.fire({
            title: category.charAt(0).toUpperCase() + category.slice(1),
            text: text,
            icon: icon,
            confirmButtonColor: '#0d6efd'
        });
    });
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            Swal.fire({
                title: 'Validation Error',
                text: `${field.name} is required`,
                icon: 'error',
                confirmButtonColor: '#0d6efd'
            });
        }
    });

    return isValid;
}

// Check if customer exists
async function checkExistingCustomer(field, value) {
    try {
        const response = await fetch(`/api/check-customer?${field}=${encodeURIComponent(value)}`);
        const data = await response.json();
        return data.exists;
    } catch (error) {
        console.error('Error checking customer:', error);
        return false;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle flash messages
    handleFlashMessages();

    // Add form validation to all forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });

    // Form validation for registration
    const registrationForm = document.querySelector('#registrationForm');
    if (registrationForm) {
        const emailInput = registrationForm.querySelector('input[name="email"]');
        const phoneInput = registrationForm.querySelector('input[name="phone"]');
        
        // Check email on blur
        emailInput?.addEventListener('blur', async function() {
            if (this.value) {
                const exists = await checkExistingCustomer('email', this.value);
                if (exists) {
                    Swal.fire({
                        title: 'Email Already Registered',
                        text: 'A customer with this email already exists!',
                        icon: 'warning',
                        confirmButtonColor: '#0d6efd'
                    });
                    this.value = '';
                    this.focus();
                }
            }
        });
        
        // Check phone on blur
        phoneInput?.addEventListener('blur', async function() {
            if (this.value) {
                const exists = await checkExistingCustomer('phone', this.value);
                if (exists) {
                    Swal.fire({
                        title: 'Phone Number Already Registered',
                        text: 'A customer with this phone number already exists!',
                        icon: 'warning',
                        confirmButtonColor: '#0d6efd'
                    });
                    this.value = '';
                    this.focus();
                }
            }
        });
    }
});
