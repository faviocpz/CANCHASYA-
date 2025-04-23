document.addEventListener("DOMContentLoaded", function () {
    fetch("/obtener_perfil_usuario")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.codigo === 1) {
          const user = data.usuario;
          document.getElementById("nombre").value = user.nombre;
          document.getElementById("dni").value = user.dni;
          document.getElementById("correo").value = user.correo;
          document.getElementById("telefono").value = user.telefono;
  
          if (user.idTipoUsuario == 2) {
            const zonaVerificacion = document.getElementById("estado_verificacion");
            if (user.verificacion_cuenta === "R") {
              zonaVerificacion.innerHTML = `
                <div class="alert alert-danger d-flex justify-content-between align-items-center">
                  <span><i class="bi bi-exclamation-triangle me-2"></i> Foto rechazada</span>
                  <button class="btn btn-outline-danger btn-sm">Nuevo intento</button>
                </div>`;
            } else if (user.verificacion_cuenta === "E") {
              zonaVerificacion.innerHTML = `
                <div class="alert alert-warning">
                  <i class="bi bi-hourglass-split me-2"></i> Aprobación pendiente
                </div>`;
            } else if (user.verificacion_cuenta === "V") {
              zonaVerificacion.innerHTML = `
                <div class="alert alert-success">
                  <i class="bi bi-check-circle me-2"></i> Aliado autorizado
                </div>`;
            }
          }
        }
      });
  });
  