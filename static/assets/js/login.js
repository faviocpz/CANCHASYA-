var formulario_deportista = `
    <div class="mb-3">
        <label for="nombres" class="form-label">Apellidos y nombres:</label>
        <input type="text" class="form-control" id="nombres" name="nombres" 
            required 
            pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(\\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+)+$"
            title="Ingresa al menos nombre y apellido, solo letras.">
    </div>
    
    <div class="mb-3">
        <label for="correo" class="form-label">Correo electrónico</label>
        <input type="email" class="form-control" id="correo" name="correo" 
            placeholder="usuario@correo.com" required>
    </div>
    
    <div class="mb-3">
        <label for="celular" class="form-label">Número celular</label>
        <input type="text" class="form-control" id="celular" name="celular" 
            required 
            pattern="^9\\d{8}$" 
            title="Debe contener 9 dígitos y empezar con 9.">
    </div>

    <div class="mb-3">
        <label for="dni" class="form-label">Número de DNI</label>
        <input type="text" class="form-control" id="dni" name="dni" 
            required 
            pattern="^\\d{8}$" 
            title="El DNI debe contener exactamente 8 dígitos.">
    </div>
    
    <div class="mb-3">
        <label for="clave" class="form-label">Contraseña</label>
        <input type="password" class="form-control" id="clave" name="password" 
            placeholder="********" required minlength="6"
            title="La contraseña debe tener al menos 6 caracteres.">
    </div>
    
    <div class="d-grid gap-2">
        <button type="submit" class="btn bg-verdecy text-blancocy fw-bold" onclick="enviar(event)">Registrar</button>
    </div>
`;


var formulario_alquiler = `
    <div class="mb-3">
      <label for="nombre" class="form-label">Nombre completo:</label>
      <input type="text" name="nombres" class="form-control" id="nombre" 
        required 
        pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(\\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+)+$"
        title="Ingresa al menos nombre y apellido, solo letras.">
    </div>

    <div class="mb-3 row">
      <div class="col-6">
        <label for="dni" class="form-label">Número de DNI:</label>
        <input type="text" name="dni" class="form-control" id="dni" 
          required 
          pattern="^\\d{8}$" 
          title="El DNI debe tener exactamente 8 dígitos.">
      </div>
      <div class="col-6">
        <label for="telefono" class="form-label">Teléfono:</label>
        <input type="text" name="telefono" class="form-control" id="telefono" 
          required 
          pattern="^9\\d{8}$" 
          title="El número debe comenzar con 9 y tener 9 dígitos.">
      </div>
    </div>

    <div class="mb-3 row">
      <div class="col-6">
        <label for="correo" class="form-label">Correo electrónico:</label>
        <input type="email" name="correo" class="form-control" id="correo" 
          placeholder="usuario@correo.com" required>
      </div>
      <div class="col-6">
        <label for="password" class="form-label">Contraseña:</label>
        <input type="password" name="password" class="form-control" id="password" 
          required minlength="6"
          title="La contraseña debe tener al menos 6 caracteres.">
      </div>
    </div>

    <div class="mb-3">
      <label for="foto" class="form-label">Sube tu Foto:</label>
      <div class="d-flex">
        <input type="file" name="foto_r" class="form-control me-2" id="foto" 
          accept="image/*" required>
        <button onclick="mostrar_imagen(this)" type="button" class="btn btn-success">
          <i class="bi bi-eye-fill"></i>
        </button>
      </div>
    </div>

    <div class="d-grid gap-2">
      <button type="submit" class="btn bg-verdecy text-blancocy fw-bold">Registrar</button>
    </div>
`;


var formulario_registro = document.getElementById('formulario_registro');


window.onload = function () {
    document.getElementById('ch_deporte').checked = true;
    var formulario_registro = document.getElementById('formulario_registro');
    formulario_registro.innerHTML = formulario_deportista;
};

var inputs_l = document.getElementsByClassName('input_registro');

Array.from(inputs_l).forEach(input => {
    input.addEventListener('click', function () {
        mostrar_formulario(this);
    });
});

function mostrar_formulario(elemento) {
    if (elemento.value === "aliado") {
        formulario_registro.innerHTML = formulario_alquiler;
    } else {
        formulario_registro.innerHTML = formulario_deportista;
    }
}

var modal = new bootstrap.Modal(document.getElementById('imageModal'));
function mostrar_imagen(imagen) {
    var foto_input = document.getElementById('foto');
    var imagen = document.getElementById('img');
    var file = foto_input.files[0];
    if (file) {
        imagen_url = URL.createObjectURL(file);
        imagen.src = imagen_url;
    } else {
        return;
    }

    modal.show();
}



async function iniciar_sesion() {
    const radio_seleccionado = document.querySelector('input[name="tipo_usuario"]:checked').value;
    var form_data = new FormData(document.getElementById('frm_iniciosesion'));
    form_data.append('tipo', radio_seleccionado);
    try {
        const response = await fetch('/inicio_sesion', {
            method: "POST",
            body: form_data
        });
        const data = await response.json();
        console.log(data);
        if (data.codigo == 1) {
            location.href = data.ruta;
        } else {
            alert("Error verifique su contraseña o correo");
        }
    } catch {
        console.log("No hay conexión");
    }

}


function toastifyMsj(texto, colorFondo = "#28a745") {
    Toastify({
        text: texto,
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: colorFondo,
        stopOnFocus: true,
    }).showToast();
}

async function enviar(event) {
    event.preventDefault();

    var form = document.getElementById('formulario_registro');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const radio_seleccionado = document.querySelector('input[name="tipo_usuario"]:checked')?.value;

    if (!radio_seleccionado) {
        toastifyMsj("Selecciona un tipo de usuario", "#dc3545");
        return;
    }

    var form_data = new FormData(form);

    console.log(radio_seleccionado);

    if (radio_seleccionado === 'deportista') {
        const response = await fetch('/registrar_deportista', {
            method: "POST",
            body: form_data
        });
        const data = await response.json();

        if (data.codigo_rpt === 1) {
            toastifyMsj("✅ Registro exitoso. Redirigiendo al login...");
            setTimeout(() => {
                location.href = "/login";
            }, 2000);
        } else if (data.codigo_rpt === 0) {
            const duplicados = data.campos_duplicados.join(" y ");
            toastifyMsj(`❌ Ya existe ${duplicados}`, "#dc3545");
        } else {
            toastifyMsj("❌ Error al registrar usuario", "#dc3545");
        }

    } else {
        try {
            const response = await fetch('/registrar_alquilador', {
                method: "POST",
                body: form_data
            });

            const data = await response.json();
            console.log(data);

            if (data.codigo_rpt == 1) {
                toastifyMsj("✅ Registro exitoso. Redirigiendo al login...");
                setTimeout(() => {
                    location.href = "/login";
                }, 2000);
            } else if (data.codigo_rpt == 2) {
                const rpt = data.rpt_duplicados;

                let mensajes = rpt.map(campo => {
                    switch (campo) {
                        case 'correo': return 'el correo';
                        case 'dni': return 'el DNI';
                        case 'telefono': return 'el teléfono';
                        default: return campo;
                    }
                });

                let mensajeFinal = "❌ " + mensajes.join(" y ") + " ya existen";
                toastifyMsj(mensajeFinal, "#dc3545");

            } else {
                toastifyMsj("❌ Error al registrar. Intenta nuevamente.", "#dc3545");
            }
        } catch (error) {
            console.error(error);
            toastifyMsj("❌ Error inesperado. Revisa la consola.", "#dc3545");
        }

    }
}



function vercontraseña() {
    var clave = document.getElementById('clave');
    var icon = document.getElementById('icon_ver');
    if (clave.type === "password") {
        clave.type = "text";
        if (icon.classList.contains('bi-eye')) {
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        }
    } else {
        clave.type = "password";
        if (icon.classList.contains('bi-eye-slash')) {
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    }
}
