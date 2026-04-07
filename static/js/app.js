/**
 * Premium Attendance System - JavaScript
 * Modern Web Application with Glassmorphism UI
 */

// Global variables
let currentPage = '';
let isAdmin = false;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Detect current page
    currentPage = detectCurrentPage();
    
    // Initialize page-specific functionality
    switch(currentPage) {
        case 'landing':
            initializeLandingPage();
            break;
        case 'employee':
            initializeEmployeePage();
            break;
        case 'admin-login':
            initializeAdminLogin();
            break;
        case 'admin-dashboard':
            initializeAdminDashboard();
            break;
        case 'employee-stats':
            initializeEmployeeStats();
            break;
    }
    
    // Initialize common features
    initializeCommonFeatures();
}

function detectCurrentPage() {
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index.html') {
        return 'landing';
    } else if (path === '/employee') {
        return 'employee';
    } else if (path === '/admin/login') {
        return 'admin-login';
    } else if (path === '/admin/dashboard') {
        return 'admin-dashboard';
    } else if (path === '/admin/employee_stats') {
        return 'employee-stats';
    }
    
    return 'unknown';
}

// ==================== COMMON FEATURES ====================

function initializeCommonFeatures() {
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Add loading states
    addLoadingStates();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Add tooltips
    addTooltips();
    
    // Initialize animations
    initializeAnimations();
}

function addSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addLoadingStates() {
    // Add loading state to buttons on click
    document.querySelectorAll('.glass-button').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled && !this.classList.contains('no-loading')) {
                showButtonLoading(this);
            }
        });
    });
}

function showButtonLoading(button) {
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    button.disabled = true;
    
    // Reset after 3 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalContent;
        button.disabled = false;
    }, 3000);
}

function hideButtonLoading(button, originalContent) {
    button.innerHTML = originalContent;
    button.disabled = false;
}

function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Escape key - close modals, go back
        if (e.key === 'Escape') {
            closeModals();
        }
        
        // Ctrl/Cmd + Enter - submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                activeForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Admin shortcuts (when logged in)
        if (isAdmin) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                window.location.href = '/admin/dashboard';
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                e.preventDefault();
                window.location.href = '/admin/employee_stats';
            }
        }
    });
}

function addTooltips() {
    // Simple tooltip implementation
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe all glass cards
    document.querySelectorAll('.glass-card').forEach(card => {
        observer.observe(card);
    });
}

function closeModals() {
    // Close any open modals or dropdowns
    document.querySelectorAll('.modal, .dropdown-open').forEach(modal => {
        modal.classList.remove('show', 'dropdown-open');
    });
}

// ==================== LANDING PAGE ====================

function initializeLandingPage() {
    console.log('Initializing landing page...');
    
    // Load system statistics
    loadSystemStats();
    
    // Add hover effects to action buttons
    addActionButtonEffects();
    
    // Initialize background animation
    initializeBackgroundAnimation();
}

function loadSystemStats() {
    // Simulate loading system stats
    // In a real implementation, this would fetch from an API
    setTimeout(() => {
        const registeredElement = document.getElementById('registered-count');
        const todayElement = document.getElementById('today-count');
        
        if (registeredElement) {
            animateCounter(registeredElement, 0, 4, 'People');
        }
        
        if (todayElement) {
            animateCounter(todayElement, 0, 2, 'Marked');
        }
    }, 500);
}

function animateCounter(element, start, end, suffix) {
    const duration = 1000;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = `${current} ${suffix}`;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

function addActionButtonEffects() {
    document.querySelectorAll('.action-buttons .glass-button').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

function initializeBackgroundAnimation() {
    // Add parallax effect to floating shapes
    document.addEventListener('mousemove', function(e) {
        const shapes = document.querySelectorAll('.floating-shape');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 0.5;
            const x = (mouseX - 0.5) * speed * 20;
            const y = (mouseY - 0.5) * speed * 20;
            
            shape.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
}

// ==================== GPS LOCATION FUNCTIONS ====================

let gpsWatchId = null;
let lastKnownLocation = null;
let gpsAttempts = 0;
const MAX_GPS_ATTEMPTS = 3;

function initializeGPS() {
    console.log('🌍 Initializing GPS location services...');
    
    if (!navigator.geolocation) {
        console.warn('⚠️ Geolocation is not supported by this browser');
        showGPSStatus('GPS not supported', 'error');
        return;
    }
    
    // Start GPS tracking in background
    startBackgroundGPS();
}

function startBackgroundGPS() {
    gpsAttempts++;
    
    if (gpsAttempts > MAX_GPS_ATTEMPTS) {
        console.log('📍 Max GPS attempts reached, continuing without GPS');
        showGPSStatus('GPS unavailable - attendance still works', 'warning');
        return;
    }
    
    showGPSStatus(`Trying GPS (${gpsAttempts}/${MAX_GPS_ATTEMPTS})...`, 'warning');
    
    const options = {
        enableHighAccuracy: false,
        timeout: 8000,  // Shorter timeout
        maximumAge: 600000  // 10 minutes cache
    };
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            lastKnownLocation = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy
            };
            console.log('📍 GPS location acquired:', lastKnownLocation);
            showGPSStatus(`GPS Active (±${Math.round(position.coords.accuracy)}m)`, 'success');
            
            // Try to update any recent attendance with GPS data
            updateRecentAttendanceWithGPS();
        },
        (error) => {
            console.warn(`⚠️ GPS attempt ${gpsAttempts} failed:`, error.message);
            
            if (gpsAttempts < MAX_GPS_ATTEMPTS) {
                // Retry after delay
                setTimeout(() => {
                    startBackgroundGPS();
                }, 2000);
            } else {
                showGPSStatus('GPS failed - attendance still works', 'warning');
            }
        },
        options
    );
}

function updateRecentAttendanceWithGPS() {
    if (!lastKnownLocation) return;
    
    console.log('📤 Updating recent attendance with GPS data...');
    
    fetch('/api/log_gps_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(lastKnownLocation)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('✅ GPS location added to attendance record');
        } else {
            console.log('ℹ️ No recent attendance to update with GPS');
        }
    })
    .catch(error => {
        console.warn('⚠️ Could not update attendance with GPS:', error);
    });
}

function showGPSStatus(message, type) {
    const gpsStatus = document.getElementById('gps-status');
    const retryButton = document.getElementById('retry-gps');
    
    if (gpsStatus) {
        gpsStatus.textContent = message;
        gpsStatus.className = `gps-status gps-${type}`;
    }
    
    // Show retry button for errors
    if (retryButton) {
        if (type === 'warning' || type === 'error') {
            retryButton.style.display = 'inline-block';
            retryButton.onclick = () => {
                console.log('🔄 Manual GPS retry...');
                gpsAttempts = 0;  // Reset attempts
                startBackgroundGPS();
            };
        } else {
            retryButton.style.display = 'none';
        }
    }
}

// Periodically try to get GPS and update attendance
setInterval(() => {
    if (!lastKnownLocation && gpsAttempts < MAX_GPS_ATTEMPTS) {
        startBackgroundGPS();
    } else if (lastKnownLocation) {
        updateRecentAttendanceWithGPS();
    }
}, 10000); // Try every 10 seconds

// ==================== EMPLOYEE PAGE ====================

function initializeEmployeePage() {
    console.log('Initializing employee page...');
    
    // Initialize GPS location services in background
    initializeGPS();
    
    // Initialize camera controls
    initializeCameraControls();
    
    // Update time display
    updateTimeDisplay();
    setInterval(updateTimeDisplay, 1000);
    
    // Load employee page stats
    loadEmployeePageStats();
}

function initializeCameraControls() {
    const startButton = document.getElementById('start-camera');
    const stopButton = document.getElementById('stop-camera');
    
    if (startButton) {
        startButton.addEventListener('click', startCamera);
    }
    
    if (stopButton) {
        stopButton.addEventListener('click', stopCamera);
    }
}

function startCamera() {
    const startButton = document.getElementById('start-camera');
    const stopButton = document.getElementById('stop-camera');
    const placeholder = document.getElementById('camera-placeholder');
    const feed = document.getElementById('camera-feed');
    
    // Show loading state
    showButtonLoading(startButton);
    
    fetch('/api/start_camera', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Hide placeholder, show feed
            if (placeholder) placeholder.style.display = 'none';
            if (feed) {
                feed.style.display = 'block';
                feed.src = '/video_feed?' + new Date().getTime(); // Prevent caching
            }
            
            // Switch buttons
            if (startButton) startButton.style.display = 'none';
            if (stopButton) stopButton.style.display = 'inline-flex';
            
            // Update status
            updateCameraStatus('Camera Active - Face Recognition Running', 'success');
            
            // Start checking for recognition events
            startRecognitionMonitoring();
        } else {
            updateCameraStatus('Failed to start camera', 'error');
        }
    })
    .catch(error => {
        console.error('Error starting camera:', error);
        updateCameraStatus('Error starting camera', 'error');
    })
    .finally(() => {
        hideButtonLoading(startButton, '<i class="fas fa-play"></i> Start Camera');
    });
}

function stopCamera() {
    const startButton = document.getElementById('start-camera');
    const stopButton = document.getElementById('stop-camera');
    const placeholder = document.getElementById('camera-placeholder');
    const feed = document.getElementById('camera-feed');
    
    // Show loading state
    stopButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Stopping...';
    stopButton.disabled = true;
    
    fetch('/api/stop_camera', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show placeholder, hide feed
            if (feed) feed.style.display = 'none';
            if (placeholder) placeholder.style.display = 'flex';
            
            // Switch buttons
            if (stopButton) stopButton.style.display = 'none';
            if (startButton) startButton.style.display = 'inline-flex';
            
            // Update status
            updateCameraStatus('Camera Inactive', 'inactive');
            
            // Stop recognition monitoring
            stopRecognitionMonitoring();
            
            console.log('✅ Camera stopped successfully');
        } else {
            console.error('❌ Failed to stop camera:', data.message);
            updateCameraStatus('Error stopping camera', 'error');
        }
    })
    .catch(error => {
        console.error('❌ Error stopping camera:', error);
        updateCameraStatus('Error stopping camera', 'error');
    })
    .finally(() => {
        // Reset button state
        stopButton.innerHTML = '<i class="fas fa-stop"></i> Stop Camera';
        stopButton.disabled = false;
    });
}

function updateCameraStatus(text, type) {
    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.status-dot');
    
    if (statusText) statusText.textContent = text;
    
    if (statusDot) {
        // Remove existing classes
        statusDot.classList.remove('status-success', 'status-error', 'status-inactive');
        
        // Add new class
        statusDot.classList.add(`status-${type}`);
    }
}

function updateTimeDisplay() {
    const timeElement = document.getElementById('current-time');
    const dateElement = document.getElementById('current-date');
    
    if (timeElement) {
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString();
    }
    
    if (dateElement) {
        const now = new Date();
        dateElement.textContent = now.toLocaleDateString();
    }
}

function loadEmployeePageStats() {
    // Load registered people count
    const registeredElement = document.getElementById('registered-people');
    if (registeredElement) {
        // This would typically come from an API
        registeredElement.textContent = '4 People';
    }
}

let recognitionMonitoringInterval;

function startRecognitionMonitoring() {
    // Monitor for recognition events (placeholder)
    recognitionMonitoringInterval = setInterval(() => {
        // In a real implementation, this might poll for recent recognitions
        // or use WebSocket for real-time updates
    }, 1000);
}

function stopRecognitionMonitoring() {
    if (recognitionMonitoringInterval) {
        clearInterval(recognitionMonitoringInterval);
    }
}

// ==================== ADMIN LOGIN ====================

function initializeAdminLogin() {
    console.log('🔐 Initializing admin login...');
    
    const loginForm = document.getElementById('login-form');
    const passwordInput = document.getElementById('password');
    
    console.log('🔐 Login form found:', !!loginForm);
    console.log('🔐 Password input found:', !!passwordInput);
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleAdminLogin);
        console.log('🔐 Submit event listener added');
    }
    
    if (passwordInput) {
        passwordInput.focus();
        passwordInput.addEventListener('input', clearLoginErrors);
        console.log('🔐 Password input focused and input listener added');
    }
    
    console.log('🔐 Admin login initialization complete');
}

function handleAdminLogin(e) {
    e.preventDefault();
    
    const passwordInput = document.getElementById('password');
    const loginButton = e.target.querySelector('button[type="submit"]');
    const password = passwordInput.value.trim();
    
    if (!password) {
        showLoginError('Please enter a password');
        return;
    }
    
    // Store original content and show loading state
    const originalContent = loginButton.innerHTML;
    loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Logging in...</span>';
    loginButton.disabled = true;
    
    console.log('🔐 Attempting admin login...');
    
    // Send login request
    fetch('/api/admin/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => {
        console.log('🔐 Login response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('🔐 Login response data:', data);
        if (data.success) {
            isAdmin = true;
            // Success animation
            loginButton.innerHTML = '<i class="fas fa-check"></i> <span>Success!</span>';
            loginButton.style.background = 'rgba(63, 185, 80, 0.3)';
            
            console.log('✅ Login successful, redirecting to dashboard...');
            
            // Redirect after short delay
            setTimeout(() => {
                window.location.href = '/admin/dashboard';
            }, 1000);
        } else {
            console.log('❌ Login failed:', data.message);
            showLoginError(data.message || 'Invalid password. Please try again.');
            // Reset button
            loginButton.innerHTML = originalContent;
            loginButton.disabled = false;
        }
    })
    .catch(error => {
        console.error('❌ Login error:', error);
        showLoginError('Connection error. Please try again.');
        // Reset button
        loginButton.innerHTML = originalContent;
        loginButton.disabled = false;
    });
}

function showLoginError(message) {
    const errorElement = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const passwordInput = document.getElementById('password');
    
    if (errorText) errorText.textContent = message;
    if (errorElement) {
        errorElement.style.display = 'flex';
        errorElement.classList.add('shake');
        setTimeout(() => errorElement.classList.remove('shake'), 500);
    }
    if (passwordInput) {
        passwordInput.classList.add('error');
        passwordInput.select();
    }
}

function clearLoginErrors() {
    const errorElement = document.getElementById('error-message');
    const passwordInput = document.getElementById('password');
    
    if (errorElement) errorElement.style.display = 'none';
    if (passwordInput) passwordInput.classList.remove('error');
}

// ==================== ADMIN DASHBOARD ====================

function initializeAdminDashboard() {
    console.log('Initializing admin dashboard...');
    
    isAdmin = true;
    
    // Initialize logout functionality
    initializeLogout();
    
    // Initialize refresh functionality
    initializeRefresh();
    
    // Initialize quick actions
    initializeQuickActions();
    
    // Update time display
    updateDashboardTime();
    setInterval(updateDashboardTime, 1000);
    
    // Load initial activity
    loadInitialActivity();
    
    // Load recent attendance with GPS
    loadRecentAttendance();
    
    // Initialize attendance refresh
    initializeAttendanceRefresh();
}

function initializeLogout() {
    const logoutButton = document.getElementById('logout-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }
}

function handleLogout() {
    fetch('/api/admin/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            isAdmin = false;
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Logout error:', error);
        // Redirect anyway
        window.location.href = '/';
    });
}

function initializeRefresh() {
    const refreshButton = document.getElementById('refresh-activity');
    if (refreshButton) {
        refreshButton.addEventListener('click', refreshDashboardData);
    }
}

function refreshDashboardData() {
    const refreshButton = document.getElementById('refresh-activity');
    const icon = refreshButton.querySelector('i');
    
    // Add spin animation
    icon.classList.add('fa-spin');
    
    // Fetch updated stats
    fetch('/api/dashboard_stats')
    .then(response => response.json())
    .then(data => {
        updateDashboardStats(data);
        addActivityItem('Data Refreshed', 'Dashboard statistics updated', 'info');
    })
    .catch(error => {
        console.error('Error refreshing data:', error);
        addActivityItem('Refresh Failed', 'Could not update statistics', 'error');
    })
    .finally(() => {
        setTimeout(() => {
            icon.classList.remove('fa-spin');
        }, 1000);
    });
}

function updateDashboardStats(data) {
    // Update stat cards
    const elements = {
        'today-total': data.today_total,
        'today-present': data.today_present,
        'today-late': data.today_late,
        'total-employees': data.total_employees
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            animateCounter(element, parseInt(element.textContent) || 0, value, '');
        }
    });
}

function initializeQuickActions() {
    // Add event listeners for quick action buttons
    const actions = {
        'export-data': exportDashboardData,
        'refresh-stats': refreshDashboardData,
        'view-reports': viewReports,
        'system-settings': systemSettings
    };
    
    Object.entries(actions).forEach(([className, handler]) => {
        document.querySelectorAll(`.${className}`).forEach(button => {
            button.addEventListener('click', handler);
        });
    });
}

function updateDashboardTime() {
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString();
    }
}

function loadInitialActivity() {
    addActivityItem('System Started', 'Admin dashboard loaded successfully', 'success');
}

function addActivityItem(title, description, type) {
    const activityList = document.getElementById('activity-list');
    if (!activityList) return;
    
    const now = new Date().toLocaleTimeString();
    
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.innerHTML = `
        <div class="activity-icon ${type}">
            <i class="fas fa-${getActivityIcon(type)}"></i>
        </div>
        <div class="activity-content">
            <p><strong>${title}</strong></p>
            <small>${description}</small>
        </div>
        <div class="activity-time">
            <span>${now}</span>
        </div>
    `;
    
    // Add with animation
    activityItem.style.opacity = '0';
    activityItem.style.transform = 'translateY(-10px)';
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Animate in
    setTimeout(() => {
        activityItem.style.opacity = '1';
        activityItem.style.transform = 'translateY(0)';
    }, 100);
    
    // Remove old items (keep max 10)
    const items = activityList.querySelectorAll('.activity-item');
    if (items.length > 10) {
        items[items.length - 1].remove();
    }
}

function getActivityIcon(type) {
    const icons = {
        'success': 'check',
        'info': 'info',
        'error': 'exclamation-triangle',
        'warning': 'exclamation'
    };
    return icons[type] || 'info';
}

// Quick action handlers
function exportDashboardData() {
    addActivityItem('Export Started', 'Preparing dashboard data for download', 'info');
    
    // Simulate export process
    setTimeout(() => {
        addActivityItem('Export Complete', 'Dashboard data exported successfully', 'success');
    }, 2000);
}

function viewReports() {
    addActivityItem('Reports Accessed', 'Viewing detailed attendance reports', 'info');
}

function systemSettings() {
    addActivityItem('Settings Opened', 'Accessing system configuration', 'info');
}

function initializeAttendanceRefresh() {
    const refreshButton = document.getElementById('refresh-attendance');
    if (refreshButton) {
        refreshButton.addEventListener('click', loadRecentAttendance);
    }
}

function loadRecentAttendance() {
    const attendanceList = document.getElementById('attendance-list');
    if (!attendanceList) return;
    
    // Show loading
    attendanceList.innerHTML = '<div class="loading-message">Loading attendance records...</div>';
    
    fetch('/api/recent_attendance')
    .then(response => response.json())
    .then(data => {
        if (data.records && data.records.length > 0) {
            displayAttendanceRecords(data.records);
        } else {
            attendanceList.innerHTML = '<div class="no-data-message">No recent attendance records found</div>';
        }
    })
    .catch(error => {
        console.error('Error loading attendance records:', error);
        attendanceList.innerHTML = '<div class="error-message">Error loading attendance records</div>';
    });
}

function displayAttendanceRecords(records) {
    const attendanceList = document.getElementById('attendance-list');
    if (!attendanceList) return;
    
    attendanceList.innerHTML = '';
    
    records.forEach(record => {
        const attendanceItem = document.createElement('div');
        attendanceItem.className = 'attendance-item';
        
        // Format location info
        let locationInfo = '';
        if (record.maps_link) {
            locationInfo = `
                <div class="location-info">
                    <a href="${record.maps_link}" target="_blank" class="maps-link">
                        <i class="fas fa-map-marker-alt"></i> View Location
                    </a>
                    <small>Accuracy: ${record.accuracy}m</small>
                </div>
            `;
        } else {
            locationInfo = '<div class="location-info"><small>Location: Not Available</small></div>';
        }
        
        // Status color
        const statusClass = record.status === 'Present' ? 'success' : 
                           record.status === 'Late' ? 'warning' : 'info';
        
        attendanceItem.innerHTML = `
            <div class="attendance-icon ${statusClass}">
                <i class="fas fa-user-check"></i>
            </div>
            <div class="attendance-content">
                <p><strong>${record.name}</strong> - ${record.status}</p>
                <small>${record.date} at ${record.time}</small>
                ${locationInfo}
            </div>
        `;
        
        attendanceList.appendChild(attendanceItem);
    });
}

// ==================== EMPLOYEE STATS ====================

function initializeEmployeeStats() {
    console.log('Initializing employee stats...');
    
    isAdmin = true;
    
    // Initialize employee selection
    initializeEmployeeSelection();
    
    // Initialize export functionality
    initializeStatsExport();
}

function initializeEmployeeSelection() {
    const employeeSelect = document.getElementById('employee-select');
    const loadButton = document.getElementById('load-stats');
    
    if (employeeSelect) {
        employeeSelect.addEventListener('change', function() {
            if (loadButton) {
                loadButton.disabled = !this.value;
            }
        });
    }
    
    if (loadButton) {
        loadButton.addEventListener('click', function() {
            const selectedEmployee = employeeSelect.value;
            if (selectedEmployee) {
                loadEmployeeStatistics(selectedEmployee);
            }
        });
    }
}

function loadEmployeeStatistics(employeeName) {
    const statsDisplay = document.getElementById('stats-display');
    const noSelection = document.getElementById('no-selection');
    const employeeNameElement = document.getElementById('employee-name');
    const employeeStatusElement = document.getElementById('employee-status');
    
    // Update UI
    if (employeeNameElement) employeeNameElement.textContent = employeeName;
    if (employeeStatusElement) employeeStatusElement.textContent = 'Loading statistics...';
    
    // Show stats display
    if (noSelection) noSelection.style.display = 'none';
    if (statsDisplay) statsDisplay.style.display = 'block';
    
    // Fetch employee stats
    fetch(`/api/employee_stats/${employeeName}`)
    .then(response => response.json())
    .then(data => {
        updateEmployeeStatsDisplay(data);
        // Charts would be initialized here if Chart.js is available
    })
    .catch(error => {
        console.error('Error loading employee stats:', error);
        if (employeeStatusElement) {
            employeeStatusElement.textContent = 'Error loading statistics';
        }
    });
}

function updateEmployeeStatsDisplay(data) {
    // Update employee info
    const employeeStatus = document.getElementById('employee-status');
    const attendancePercentage = document.getElementById('attendance-percentage');
    
    if (employeeStatus) {
        employeeStatus.textContent = `Last seen: ${data.last_attendance}`;
    }
    
    if (attendancePercentage) {
        attendancePercentage.textContent = `${Math.round(data.attendance_percentage)}%`;
    }
    
    // Update stat cards
    const statElements = {
        'total-days': data.total_days,
        'present-days': data.present_days,
        'late-days': data.late_days,
        'last-attendance': data.last_attendance
    };
    
    Object.entries(statElements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            if (typeof value === 'number') {
                animateCounter(element, 0, value, '');
            } else {
                element.textContent = value;
            }
        }
    });
    
    // Update score circle color
    updateScoreCircle(data.attendance_percentage);
}

function updateScoreCircle(percentage) {
    const scoreCircle = document.querySelector('.score-circle');
    if (!scoreCircle) return;
    
    // Remove existing classes
    scoreCircle.classList.remove('excellent', 'good', 'average', 'poor');
    
    // Add appropriate class
    if (percentage >= 90) {
        scoreCircle.classList.add('excellent');
    } else if (percentage >= 75) {
        scoreCircle.classList.add('good');
    } else if (percentage >= 60) {
        scoreCircle.classList.add('average');
    } else {
        scoreCircle.classList.add('poor');
    }
}

function initializeStatsExport() {
    const exportButton = document.getElementById('export-employee-data');
    if (exportButton) {
        exportButton.addEventListener('click', exportEmployeeData);
    }
}

function exportEmployeeData() {
    const employeeSelect = document.getElementById('employee-select');
    if (!employeeSelect || !employeeSelect.value) {
        alert('Please select an employee first');
        return;
    }
    
    const employeeName = employeeSelect.value;
    
    // Show loading state
    const exportButton = document.getElementById('export-employee-data');
    const originalContent = exportButton.innerHTML;
    showButtonLoading(exportButton);
    
    // Simulate export process
    setTimeout(() => {
        // In a real implementation, this would generate and download a CSV file
        alert(`Export completed for ${employeeName}`);
        hideButtonLoading(exportButton, originalContent);
    }, 2000);
}

// ==================== UTILITY FUNCTIONS ====================

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

function formatTime(date) {
    return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).format(date);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// ==================== ERROR HANDLING ====================

window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.message) {
        showNotification('An error occurred. Please refresh the page.', 'error');
    }
});

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ==================== PERFORMANCE MONITORING ====================

// Monitor page load performance
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${Math.round(loadTime)}ms`);
    
    // Report slow loads
    if (loadTime > 3000) {
        console.warn('Slow page load detected');
    }
});

// Export functions for global access
window.AttendanceApp = {
    showNotification,
    addActivityItem,
    updateCameraStatus,
    exportEmployeeData
};