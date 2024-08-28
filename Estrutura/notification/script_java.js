document.addEventListener('DOMContentLoaded', () => {
    const errorTitles = document.querySelectorAll('.error-title');
    const toggleAllButton = document.getElementById('toggleAll');
    const errorDetails = document.querySelectorAll('.error-details');

    function toggleDetails(details, show) {
        if (show) {
            details.classList.add('show');
        } else {
            details.classList.remove('show');
        }
    }

    errorTitles.forEach(title => {
        title.addEventListener('click', () => {
            const details = title.nextElementSibling;
            const isVisible = details.classList.contains('show');

            errorDetails.forEach(detail => {
                detail.classList.remove('show');
            });

            errorTitles.forEach(t => {
                t.classList.remove('active');
            });

            if (!isVisible) {
                details.classList.add('show');
                title.classList.add('active');
            }
        });
    });

    if (toggleAllButton) {
        toggleAllButton.addEventListener('click', () => {
            const allVisible = Array.from(errorDetails).every(detail => detail.classList.contains('show'));

            if (allVisible) {
                errorDetails.forEach(detail => {
                    detail.classList.remove('show');
                });
                errorTitles.forEach(title => {
                    title.classList.remove('active');
                });
                toggleAllButton.textContent = 'Show All';
            } else {
                errorDetails.forEach(detail => {
                    detail.classList.add('show');
                });
                errorTitles.forEach(title => {
                    title.classList.add('active');
                });
                toggleAllButton.textContent = 'Hide All';
            }
        });
    } else {
        console.warn('Toggle All button not found.');
    }
});
