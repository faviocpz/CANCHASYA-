pintar_horario();
function pintar_horario(){

    Array.from(datos_canchas).forEach(element => {
        console.log(element);
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
        console.log(response);

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


function eliminar_reserva(){
    const id = id_rs.value;
    console.log(id);

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
    const datos = {
        'id_usuario': id_usuario,
        'hora_inicio': detalle_hora.split('-')[0].trim(),
        'hora_fin': detalle_hora.split('-')[1].trim(),
        'fecha': fecha,
        'id_cancha': document.getElementById('id_cancha').value
    }

    if(id_usuario && detalle_hora){
        const response = await fetch('/alquiler_cancha', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();
        console.log(resultado);
        if(resultado.status == 1){
            alert("Reserva registrada correctamente")
            myModal.hide()
        }else{
            boton_agregarR.disabled = false;
            boton_agregarR.innerHTML = `Agregar reserva`

            alert("No se pudo registrar correctamente la reserva")
        }
    }else{
        console.log("Verifique los datos del usuario");
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
    
}