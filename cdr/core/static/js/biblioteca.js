    // JavaScript para actualizar el formulario de eliminación con el ID del juego seleccionado
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const juegoId = button.getAttribute('data-id');
        const juegoNombre = button.getAttribute('data-nombre');
        
        // Actualizar el nombre del juego en el modal
        const nombreElement = document.getElementById('juegoNombre');
        nombreElement.textContent = juegoNombre;

        // Actualizar el formulario de eliminación con la URL correcta
        const deleteForm = document.getElementById('deleteForm');
        deleteForm.action = "{% url 'juego_eliminar' 0 %}".slice(0, -1) + juegoId + "/";
    });