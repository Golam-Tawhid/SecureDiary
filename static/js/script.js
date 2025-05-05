/**
 * Secure Diary Application
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password strength indicator if password fields exist
    const passwordField = document.querySelector('input[type="password"][name="password"]');
    if (passwordField) {
        // Create password strength indicator
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength mt-2 progress';
        strengthIndicator.style.height = '5px';
        
        const strengthBar = document.createElement('div');
        strengthBar.className = 'progress-bar';
        strengthBar.style.width = '0%';
        strengthBar.setAttribute('role', 'progressbar');
        strengthBar.setAttribute('aria-valuenow', '0');
        strengthBar.setAttribute('aria-valuemin', '0');
        strengthBar.setAttribute('aria-valuemax', '100');
        
        strengthIndicator.appendChild(strengthBar);
        passwordField.parentNode.appendChild(strengthIndicator);
        
        // Assess password strength
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            // Length check
            if (password.length >= 8) strength += 25;
            
            // Complexity checks
            if (/[a-z]/.test(password)) strength += 15;
            if (/[A-Z]/.test(password)) strength += 20;
            if (/[0-9]/.test(password)) strength += 20;
            if (/[^a-zA-Z0-9]/.test(password)) strength += 20;
            
            // Update progress bar
            strengthBar.style.width = strength + '%';
            
            // Update color based on strength
            if (strength < 40) {
                strengthBar.className = 'progress-bar bg-danger';
            } else if (strength < 70) {
                strengthBar.className = 'progress-bar bg-warning';
            } else {
                strengthBar.className = 'progress-bar bg-success';
            }
            
            strengthBar.setAttribute('aria-valuenow', strength);
        });
    }
    
    // Auto-resize textarea fields
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        // Trigger on page load
        textarea.dispatchEvent(new Event('input'));
    });
});
