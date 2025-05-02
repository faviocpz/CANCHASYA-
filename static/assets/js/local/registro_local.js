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