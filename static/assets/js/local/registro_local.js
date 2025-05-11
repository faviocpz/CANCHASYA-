document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.getElementById('logo');
    const bannerInput = document.getElementById('banner');
    const viewLogoBtn = document.getElementById('viewLogoBtn');
    const viewBannerBtn = document.getElementById('viewBannerBtn');
    const modalPreview = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
    const modalImage = document.getElementById('modalPreviewImage');
    
    function handleFileChange(input, viewBtn) {
        return function(e) {
            if (input.files && input.files[0]) {
                viewBtn.disabled = false;
                        
                viewBtn.onclick = function() {
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        modalImage.src = event.target.result;
                        modalPreview.show();
                    };
                    reader.readAsDataURL(input.files[0]);
                };
            } else {
                viewBtn.disabled = true;
            }
        };
    }

    logoInput.addEventListener('change', handleFileChange(logoInput, viewLogoBtn));
    bannerInput.addEventListener('change', handleFileChange(bannerInput, viewBannerBtn));

    document.querySelector('form').addEventListener('submit', function(e) {
        const logo = logoInput.files[0];
        const banner = bannerInput.files[0];
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        const maxSize = 2 * 1024 * 1024; // 2MB

        if (logo && (!allowedTypes.includes(logo.type) || logo.size > maxSize)) {
            alert('El logo debe ser una imagen (JPEG/PNG/GIF) de menos de 2MB');
            e.preventDefault();
        }

        if (banner && (!allowedTypes.includes(banner.type) || banner.size > maxSize)) {
            alert('El banner debe ser una imagen (JPEG/PNG/GIF) de menos de 2MB');
            e.preventDefault();
        }
    });
});

const s_hmi = document.getElementById('h_minicio');
const s_hmf = document.getElementById('h_mfin');
const s_hti = document.getElementById('h_tinicio');
const s_htf = document.getElementById('h_tfin');
const s_hni = document.getElementById('h_ninicio');
const s_hnf = document.getElementById('h_nfin');

s_hmi.addEventListener("change", function() {
    let hora_minicio = this.value;
    if (hora_minicio != ""){
        completar_camposoption(parseInt(hora_minicio)+1, s_hmf, 13);
    }else{
        limpiar_select(1);
    }
});

function limpiar_select(option){
    switch (option) {
        case 1:
            s_hmf.setAttribute("disabled", "true");
            s_hmf.value = "";
            s_hti.setAttribute("disabled", "true");
            s_hti.value = "";
            s_htf.setAttribute("disabled", "true");
            s_htf.value = "";
            s_hni.setAttribute("disabled", "true");
            s_hni.value = "";
            s_hnf.setAttribute("disabled", "true");
            s_hnf.value = "";
            break;
        case 2:
            s_hti.setAttribute("disabled", "true");
            s_hti.value = "";
            s_htf.setAttribute("disabled", "true");
            s_htf.value = "";
            s_hni.setAttribute("disabled", "true");
            s_hni.value = "";
            s_hnf.setAttribute("disabled", "true");
            s_hnf.value = "";
            break;
        case 3:
            s_htf.setAttribute("disabled", "true");
            s_htf.value = "";
            s_hni.setAttribute("disabled", "true");
            s_hni.value = "";
            s_hnf.setAttribute("disabled", "true");
            s_hnf.value = "";
            break;
        case 4:
            s_hni.setAttribute("disabled", "true");
            s_hni.value = "";
            s_hnf.setAttribute("disabled", "true");
            s_hnf.value = "";
            break;
        case 5:
            s_hnf.setAttribute("disabled", "true");
            s_hnf.value = "";
            break;
    }
}


s_hmf.addEventListener("change", function() {
    let hora_mfin = this.value;
    if (hora_mfin != ""){
        completar_camposoption( 12, s_hti, 17);
    }else{
        limpiar_select(2);
    }
});

s_hti.addEventListener("change", function() {
    let hora_tinicio = this.value;
    if (hora_tinicio != ""){
        completar_camposoption(17, s_htf, 19);
    }else{
        limpiar_select(3);
    }
});

s_htf.addEventListener("change", function() {
    let hora_tfin = this.value;
    if (hora_tfin != ""){
        completar_camposoption(parseInt(hora_tfin) , s_hni, 20);
    }else{
        limpiar_select(4);
    }
});

s_hni.addEventListener("change", function() {
    let hora_ninicio = this.value;
    if (hora_ninicio != ""){
        completar_camposoption(parseInt(hora_ninicio)+1 , s_hnf, 25);
    }else{
        limpiar_select(5);
    }
});




function completar_camposoption(hora_minicio, select, hora_fin) {
    let lista_select = '<option value="">Seleccione una hora</option>';
    for (let hora = hora_minicio; hora < hora_fin; hora++) {
        lista_select += `
            <option value="${hora}">${hora}:00</option>
        `;
    }
    select.innerHTML = lista_select;
    select.removeAttribute('disabled');
}
