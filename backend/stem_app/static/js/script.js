// Main JavaScript file for STEM Project Management

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Format datetime-local inputs with current project deadline
    const deadlineInputs = document.querySelectorAll('input[type="datetime-local"]');
    deadlineInputs.forEach(input => {
        if (!input.value && input.dataset.value) {
            // Convert ISO format to format expected by datetime-local input
            const date = new Date(input.dataset.value);
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');

            input.value = `${year}-${month}-${day}T${hours}:${minutes}`;
        }
    });

    // File input custom text
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function (e) {
            const fileName = this.files[0]?.name || 'Chọn file';
            const nextSibling = this.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });

    // Confirmation dialogs
    const confirmForms = document.querySelectorAll('.needs-confirmation');
    confirmForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!confirm('Bạn có chắc chắn muốn thực hiện hành động này?')) {
                e.preventDefault();
                return false;
            }
        });
    });
}); 