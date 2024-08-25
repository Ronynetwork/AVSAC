// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os títulos dos erros
    const errorTitles = document.querySelectorAll('.error-title');

    errorTitles.forEach(title => {
        title.addEventListener('click', () => {
            // Seleciona o próximo elemento irmão (detalhes do erro)
            const details = title.nextElementSibling;

            // Alterna a visibilidade dos detalhes
            if (details.classList.contains('show')) {
                details.classList.remove('show');
            } else {
                // Esconde todos os detalhes
                document.querySelectorAll('.error-details').forEach(detail => {
                    detail.classList.remove('show');
                });
                // Mostra o detalhe clicado
                details.classList.add('show');
            }
        });
    });
});
