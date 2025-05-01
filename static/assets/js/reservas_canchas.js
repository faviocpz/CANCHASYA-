const tiempo_final = document.getElementById('end_time');

document.getElementById('start_time').addEventListener('change', function() {
    const value = this.value;
    const [hours, minutes] = value.split(":");
    if (parseInt(hours) < 7) {
        alert('La hora mínima permitida es las 7:00 AM');
        this.value = '07:00';
    }
    const duracion = document.getElementById('duration');
    duracion.value = '0';
    tiempo_final.value = '';

    if (duracion.hasAttribute('disabled')) {
        duracion.removeAttribute('disabled');
    }

});

document.getElementById('start_time').addEventListener('click', function() {
    const duracion = document.getElementById('duration');
    if (!duracion.hasAttribute('disabled')) {
        duracion.setAttribute('disabled', 'disabled');
    }
});

function eliminar_reserva(){
    const titulo = document.getElementById('titulo_formulario');
    titulo.textContent = "Eliminar reserva";
}


function reservar(){
    const titulo = document.getElementById('titulo_formulario');
    titulo.textContent = "Reservar cancha";
}


document.getElementById('duration').addEventListener('change', function() {
    const duracion = document.getElementById('duration').value;
    const boton =  document.getElementById('confirmar');

    if(duracion == '0'){
        alert('seleccione una opcion');
        if(!boton.hasAttribute('disabled')){
            boton.setAttribute('disabled', 'disabled');
        }
        tiempo_final.value = '';
    }else{
        if(boton.hasAttribute('disabled')){
            boton.removeAttribute('disabled', 'disabled');
        }
        calcular_hora();
    }
});


function calcular_hora() {
    const time = document.getElementById('start_time').value;
    const duracion = parseFloat(document.getElementById('duration').value);

    const [hours, minutes] = time.split(":").map(Number);

    // Convertir la duración en horas y minutos
    const durationHours = Math.floor(duracion); // Obtener las horas completas
    const durationMinutes = Math.round((duracion % 1) * 60); // Obtener los minutos restantes

    // Calcular la hora final
    const endHours = hours + durationHours;
    const endMinutes = minutes + durationMinutes;

    // Ajustar horas y minutos si es necesario
    const adjustedHours = endHours + Math.floor(endMinutes / 60);
    const adjustedMinutes = endMinutes % 60;

    // Establecer la hora final en el campo de texto
    tiempo_final.value = `${String(adjustedHours).padStart(2, '0')}:${String(adjustedMinutes).padStart(2, '0')}`;
}



function aplicar_accion(){
    const hora_inicio = document.getElementById('start_time').value;
    const hora_fin = document.getElementById('end_time').value;
    const fechas = document.getElementsByClassName('dias');
    const fecha_seleccionada = document.getElementById('date').value;
    dibujar(hora_inicio, hora_fin, fechas, fecha_seleccionada);
}

let indice;
function dibujar(hora_inicio, hora_fin, fechas, fecha_seleccionada){
    const tabla = document.getElementsByClassName('tabla_fecha_hora');
    const [hr_inicio, minuto_inicio] = hora_inicio.split(':');
    const [hr_fin, minuto_fin] = hora_fin.split(':');


    Array.from(fechas).forEach((tr) => {
        let fecha = tr.textContent;
        indice ++;
        if (fecha == fecha_seleccionada){
            console.log(fecha_seleccionada);
            return;
        }
    })

    



}