/** @odoo-module **/

/**
 * Navbar Focus Bug Fix
 * Her sayfa geçişinde navbar butonlarının üzerindeki focus'u kaldırır.
 * Hiçbir import, hiçbir renk değişikliği yok.
 */

(function () {
    function blurNavbarItems() {
        const navbar = document.querySelector(".o_main_navbar");
        if (navbar) {
            const focused = navbar.querySelector(":focus");
            if (focused) {
                focused.blur();
            }
        }
    }

    // Navbar butonlarına tıklandığında kısa gecikme ile blur uygula
    document.addEventListener("click", function (e) {
        const navEntry = e.target.closest(".o_nav_entry, .o_menu_sections .dropdown-toggle");
        if (navEntry) {
            setTimeout(blurNavbarItems, 100);
        }
    }, true);
})();
