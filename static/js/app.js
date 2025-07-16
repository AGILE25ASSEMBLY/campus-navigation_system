// Campus Navigation System - JavaScript functionality

// Global variables
let locations = [];
let currentQRCode = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadLocations();
    generateQRCode();
});

function initializeApp() {
    console.log('Campus Navigation System initialized');
    
    // Check if we're on mobile device
    if (window.innerWidth <= 768) {
        document.body.classList.add('mobile-device');
    }
    
    // Add touch event support
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
    }
}

function setupEventListeners() {
    // Search functionality for start location
    const startInput = document.getElementById('start');
    const destInput = document.getElementById('destination');
    
    if (startInput) {
        startInput.addEventListener('input', function() {
            handleLocationSearch(this.value, 'startSuggestions');
        });
        
        startInput.addEventListener('blur', function() {
            // Delay hiding suggestions to allow clicks
            setTimeout(() => {
                hideSuggestions('startSuggestions');
            }, 200);
        });
    }
    
    if (destInput) {
        destInput.addEventListener('input', function() {
            handleLocationSearch(this.value, 'destinationSuggestions');
        });
        
        destInput.addEventListener('blur', function() {
            // Delay hiding suggestions to allow clicks
            setTimeout(() => {
                hideSuggestions('destinationSuggestions');
            }, 200);
        });
    }
    
    // Form submission
    const form = document.getElementById('navigationForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
    }
    
    // Window resize handler
    window.addEventListener('resize', function() {
        if (currentQRCode) {
            generateQRCode();
        }
    });
}

async function loadLocations() {
    try {
        const response = await fetch('/api/locations');
        const data = await response.json();
        
        locations = [];
        data.forEach(floor => {
            floor.locations.forEach(location => {
                locations.push({
                    key: location.key,
                    name: location.name,
                    floor: floor.floor
                });
            });
        });
        
        console.log('Loaded locations:', locations.length);
    } catch (error) {
        console.error('Error loading locations:', error);
    }
}

function handleLocationSearch(query, suggestionContainerId) {
    const container = document.getElementById(suggestionContainerId);
    
    if (!container || !query.trim()) {
        hideSuggestions(suggestionContainerId);
        return;
    }
    
    // Filter locations based on query
    const filtered = locations.filter(location => 
        location.name.toLowerCase().includes(query.toLowerCase()) ||
        location.key.toLowerCase().includes(query.toLowerCase())
    ).slice(0, 5); // Limit to 5 suggestions
    
    if (filtered.length === 0) {
        hideSuggestions(suggestionContainerId);
        return;
    }
    
    // Build suggestions HTML
    const suggestionsHTML = filtered.map(location => `
        <div class="suggestion-item" onclick="selectLocation('${location.key}', '${location.name}', '${suggestionContainerId}')">
            <div class="suggestion-name">${location.name}</div>
            <div class="suggestion-floor">${location.floor}</div>
        </div>
    `).join('');
    
    container.innerHTML = suggestionsHTML;
    container.style.display = 'block';
}

function selectLocation(key, name, suggestionContainerId) {
    const inputId = suggestionContainerId.replace('Suggestions', '');
    const input = document.getElementById(inputId);
    
    if (input) {
        input.value = name;
    }
    
    hideSuggestions(suggestionContainerId);
}

function hideSuggestions(suggestionContainerId) {
    const container = document.getElementById(suggestionContainerId);
    if (container) {
        container.style.display = 'none';
    }
}

function generateQRCode() {
    const qrContainer = document.getElementById('qrcode');
    if (!qrContainer) return;
    
    // Clear existing QR code
    qrContainer.innerHTML = '';
    
    // Get current URL
    const currentUrl = window.location.origin + window.location.pathname;
    
    // Determine QR code size based on screen size
    const isMobile = window.innerWidth <= 768;
    const qrSize = isMobile ? 6 : 8;
    
    try {
        // Generate QR code using qrcode-generator
        const qr = qrcode(0, 'M');
        qr.addData(currentUrl);
        qr.make();
        
        // Create canvas element
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        const cellSize = isMobile ? 4 : 6;
        const modules = qr.getModuleCount();
        const canvasSize = modules * cellSize;
        
        canvas.width = canvasSize;
        canvas.height = canvasSize;
        
        // Draw QR code
        for (let row = 0; row < modules; row++) {
            for (let col = 0; col < modules; col++) {
                ctx.fillStyle = qr.isDark(row, col) ? '#000000' : '#ffffff';
                ctx.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
            }
        }
        
        // Add border styling
        canvas.style.border = '2px solid var(--bs-border-color)';
        canvas.style.borderRadius = '8px';
        canvas.style.padding = '10px';
        canvas.style.background = 'var(--bs-body-bg)';
        
        qrContainer.appendChild(canvas);
        console.log('QR Code generated successfully');
        currentQRCode = true;
        
    } catch (error) {
        console.error('QR Code generation failed:', error);
        qrContainer.innerHTML = '<p class="text-danger">Failed to generate QR code</p>';
    }
}

// Utility functions
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
});

// Service Worker registration (for PWA functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Note: Service worker file would need to be created separately
        // navigator.serviceWorker.register('/service-worker.js');
    });
}

// Accessibility improvements
document.addEventListener('keydown', function(event) {
    // Escape key closes suggestions
    if (event.key === 'Escape') {
        hideSuggestions('startSuggestions');
        hideSuggestions('destinationSuggestions');
    }
});

// Performance optimization
const debouncedSearch = debounce(handleLocationSearch, 300);

// Export functions for use in other scripts
window.CampusNavigation = {
    generateQRCode,
    showToast,
    loadLocations
};
