// Main JavaScript for Travel Agent Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any components
    initializeComponents();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize login page functionality if we're on the login page
    initLoginPage();
});

// Initialize UI components
function initializeComponents() {
    // Initialize date pickers
    const datePickers = document.querySelectorAll('.date-picker');
    if (datePickers) {
        datePickers.forEach(function(picker) {
            picker.valueAsDate = new Date();
        });
    }
    
    // Initialize any alerts with auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        alerts.forEach(function(alert) {
            if (!alert.classList.contains('alert-persistent')) {
                setTimeout(function() {
                    alert.style.opacity = '0';
                    setTimeout(function() {
                        alert.style.display = 'none';
                    }, 500);
                }, 5000);
            }
        });
    }
}

// Set up event listeners
function setupEventListeners() {
    // Form validation
    const forms = document.querySelectorAll('form.needs-validation');
    if (forms) {
        forms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }
    
    // Booking price calculation
    const packageSelect = document.getElementById('package-select');
    const numTravelers = document.getElementById('num-travelers');
    const totalPrice = document.getElementById('total-price');
    
    if (packageSelect && numTravelers && totalPrice) {
        const updatePrice = function() {
            const packageOption = packageSelect.options[packageSelect.selectedIndex];
            const price = parseFloat(packageOption.getAttribute('data-price') || 0);
            const travelers = parseInt(numTravelers.value || 1);
            
            totalPrice.textContent = (price * travelers).toFixed(2);
        };
        
        packageSelect.addEventListener('change', updatePrice);
        numTravelers.addEventListener('change', updatePrice);
        numTravelers.addEventListener('keyup', updatePrice);
    }
    
    // Delete confirmation
    const deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons) {
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    event.preventDefault();
                }
            });
        });
    }
}

// Function for booking status changes
function updateBookingStatus(bookingId, status) {
    const form = document.getElementById('status-form');
    const statusInput = document.getElementById('status');
    
    if (form && statusInput) {
        statusInput.value = status;
        form.submit();
    }
}

// Function to preview travel package details
function previewPackage(packageId) {
    fetch(`/packages/${packageId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('preview-name').textContent = data.name;
            document.getElementById('preview-destination').textContent = data.destination;
            document.getElementById('preview-duration').textContent = `${data.duration} days`;
            document.getElementById('preview-price').textContent = `$${data.price}`;
            
            const previewModal = new bootstrap.Modal(document.getElementById('package-preview-modal'));
            previewModal.show();
        })
        .catch(error => {
            console.error('Error fetching package details:', error);
            alert('Could not load package details. Please try again.');
        });
}
