document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');

  // Verificaciones para evitar errores si algún elemento no existe
  if (!toggleBtn || !sidebar || !mainContent) {
    console.error('No se encontraron elementos necesarios para el toggle de sidebar.');
    return;
  }

  // Al hacer clic en el botón toggle, se agrega/quita la clase "show" para abrir/cerrar el sidebar
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
  });

  // Al hacer clic en el área principal, si estamos en móvil y el sidebar está abierto, se cierra
  mainContent.addEventListener('click', () => {
    if (window.innerWidth <= 991.98 && sidebar.classList.contains('show')) {
      sidebar.classList.remove('show');
    }
  });

  // Al hacer clic en cualquier enlace del sidebar, si estamos en móvil y el sidebar está abierto, se cierra
  sidebar.querySelectorAll('a.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 991.98 && sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
      }
    });
  });
});
