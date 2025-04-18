var formulario_deportista = `
    <div class="mb-3">
        <label for="correo" class="form-label">Apellidos y nombres: </label>
        <input type="text" class="form-control" id="nombres" required>
    </div>
    <div class="mb-3">
        <label for="correo" class="form-label">Correo electrónico</label>
        <input type="email" class="form-control" id="correo" placeholder="usuario@correo.com" required>
    </div>
    <div class="mb-3">
        <label for="clave" class="form-label">Contraseña</label>
        <input type="password" class="form-control" id="clave" placeholder="********" required>
    </div>
    <div class="d-grid gap-2">
        <button type="submit" class="btn bg-verdecy text-blancocy fw-bold" onclick="enviar()">Registrar</button>
    </div>
`;

var formulario_alquiler = `

    <div class="mb-3">
        <label for="nombre" class="form-label">Nombre completo:</label>
        <input type="text" name="nombres" class="form-control" id="nombre" required>
    </div>
    <div class="mb-3">
        <label for="dni" class="form-label">Número de DNI:</label>
        <input type="text" name="dni" class="form-control" id="dni" required>
    </div>
    <div class="mb-3">
        <label for="correo" class="form-label">Correo electrónico:</label>
        <input type="email" name="correo" class="form-control" id="correo" placeholder="usuario@correo.com" required>
    </div>
    <div class="mb-3">
        <label for="tel" class="form-label">Teléfono:</label>
        <input type="text" name="tel" class="form-control" id="tel" required>
    </div>
    <div class="mb-3">
        <label for="password" class="form-label">Contraseña:</label>
        <input type="password" name="password" class="form-control" id="password" required>
    </div>
    <div class="mb-3">
        <label for="foto" class="form-label">Sube tu Foto:</label>
        <div class="d-flex">
            <input type="file" name="foto_r" class="form-control me-2" id="foto" accept="image/*" required>
            <button onclick="mostrar_imagen(this)"  type="button" class="btn btn-success"><i class="bi bi-eye-fill"></i> </button>
        </div>
    </div>
    <div class="d-grid gap-2">
        <button type="button" class="btn bg-verdecy text-blancocy fw-bold" onclick="enviar()">Registrar</button>
    </div>
`;

var formulario_registro = document.getElementById('formulario_registro');


window.onload = function() {
    document.getElementById('ch_deporte').checked = true;
    var formulario_registro = document.getElementById('formulario_registro');
    formulario_registro.innerHTML = formulario_deportista;
};

var inputs_l = document.getElementsByClassName('input_registro');

Array.from(inputs_l).forEach(input => {
    input.addEventListener('click', function() {
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
function mostrar_imagen(imagen){
    var foto_input = document.getElementById('foto');
    var imagen = document.getElementById('img');
    var file = foto_input.files[0];
    if(file){
        imagen_url = URL.createObjectURL(file);
        imagen.src = imagen_url;
    }else{
        return;
    }

    modal.show();
}


async function enviar(){
    const radio_seleccionado = document.querySelector('input[name="tipo_usuario"]:checked').value;
    var form_data = new FormData(document.getElementById('formulario_registro'));

    if (radio_seleccionado === 'deportista') {
        
    } else {
        try{
            const response = await fetch('/registrar_alquilador',{
                method:"POST",
                body: form_data 
            });
            const data = await response.json();
            console.log(data);
            if(data.codigo_rpt == 1){
                location.href = "/maestra_interna";
            }else{
                const rpt_duplicados = data.rpt_duplicados;

                if(rpt_duplicados.length > 0){
                    alert('el correo y dni ya existe');
                }else{
                    if (rpt_duplicados[0] == 'correo' || rpt_duplicados[1] == 'correo' ){
                        alert('el correo ya existe');
                    }else{
                        alert('el dni ya existe');
                    }
                }
            }
        }catch {
            alert("No hay conexión");
        }
    }
}



async function iniciar_sesion(){
    const radio_seleccionado = document.querySelector('input[name="tipo_usuario"]:checked').value;
    var form_data = new FormData(document.getElementById('frm_iniciosesion'));
    form_data.append('tipo', radio_seleccionado);
    try{
        const response = await fetch('/inicio_sesion',{
            method:"POST",
            body: form_data 
        });
        const data = await response.json();
        console.log(data);
        if(data.codigo == 1){
            location.href = data.ruta;
        }else {
            alert("Error verifique su contraseña o correo");
        }
    }catch {
        console.log("No hay conexión");
    }
    
}