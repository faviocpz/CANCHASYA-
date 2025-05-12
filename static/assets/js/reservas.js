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
const boton_agregarR = `<button class="btn btn-success w-100" > Agregar Reserva </button>`
const id_rs = document.getElementById('id_rs');

async function  abrir_nodal(button, cancha){
    id_rs.value = '';
    spanCancha.textContent = cancha;
    spanHorario.textContent = button.textContent;

    if (button.classList.contains('btn-danger')) {
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