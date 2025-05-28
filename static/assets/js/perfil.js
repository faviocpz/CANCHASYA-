document.addEventListener('DOMContentLoaded', () => {
  // Botón para abrir modal nuevo intento
  const btnNuevoIntento = document.getElementById('btn_nuevo_intento');
  if (btnNuevoIntento) {
    btnNuevoIntento.addEventListener('click', function() {
      const modalElement = document.getElementById('modalFoto');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }

      // Limpiar input y vista previa
      const fotoPerfilInput = document.getElementById('foto_perfil');
      const fotoPreviaImg = document.getElementById('foto_previa');
      if (fotoPerfilInput) fotoPerfilInput.value = '';
      if (fotoPreviaImg) {
        fotoPreviaImg.style.display = 'none';
        fotoPreviaImg.src = '';
      }
    });
  }

  // Función para vista previa de imagen
  window.previewImage = function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
      const preview = document.getElementById('foto_previa');
      if (preview) {
        preview.style.display = 'block';
        preview.src = e.target.result;
      }
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  // Enviar formulario de foto
  const formFoto = document.getElementById('form_foto');
  if (formFoto) {
    formFoto.addEventListener('submit', function(event) {
      event.preventDefault();  // Evitar recarga

      const inputFile = document.getElementById('foto_perfil');
      if (!inputFile) {
        alert('Input de foto no encontrado.');
        return;
      }

      if (inputFile.files.length === 0) {
        alert('Por favor selecciona una foto para subir.');
        return;
      }

      const formData = new FormData();
      formData.append('foto_perfil', inputFile.files[0]);

      const correoInput = document.getElementById('correo');
      if (correoInput) {
        formData.append('correo', correoInput.value);
      }

      fetch('/actualizar_foto_verificacion', {
        method: 'POST',
        body: formData,
      })
      .then(response => response.json())
      .then(data => {
        if (data.codigo_rpt === 1) {
          alert('Foto actualizada correctamente.');
          window.location.reload();
        } else {
          alert('Hubo un error al subir la foto.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema con la solicitud.');
      });
    });
  }
});
