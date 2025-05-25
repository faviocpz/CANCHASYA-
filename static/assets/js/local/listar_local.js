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
    inputElem.focus();

    if (prefix === "facebook" || prefix === "instagram") {
      inputElem.value = textElem.getAttribute("data-url") || "";
    } else {
      inputElem.value = textElem.textContent.trim();
    }

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

    fetch("/api/local/editar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrf_token"), // elimina o ajusta si no usas CSRF
      },
      body: JSON.stringify({
        campo: prefix,
        valor: newValue,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          if (prefix === "facebook") {
            textElem.innerHTML = newValue
              ? `<a href="${newValue}" target="_blank" class="text-decoration-none">Ver página</a>`
              : "No disponible";
            textElem.setAttribute("data-url", newValue);
          } else if (prefix === "instagram") {
            textElem.innerHTML = newValue
              ? `<a href="${newValue}" target="_blank" class="text-decoration-none">Ver perfil</a>`
              : "No disponible";
            textElem.setAttribute("data-url", newValue);
          } else {
            textElem.textContent = newValue;
          }
          cancelBtn.click();
        } else {
          alert("Error al guardar: " + (data.error || "Error desconocido"));
        }
      })
      .catch(() => alert("Error en la conexión al servidor."));
  });

  inputElem.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      saveBtn.click();
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  setupInlineEdit(
    "nombre",
    (val) => val.length >= 3 && val.length <= 100,
    "El nombre debe tener entre 3 y 100 caracteres."
  );
  setupInlineEdit(
    "direccion",
    (val) => val.length >= 5 && val.length <= 255,
    "La dirección debe tener entre 5 y 255 caracteres."
  );
  setupInlineEdit(
    "tel",
    (val) => /^[0-9]{9}$/.test(val),
    "El teléfono debe tener 9 dígitos numéricos."
  );
  setupInlineEdit(
    "correo",
    (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val),
    "Ingrese un correo electrónico válido."
  );
  setupInlineEdit(
    "facebook",
    (val) => val === "" || /^https?:\/\/.+$/.test(val),
    "Ingrese una URL válida para Facebook o déjelo vacío."
  );
  setupInlineEdit(
    "instagram",
    (val) => val === "" || /^https?:\/\/.+$/.test(val),
    "Ingrese una URL válida para Instagram o déjelo vacío."
  );
});


function openModal(src) {
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    document.getElementById('modalImage').src = src;
    modal.show();
}

