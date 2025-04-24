var botones_menu = document.getElementsByClassName('btn_estilo_hover');

Array.from(botones_menu).forEach(botones => {
    botones.addEventListener('click', function(){
        mostrar_submenus(this.parentElement);
    } )
});

function mostrar_submenus(elemento){
    var submenus = elemento.getElementsByClassName('submenus')[0];

    if(!submenus.classList.contains('d-none')){
        submenus.classList.add('d-none');
    }else{
        submenus.classList.remove('d-none');
    }
}


function salir(){
    location.href = "/";
}