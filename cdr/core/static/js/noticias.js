document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById("deleteModal");
    const noticiaTitulo = document.getElementById("noticiaTitulo");
    const deleteForm = document.getElementById("deleteForm");

    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget; // Botón que abrió el modal
        const noticiaId = button.getAttribute("data-id");
        const noticiaName = button.getAttribute("data-titulo");

        // Actualizar el contenido del modal
        noticiaTitulo.textContent = noticiaName;

        // Actualizar la acción del formulario
        deleteForm.action = `/noticias/eliminar/${noticiaId}`;
    });
});