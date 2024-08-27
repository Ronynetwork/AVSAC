// scripts.js
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

            // Oculta todos os detalhes
            errorDetails.forEach(detail => {
                detail.classList.remove('show');
            });
            // Remove a classe active de todos os títulos
            errorTitles.forEach(t => {
                t.classList.remove('active');
            });

            // Mostra ou oculta o detalhe correspondente
            if (!isVisible) {
                details.classList.add('show');
                title.classList.add('active');
            }
        });
    });

    toggleAllButton.addEventListener('click', () => {
        const allVisible = Array.from(errorDetails).every(detail => detail.classList.contains('show'));

        if (allVisible) {
            // Se todos estão visíveis, oculta todos
            errorDetails.forEach(detail => {
                detail.classList.remove('show');
            });
            errorTitles.forEach(title => {
                title.classList.remove('active');
            });
            toggleAllButton.textContent = 'Show All';
        } else {
            // Se não todos estão visíveis, mostra todos
            errorDetails.forEach(detail => {
                detail.classList.add('show');
            });
            errorTitles.forEach(title => {
                title.classList.add('active');
            });
            toggleAllButton.textContent = 'Hide All';
        }
    });
});
