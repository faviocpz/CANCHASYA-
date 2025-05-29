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


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function setupInlineEdit(prefix, validateFn, alertMsg) {
  const editBtn = document.getElementById(`edit-${prefix}-btn`);
  const saveBtn = document.getElementById(`save-${prefix}-btn`);
  const cancelBtn = document.getElementById(`cancel-${prefix}-btn`);
  const textElem = document.getElementById(`${prefix}-text`);
  const inputElem = document.getElementById(`${prefix}-input`);

  editBtn.addEventListener("click", () => {
    editBtn.classList.add("d-none");
    saveBtn.classList.remove("d-none");
    cancelBtn.classList.remove("d-none");
    textElem.classList.add("d-none");
    inputElem.classList.remove("d-none");
    inputElem.value = textElem.textContent.trim();
    inputElem.focus();
  });

  cancelBtn.addEventListener("click", () => {
    inputElem.value = textElem.textContent.trim();
    editBtn.classList.remove("d-none");
    saveBtn.classList.add("d-none");
    cancelBtn.classList.add("d-none");
    textElem.classList.remove("d-none");
    inputElem.classList.add("d-none");
  });

  saveBtn.addEventListener("click", () => {
    const newValue = inputElem.value.trim();
    if (validateFn && !validateFn(newValue)) {
      alert(alertMsg || `Valor inválido para ${prefix}`);
      return;
    }

    fetch("/api/perfil/editar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrf_token"), // si usas CSRF, si no elimina esta línea
      },
      body: JSON.stringify({
        campo: prefix,
        valor: newValue,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          textElem.textContent = newValue;
          cancelBtn.click();
        } else {
          alert("Error al guardar: " + (data.error || "Error desconocido"));
        }
      })
      .catch(() => alert("Error en la conexión al servidor."));
  });

  inputElem.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      saveBtn.click();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupInlineEdit(
    "nombre",
    (val) => val.length >= 3 && val.length <= 100,
    "El nombre debe tener entre 3 y 100 caracteres."
  );
  setupInlineEdit(
    "correo",
    (val) =>
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) && val.length >= 5 && val.length <= 100,
    "Ingrese un correo electrónico válido."
  );
  setupInlineEdit(
    "telefono",
    (val) => /^[0-9]{9}$/.test(val),
    "El teléfono debe tener 9 dígitos numéricos."
  );
});


