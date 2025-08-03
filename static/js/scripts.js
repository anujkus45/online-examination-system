// Global JavaScript for the Online Examination System

// Document ready function (similar to jQuery's $(document).ready())
document.addEventListener('DOMContentLoaded', function() {
    console.log("Online Examination System scripts loaded!");

    // Example: Dismiss Bootstrap alerts automatically after a few seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-dismissible')) { // Don't auto-dismiss if it has a close button
            setTimeout(function() {
                const bootstrapAlert = bootstrap.Alert.getInstance(alert);
                if (bootstrapAlert) {
                    bootstrapAlert.close();
                } else {
                    // Fallback for alerts without a close button initialized by JS
                    alert.remove();
                }
            }, 5000); // Dismiss after 5 seconds
        }
    });


});


