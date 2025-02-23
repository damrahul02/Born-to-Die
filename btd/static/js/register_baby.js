document.addEventListener('DOMContentLoaded', function() {
    // Date handling
    const yearSelect = document.getElementById('selectYear');
    const monthSelect = document.getElementById('selectMonth');
    const daySelect = document.getElementById('selectDay');

    // Populate year dropdown
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= currentYear - 10; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }

    // Populate month dropdown
    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    months.forEach(month => {
        const option = document.createElement('option');
        option.value = month;
        option.textContent = month;
        monthSelect.appendChild(option);
    });

    // Update days based on month and year
    function updateDays() {
        const year = parseInt(yearSelect.value);
        const month = monthSelect.selectedIndex + 1;
        const daysInMonth = new Date(year, month, 0).getDate();

        daySelect.innerHTML = '';
        for (let day = 1; day <= daysInMonth; day++) {
            const option = document.createElement('option');
            option.value = day;
            option.textContent = day;
            daySelect.appendChild(option);
        }
    }

    yearSelect.addEventListener('change', updateDays);
    monthSelect.addEventListener('change', updateDays);

    // Initial days population
    updateDays();

    // Form validation
    document.getElementById('babyRegistrationForm').addEventListener('submit', function(e) {
        const required = [
            'first_name', 'last_name', 'full_name', 'gender', 'religion',
            'birth_country', 'present_address', 'permanent_address',
            'fatherName', 'fatherNid', 'motherName', 'motherNid',
            'contact', 'relationship'
        ];

        let isValid = true;
        required.forEach(field => {
            const input = document.querySelector(`[name="${field}"]`);
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});