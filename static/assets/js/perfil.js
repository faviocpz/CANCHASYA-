document.getElementById('btn_nuevo_intento').addEventListener('click', function() {
  const modal = new bootstrap.Modal(document.getElementById('modalFoto'));
  modal.show();

  // Limpiar el input y la imagen de vista previa cuando se abre el modal
  document.getElementById('foto_perfil').value = ''; 
  document.getElementById('foto_previa').style.display = 'none';
  document.getElementById('foto_previa').src = '';
});

function previewImage(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const preview = document.getElementById('foto_previa');
    preview.style.display = 'block';
    preview.src = e.target.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  }
}

// Al hacer clic en el botón "Enviar", enviamos la foto al servidor
document.getElementById('form_foto').addEventListener('submit', function(event) {
  event.preventDefault();  // Prevenir el comportamiento por defecto del formulario (que hace un POST y recarga la página automáticamente)

  const inputFile = document.getElementById('foto_perfil');
  const formData = new FormData();

  // Verificar si hay un archivo seleccionado
  if (inputFile.files.length > 0) {
    formData.append('foto_perfil', inputFile.files[0]);  // Agregar archivo al FormData
    formData.append('correo', document.getElementById('correo').value);  // Agregar correo al FormData

    // Enviar solicitud al servidor para actualizar la foto
    fetch('/actualizar_foto_verificacion', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.codigo_rpt === 1) {
        // Foto subida correctamente
        alert('Foto actualizada correctamente.');

        // Recargar la página para ver los cambios reflejados
        window.location.reload();
      } else {
        alert('Hubo un error al subir la foto.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Hubo un problema con la solicitud.');
    });
  } else {
    alert('Por favor selecciona una foto para subir.');
  }
});
