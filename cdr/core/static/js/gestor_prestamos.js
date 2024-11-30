$(document).ready(function() {
    $('#tablaPrestamos').DataTable({
        paging: true,          // Activa la paginación
        searching: true,       // Activa el filtro de búsqueda
        ordering: true,        // Activa el ordenamiento por columnas
        order: [[2, 'desc']],   // Ordena por la columna "Estado" al cargar
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" // Traducción al español
        },
        columnDefs: [
            { orderable: false, targets: 5 } // Desactiva el ordenamiento en la columna de "Acciones"
        ]
    });
});