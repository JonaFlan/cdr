    // JavaScript para actualizar el formulario de eliminación con el ID del juego seleccionado
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const juegoId = button.getAttribute('data-id');
        const juegoNombre = button.getAttribute('data-nombre');
        
        // Actualizar el nombre del juego en el modal
        const nombreElement = document.getElementById('juegoNombre');
        nombreElement.textContent = juegoNombre;

        // Crear el formulario dinámicamente con el ID del juego
        const deleteForm = document.getElementById('deleteForm');
        deleteForm.action = "/juegos/eliminar/0".replace('0', juegoId);
    });