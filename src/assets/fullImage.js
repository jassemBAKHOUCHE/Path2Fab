const lightbox = document.getElementById("lightbox");
const lightboxImg = lightbox.querySelector("img");
const closeBtn = document.getElementById("lightbox-close");

document.querySelectorAll(".clickable-image").forEach(img => {
    img.addEventListener("click", () => {
        lightboxImg.src = img.src;
        lightbox.classList.add("show");  // Active la transition d'apparition
        document.body.style.overflow = "hidden";
    });
});

function closeLightbox() {
    lightbox.classList.remove("show");  // Retire la classe pour la transition de fermeture
    lightboxImg.src = "";
    document.body.style.overflow = "";
}

closeBtn.addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) closeLightbox(); // Fermer si on clique en dehors de l'image
});
