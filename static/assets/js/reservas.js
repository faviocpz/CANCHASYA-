pintar_horario();
function pintar_horario(){

    Array.from(datos_canchas).forEach(element => {
        const reservado = element.reservas;

        let horas = document.getElementById(element.id_cancha);
        let botones = horas.querySelectorAll('.horas');
        
        botones.forEach(btn => {
            const verifica = reservado.some(hora_r => hora_r.startsWith(btn.dataset.inicio));
            if(verifica){
                btn.style.backgroundColor = 'red';
            }

        });



    });
}
