// Script per il menu mobile
document.getElementById('menuToggle').addEventListener('click', function () {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('hidden'); 
});

// Script per l'account button
document.addEventListener("DOMContentLoaded", function() {
    const userMenuButton = document.getElementById("user-menu-button");
    const userMenuButtonMobile = document.getElementById("user-menu-button-mobile");
    const userDropdown = document.getElementById("user-dropdown");

    window.addEventListener("click", function(event) {
      if (!userDropdown.contains(event.target) && !userMenuButton.contains(event.target) && !userMenuButtonMobile.contains(event.target)) {
        userDropdown.classList.add("hidden");
        userMenuButton.setAttribute("aria-expanded", false);
        userMenuButtonMobile.setAttribute("aria-expanded", false);
      }
    });

    userMenuButton.addEventListener("click", toggleDropdown);
    userMenuButtonMobile.addEventListener("click", toggleDropdown);

    function toggleDropdown() {
      const isExpanded = this.getAttribute("aria-expanded") === "true";

      this.setAttribute("aria-expanded", !isExpanded);
      userDropdown.classList.toggle("hidden");
    }
});