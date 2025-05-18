const minimoSelect = document.getElementById('hora_fin_select');
const maximoSelect = document.getElementById('hora_inicio_select');

const min = minimoSelect.options[0].value;
const maximo = maximoSelect.options[minimoSelect.options.length - 1].value;


pintar_horario(datos_canchas);
async function pintar_horario(datos_canchas){

    Array.from(datos_canchas).forEach(element => {
        const reservado = element.reservas;
        let horas = document.getElementById(element.id_cancha);
        let botones = horas.querySelectorAll('.horas');
        let id = 0;
        let id_r = 0;
        botones.forEach(btn => {
            const verifica = reservado.some(hora_r => {
                if(hora_r.hr.startsWith(btn.dataset.inicio)){
                    id = hora_r.id;
                    id_r = hora_r.id_reserva;
                    return true;
                }
                return false;
            });
            if(verifica){
                btn.classList.remove('btn-success');
                btn.classList.add('btn-danger');
                btn.dataset.idjugador = id;
                btn.dataset.idresrva = id_r;
            }
    
        });
    });
}
var myModal = new bootstrap.Modal(document.getElementById('modal_detalle'));
const spanCancha = document.getElementById('detalle_cancha');
const spanHorario = document.getElementById('detalle_hora');
const spanEstado = document.getElementById('detalle_estado');
const footmodal = document.getElementById('foot_modal');
const spanCliente = document.getElementById('detalle_cliente');
const boton_eliminarR = `<button class="btn btn-danger w-100" onclick="eliminar_reserva()"> Eliminar Reserva </button>`
const boton_agregarR = `<button class="btn btn-success w-100" disabled id="btn_rese" onclick="agregar_reserva()"> Agregar Reserva </button>`
const id_rs = document.getElementById('id_rs');
const id_cancha = document.getElementById('id_cancha');

async function  abrir_nodal(button, cancha, cancha_id){
    document.getElementById('numero_dni').value = "";
    id_rs.value = '';
    id_cancha.value = cancha_id;
    spanCancha.textContent = cancha;
    spanHorario.textContent = button.textContent;
    if (button.classList.contains('btn-danger')) {
        document.getElementById('frm_usu').classList.add('d-none');
        let id_jugador = button.dataset.idjugador;
        let id_reserv = button.dataset.idresrva;
        spanEstado.textContent = "Reservado";
        if(spanEstado.classList.contains('bg-success')){
            spanEstado.classList.remove('bg-success');
        }
        spanEstado.classList.add('badge','bg-danger');
        footmodal.innerHTML = boton_eliminarR;

        let datos = await fetch(`/datos_clientejugador/${id_jugador}`);
        let response = await datos.json()

        if(response.status == 1){
            let jugador = response.valor[0]; 
            spanCliente.innerHTML = `
                <strong>Nombre:</strong> ${jugador.nombre} <br>
                <strong>Correo:</strong> ${jugador.correo} <br>
                <strong>Teléfono:</strong> ${jugador.telefono}
            `;
            id_rs.value = id_reserv;
        }else{
            spanCliente.innerHTML = '<strong>Nombre:</strong> Anónimo <br>';
        }
    }else{
        document.getElementById('frm_usu').classList.remove('d-none');

        footmodal.innerHTML = boton_agregarR;
        spanEstado.textContent = "Libre";
        if(spanEstado.classList.contains('bg-danger')){
            spanEstado.classList.remove('bg-danger');
        }
        spanEstado.classList.add('badge', 'bg-success');
        spanCliente.innerHTML = '<strong>Nombre:</strong> Anónimo <br>';

    }

    myModal.show();
}


async function eliminar_reserva(){
    const id = id_rs.value;
    const ch = document.getElementById('id_cancha').value;
    const botones = document.getElementById(ch).querySelectorAll('.horas');
    const hr = document.getElementById('detalle_hora').textContent.split('-')[0].trim();
    const boton_r = document.getElementById('modal_detalle').querySelector('.btn-danger');

    try{
        boton_r.disabled = true;
        boton_r.innerHTML = `  <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Eliminando reserva...`;
        const response = await fetch(`/eliminar_reserva/${id}`);
        const data = await response.json();
        if(data.status == 1){
            botones.forEach(boton => {
                if (boton.dataset.inicio == hr) {
                    boton.classList.add('btn-success');
                    boton.classList.remove('btn-danger');
                }
            });
            mensajeOK('Reserva eliminada con éxito');
            myModal.hide();
        }else{
            mensajeNOT('La reserva no se pudo eliminar');
            boton_r.innerHTML = "Eliminar Reserva";
        }
    }catch{
            mensajeNOT('La reserva no se pudo eliminar');
    }finally{
        boton_r.disabled = false;
    }
}


async function verificar_usuariodni(){
    let dni_e  = document.getElementById('numero_dni').value;
    let  id_j = document.getElementById('id_rs');
    id_j.value = "";

    try {
        const response = await fetch(`/verificar_usuarioDni/${dni_e}`);
        const datos = await response.json();
        if(datos.codigo == 1){
            let jugador = datos.datos;
            console.log(jugador);
            spanCliente.innerHTML = `
                <strong>Nombre:</strong> ${jugador.nombre} <br>
                <strong>Correo:</strong> ${jugador.correo} <br>
                <strong>Teléfono:</strong> ${jugador.telefono}
            `;
            id_j.value = jugador.id;
            document.getElementById('btn_rese').disabled = false;
        }else{
            document.getElementById('btn_rese').disabled = true;
            spanCliente.innerHTML = '<strong>Nombre:</strong> Anónimo <br>'; 
        }
    } catch (error) {
        console.error('Error al hacer fetch:', error);
    }

}

document.getElementById('numero_dni').addEventListener('input', function() {
    let valor = document.getElementById('numero_dni').value;
    const btn = document.getElementById('btn_search');
    const btn_a = document.getElementById('btn_rese');
    btn.disabled = valor.length !== 8;
    btn_a.disabled = true;
    document.getElementById('detalle_cliente').textContent = "";
});



async function agregar_reserva(){
    const id_usuario = document.getElementById('id_rs').value;
    const detalle_hora = document.getElementById('detalle_hora').textContent.trim();
    const fecha = document.getElementById('fecha_actual').value;
    const boton_r = document.getElementById('modal_detalle').querySelector('.btn-success');
    const data_idjugador = 1;
    const data_idresrva = 1;
    const datos = {
        'id_usuario': id_usuario,
        'hora_inicio': detalle_hora.split('-')[0].trim(),
        'hora_fin': detalle_hora.split('-')[1].trim(),
        'fecha': fecha,
        'id_cancha': document.getElementById('id_cancha').value
    }
    try{
        if(id_usuario && detalle_hora){
            boton_r.disabled = true;
            boton_r.innerHTML = `    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Agregando reserva...`;
            const response = await fetch('/alquiler_cancha', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            });

            const resultado = await response.json();
            if(resultado.status == 1){
                datos_fecha_nueva('si');
                mensajeOK("Reserva registrada exitosamente!");
                myModal.hide();
            }else{
                boton_agregarR.innerHTML = `Agregar Reserva`
                mensajeNOT("No se pudo registrar correctamente la reserva!");            
            }
        }else{
            console.log("Verifique los datos del usuario");
        }
    }finally{
        boton_r.disabled = false;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const horaInicioSelect = document.getElementById('hora_inicio_select');
    const horaFinSelect = document.getElementById('hora_fin_select');

    function actualizarOpcionesFin() {
        const horaInicio = parseInt(horaInicioSelect.value);
        
        if (isNaN(horaInicio)) {            
            horaFinSelect.querySelectorAll('option').forEach(option => {
                if (option.value !== "") option.style.display = '';
            });
            return;
        }

        horaFinSelect.querySelectorAll('option').forEach(option => {
            if (option.value !== "") {
                const horaOption = parseInt(option.value);
                option.style.display = horaOption > horaInicio ? '' : 'none';
            }
        });

        if (parseInt(horaFinSelect.value) <= horaInicio) {
            horaFinSelect.value = "";
        }
    }
    
    function actualizarOpcionesInicio() {
        const horaFin = parseInt(horaFinSelect.value);
        
        if (isNaN(horaFin)) {
            horaInicioSelect.querySelectorAll('option').forEach(option => {
                if (option.value !== "") option.style.display = '';
            });
            return;
        }

        horaInicioSelect.querySelectorAll('option').forEach(option => {
            if (option.value !== "") {
                const horaOption = parseInt(option.value);
                option.style.display = horaOption < horaFin ? '' : 'none';
            }
        });

        if (parseInt(horaInicioSelect.value) >= horaFin) {
            horaInicioSelect.value = "";
        }
    }

    horaInicioSelect.addEventListener('change', actualizarOpcionesFin);
    horaFinSelect.addEventListener('change', actualizarOpcionesInicio);

    actualizarOpcionesFin();
    actualizarOpcionesInicio();
});



function filtrar(){
    const filtro_e = document.getElementById('filtro_e').value;
    const filtro_hi = parseInt(document.getElementById('hora_inicio_select').value);
    const filtro_hf = parseInt(document.getElementById('hora_fin_select').value);
    const body = document.querySelectorAll('.listas_canchas');

    Array.from(body).forEach(element => {
        let hr = element.querySelectorAll('.horarios_cc .horas');
        Array.from(hr).forEach((button) => {
            const hora_inicio = parseInt(button.textContent.split('-')[0].slice().split(':')[0]);
            const hor_fin = parseInt(button.textContent.split('-')[1].slice().split(':')[0]);
            const estado = button.classList.contains('btn-success');

            if(filtro_e == 'A'){
                console.log(estado);
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == true){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }else if(filtro_e == 'I'){
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == false){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }           
            }else{
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }

        })

    });
}


document.getElementById('fecha_actual').addEventListener('change', function () {
    let h_ini = document.getElementById('hora_inicio_select');
    let f_fin = document.getElementById('hora_fin_select');
    document.getElementById('filtro_e').value = "T";
    Array.from(h_ini.options).forEach(option => {
        if (option.style.display === "none") {
            option.style.display = "";
        }
    });

    Array.from(f_fin.options).forEach(option => {
        if (option.style.display === "none") {
            option.style.display = "";
        }
    });
    
    //h_ini.value = min;
    //f_fin.value = maximo;
    datos_fecha_nueva();
});

const load = document.querySelector('.loader');

async function datos_fecha_nueva(estado) {
    if(!estado){
        load.classList.remove('d-none');
    }
    
    try {
        const fecha = document.getElementById('fecha_actual').value;
        const response = await fetch(`/pagina_reservasfiltro/${fecha}`);
        const data = await response.json();

        if (data.status === 1) {
            renderCanchas(data.data, data.horario);
            pintar_horario(data.data);
            filtrar();
        } else {
            document.querySelector('.listas_canchas').innerHTML = "<p class='text-danger'>No hay canchas disponibles.</p>";
        }
    } finally {
        load.classList.add('d-none');
    }
}

async function renderCanchas(canchas, horarios) {
    const contenedor = document.querySelector('.listas_canchas');
    contenedor.innerHTML = '';

    canchas.forEach(cancha => {
        const div = document.createElement('div');
        div.classList.add('row');
        div.id = cancha.id_cancha;

        div.innerHTML = `
            <div class="col-2 text-center">
                <input type="text" value="${cancha.id_cancha}" class="d-none">
                <span class="fw-bold text-primary">${cancha.nombre}</span>
            </div>
            <div class="col-10 horarios_cc">
                ${horarios.map(h => `
                    <button class="btn btn-success m-1 horas"
                        data-inicio="${h.hora_inicio}"
                        onclick="abrir_nodal(this, '${cancha.nombre}', '${cancha.id_cancha}')">
                        ${h.hora_inicio} - ${h.hora_fin}
                    </button>
                `).join('')}
            </div>
        `;
        contenedor.appendChild(div);
    });
}

document.getElementById('filtro_e').addEventListener('change', function(){
const filtro_e = document.getElementById('filtro_e').value;
    const filtro_hi = parseInt(document.getElementById('hora_inicio_select').value);
    const filtro_hf = parseInt(document.getElementById('hora_fin_select').value);
    const body = document.querySelectorAll('.listas_canchas');

    Array.from(body).forEach(element => {
        let hr = element.querySelectorAll('.horarios_cc .horas');
        Array.from(hr).forEach((button) => {
            const hora_inicio = parseInt(button.textContent.split('-')[0].slice().split(':')[0]);
            const hor_fin = parseInt(button.textContent.split('-')[1].slice().split(':')[0]);
            const estado = button.classList.contains('btn-success');

            if(filtro_e == 'A'){
                console.log(estado);
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == true){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }else if(filtro_e == 'I'){
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == false){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }           
            }else{
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }

        })

    });
});

document.getElementById('hora_inicio_select').addEventListener('change', function() {
    const filtro_e = document.getElementById('filtro_e').value;
    const filtro_hi = parseInt(document.getElementById('hora_inicio_select').value);
    const filtro_hf = parseInt(document.getElementById('hora_fin_select').value);
    const body = document.querySelectorAll('.listas_canchas');

    Array.from(body).forEach(element => {
        let hr = element.querySelectorAll('.horarios_cc .horas');
        Array.from(hr).forEach((button) => {
            const hora_inicio = parseInt(button.textContent.split('-')[0].slice().split(':')[0]);
            const hor_fin = parseInt(button.textContent.split('-')[1].slice().split(':')[0]);
            const estado = button.classList.contains('btn-success');

            if(filtro_e == 'A'){
                console.log(estado);
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == true){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }else if(filtro_e == 'I'){
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == false){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }           
            }else{
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }

        })

    });
});

document.getElementById('hora_fin_select').addEventListener('change', function() {
    const filtro_e = document.getElementById('filtro_e').value;
    const filtro_hi = parseInt(document.getElementById('hora_inicio_select').value);
    const filtro_hf = parseInt(document.getElementById('hora_fin_select').value);
    const body = document.querySelectorAll('.listas_canchas');

    Array.from(body).forEach(element => {
        let hr = element.querySelectorAll('.horarios_cc .horas');
        Array.from(hr).forEach((button) => {
            const hora_inicio = parseInt(button.textContent.split('-')[0].slice().split(':')[0]);
            const hor_fin = parseInt(button.textContent.split('-')[1].slice().split(':')[0]);
            const estado = button.classList.contains('btn-success');

            if(filtro_e == 'A'){
                console.log(estado);
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == true){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }else if(filtro_e == 'I'){
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf && estado == false){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }           
            }else{
                if(hora_inicio >= filtro_hi && hor_fin <= filtro_hf){
                    button.classList.contains('d-none') ? button.classList.remove('d-none'): 1;
                }else{
                    button.classList.contains('d-none') ? 1: button.classList.add('d-none');
                }
            }

        })

    });
});



function mensajeOK(mensaje) {
    Toastify({
        text: mensaje,
        duration: 2000, // 2 segundos
        close: true,
        gravity: "bottom",
        position: "right",
        backgroundColor: "#28a745", // Verde Bootstrap
        stopOnFocus: true,
    }).showToast();
}

function mensajeNOT(mensaje) {
    Toastify({
        text: mensaje,
        duration: 2000, // 2 segundos
        close: true,
        gravity: "bottom",
        position: "right",
        backgroundColor: "#dc3545", // Rojo Bootstrap
        stopOnFocus: true,
    }).showToast();
}
