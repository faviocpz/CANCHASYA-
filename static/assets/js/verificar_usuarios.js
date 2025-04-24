var modal = new bootstrap.Modal(document.getElementById('modal_verificacion'));

function mostrar_modal(url_foto, dni, id,nombre_user, correo){
    const basePath = '/static/assets/img_usuario/alquilador';
    document.getElementById('foto_usuario').src = `${basePath}/${id}/verificar_img_${url_foto}`;
    document.getElementById('nombre_user').value = nombre_user;
    document.getElementById('dni_usuario').value = dni;

    var btn_fotor = document.getElementById('foto_r');
    var btn_aceptar = document.getElementById('foto_v');
    btn_fotor.onclick = function() {
        var asunto = 'Imagen no válida';
        var cuerpo = 'Estimado usuario, la imagen proporcionada está borrosa o no cumple con los requisitos. Por favor, cargue una nueva imagen clara y legible para continuar con el proceso de verificación.';
        mensaje_email(asunto, correo, cuerpo);
        cambiar_estado('R', id);
    };
    
    btn_aceptar.onclick = function() {
        var asunto = 'Cuenta verificada';
        var cuerpo = 'Estimado usuario, su cuenta ha sido verificada';
        mensaje_email(asunto, correo, cuerpo);
        cambiar_estado('V', id);
    };
    
    modal.show();
}

async function mensaje_email(asunto, email, cuerpo){
    try {
        const response = await fetch('/enviar_correo', {
            method: "POST",
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
            asunto_f: asunto,
            email_f: email,
            cuerpo_f: cuerpo
            })
        });
        const data = await response.json();

        if(data.codigo == 1){
            alert("Se envio correctamente");
        }else{
            alert("No se pudo enviar el correo");
        }
    } catch (error) {
        alert("No se pudo enviar el correo");
    }
}


async function cambiar_estado(estado, id){
    try {
        const response = await fetch(`/cambiar_estado_usuario/${estado}/${id}`)
        const data = await response.json();

        if(data.codigo == 1){
            alert('Estado del usuario actualizado');
            
            // Actualizar la fila correspondiente de la tabla sin recargarla
            actualizar_fila_estado(id, estado);
        } else {
            alert('No se pudo cambiar el estado');
        }
    } catch (error) {
        alert('No se pudo cambiar el estado');
    }
    modal.hide();  // Cerrar el modal después de actualizar el estado
}

function actualizar_fila_estado(id, estado) {
    const tbody = document.getElementById('datos_solicitud');
    const filas = tbody.rows;

    for (let fila of filas) {
        const tdId = fila.cells[0].textContent;  // Obtener el ID desde la primera celda de cada fila
        if (tdId == id) {
            // Obtener la celda de estado y actualizar su valor
            const tdEstado = fila.cells[4];
            const btnVerificar = fila.querySelector("button"); // Obtener el botón de verificar
            
            if (estado === 'R') {
                tdEstado.innerHTML = '<span class="text-danger">Foto rechazada.</span>';
                btnVerificar.disabled = true;  // Deshabilitar el botón de verificar si fue rechazada
            } else if (estado === 'V') {
                tdEstado.innerHTML = '<span class="text-success">Aliado autorizado.</span>';
                btnVerificar.disabled = true;  // Deshabilitar el botón de verificar si fue autorizado
            }
            break;  // Salir del loop una vez que hemos encontrado la fila correcta
        }
    }
}
function buscar(elemento){
    var texto = elemento.value;
    var tbody = document.getElementById('datos_solicitud');
    if (texto.length > 0) {
        Array.from(tbody.rows).forEach(tr => {
            
            if (tr.cells[1].textContent.includes(texto)) {
                tr.classList.remove('d-none');
            } else {
                tr.classList.add('d-none');
            }
        });
    } else {
        Array.from(tbody.rows).forEach(tr => {
            tr.classList.remove('d-none');
        });
    }
}


