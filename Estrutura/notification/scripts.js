// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const errorListItems = document.querySelectorAll('#errorList li');
    const detailsContainer = document.getElementById('detailsContainer');

    errorListItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('data-target');
            const targetDetail = document.getElementById(targetId);

            // Oculta todos os detalhes
            const allDetails = detailsContainer.querySelectorAll('.details');
            allDetails.forEach(detail => {
                detail.classList.remove('active');
            });

            // Mostra o detalhe correspondente
            if (targetDetail) {
                targetDetail.classList.add('active');
            }
        });
    });
});
