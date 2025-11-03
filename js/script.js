        // Obtener todos los botones de categoría
        const categoryBtns = document.querySelectorAll('.category-btn');
        const contentAreas = document.querySelectorAll('.content-area');

        // Función para cambiar de categoría
        function changeCategory(category) {
            // Remover clase active de todos los botones y áreas de contenido
            categoryBtns.forEach(btn => btn.classList.remove('active'));
            contentAreas.forEach(area => area.classList.remove('active'));

            // Agregar clase active al botón y área correspondiente
            document.querySelector(`[data-category="${category}"]`).classList.add('active');
            document.getElementById(category).classList.add('active');
        }

        // Agregar evento de hover a cada botón
        categoryBtns.forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                const category = this.getAttribute('data-category');
                changeCategory(category);
            });
        });

// Lista de certificaciones
const certificados = [
  {
    nombre: "Ciberseguridad",
    img: "../images/Certificate Introduction Cybersecurity.svg",
    pdf: "../archivos/Certificate Introduction Cybersecurity.pdf"
  },
  {
    nombre: "Amenazas Cibernéticas",
    img: "../images/GestióndeAmenazas.svg",
    pdf: "../archivos/Gestión de Amenazas Cibernéticas.pdf"
  },
  {
    nombre: "NDG Linux",
    img: "../images/NDG Linux.svg",
    pdf: "../archivos/NDG Linux.pdf"
  },
    {
    nombre: "Robótica",
    img: "../images/Robotica.svg",
    pdf: "../archivos/Formación Complementaria de Robotica.pdf"
  }
];

const certGrid = document.getElementById("certGrid");

certificados.forEach(cert => {
  const card = document.createElement("div");
  card.classList.add("cert-card");

  card.innerHTML = `
    <div class="cert-title">${cert.nombre}</div>
    <img src="${cert.img}" alt="${cert.nombre}">
    <div class="overlay">
      <a href="${cert.pdf}" download class="download-btn">Descargar PDF</a>
    </div>
  `;

  certGrid.appendChild(card);
});

// Animación de máquina de escribir para el título
const titles = ["Software Developer", "Front-End Developer"];
let currentTitle = 0;
let charIndex = 0;
let isDeleting = false;
const typingSpeed = 100;     // velocidad de escritura
const deletingSpeed = 60;    // velocidad de borrado
const delayBetweenTitles = 1200; // pausa entre textos

const typewriterElement = document.getElementById("typewriter");

function typeEffect() {
  const currentText = titles[currentTitle];

  if (!isDeleting && charIndex < currentText.length) {
    // Escribiendo letras
    typewriterElement.textContent = currentText.substring(0, charIndex + 1);
    charIndex++;
    setTimeout(typeEffect, typingSpeed);
  } else if (isDeleting && charIndex > 0) {
    // Borrando letras
    typewriterElement.textContent = currentText.substring(0, charIndex - 1);
    charIndex--;
    setTimeout(typeEffect, deletingSpeed);
  } else {
    // Cambio de estado
    if (!isDeleting) {
      // Pausa antes de borrar
      isDeleting = true;
      setTimeout(typeEffect, delayBetweenTitles);
    } else {
      // Cambiar al siguiente título
      isDeleting = false;
      currentTitle = (currentTitle + 1) % titles.length;
      setTimeout(typeEffect, typingSpeed);
    }
  }
}

// Inicia animación
document.addEventListener("DOMContentLoaded", typeEffect);
