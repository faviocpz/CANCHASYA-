console.log('interna.js cargado');

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');

  function updateToggleVisibility() {
    if (window.innerWidth <= 991.98) {
      if (sidebar.classList.contains('show')) {
        toggleBtn.style.display = 'none';  
      } else {
        toggleBtn.style.display = 'block'; 
      }
    } else {
      toggleBtn.style.display = 'none'; 
    }
  }

  if (!toggleBtn || !sidebar || !mainContent) {
    console.error('No se encontraron elementos necesarios para el toggle de sidebar.');
    return;
  }

  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
    updateToggleVisibility();
  });

  mainContent.addEventListener('click', () => {
    if (window.innerWidth <= 991.98 && sidebar.classList.contains('show')) {
      sidebar.classList.remove('show');
      updateToggleVisibility();
    }
  });

  sidebar.querySelectorAll('a.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 991.98 && sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
        updateToggleVisibility();
      }
    });
  });

  window.addEventListener('resize', updateToggleVisibility);

  updateToggleVisibility();
});
