$(document).ready(function () {
    $('#tablaPrestamos').DataTable({
        paging: true,
        ordering: true, // Permitir ordenamiento manual del usuario
        order: [[2, "desc"], [3, "desc"]], // Configuración inicial: prioridad y fechas
        columnDefs: [
            {
                targets: 0, // Columna 0 (Usuario o similar)
                orderable: true,
            },
            {
                targets: 1, // Columna 1 (Préstamos u otra)
                orderable: true,
            },
            {
                targets: 6, // Acciones: No se permite ordenar
                orderable: false,
            },
        ],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json",
        },
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const confirmModal = document.getElementById('confirmModal');
    const modalTitle = document.getElementById('confirmModalLabel');
    const modalMessage = document.getElementById('modalMessage');
    const gameName = document.getElementById('gameName');
    const confirmActionBtn = document.getElementById('confirmActionBtn');

    // Cuando se abre el modal
    confirmModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const message = button.getAttribute('data-message'); // Mensaje personalizado
        const title = button.getAttribute('data-title'); // Título del modal
        const game = button.getAttribute('data-game-name'); // Nombre del juego
        const url = button.getAttribute('data-url'); // URL para confirmar la acción

        // Configura el título, mensaje, nombre del juego y la acción del botón
        modalTitle.textContent = title;
        modalMessage.textContent = message;
        gameName.textContent = game;
        confirmActionBtn.href = url;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});