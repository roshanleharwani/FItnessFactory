// JavaScript code for slideshow animation
document.addEventListener("DOMContentLoaded", function() {
    const bannerContainer = document.querySelector('.banner-container');
    const banners = document.querySelectorAll('.banner');

    let index = 0;

    function showBanner() {
        banners.forEach((banner, idx) => {
            if (idx === index) {
                banner.style.display = 'inline-block';
            } else {
                banner.style.display = 'none';
            }
        });

        index++;
        if (index >= banners.length) {
            index = 0;
        }
    }

    setInterval(showBanner, 3000);
});
