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
// {
//     nombre: "Bachiller Académico",
//     img: "../images/bachillerAcademico.svg",
//     pdf: "../archivos/bachillerAcademico.pdf"
//   },
  {
    nombre: "Técnico en Sistemas",
    img: "../images/tecnicoSistemas.svg",
    pdf: "../archivos/tecnicoSistemas.pdf"
  },
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
  },
    {
    nombre: "Excel",
    img: "../images/certificadoexcel.svg",
    pdf: "../archivos/certificadoexcel.pdf"
  },
  {
    nombre: "Inglés",
    img: "../images/certificadoingles.svg",
    pdf: "../archivos/certificadoingles.pdf"
  },
  {
    nombre: "AWS Cloud Security",
    img: "../images/AWS-CloudSecurity.svg",
    pdf: "../archivos/AWS-CloudSecurity.pdf"
  },
  {
    nombre: "HCIA-Big Data V3.5-Huawei",
    img: "../images/HCIA-BigDataV3.5Course5-RobinsonAndresGonzalezQuintero.svg",
    pdf: "../archivos/HCIA-BigDataV3.5Course5-RobinsonAndresGonzalezQuintero.pdf"
  },
  {
    nombre: "Introducción Análisis de Datos",
    img: "../images/Analisis_de_Datos_Microsoft.svg",
    pdf: "../archivos/Analisis_de_Datos_Microsoft.pdf"
  },
  {
    nombre: "Scrum - Gestión de Proyectos",
    img: "../images/Scrum-GestionProyectosy-RobinsonAndresGonzalezQuintero.svg",
    pdf: "../archivos/Scrum-GestionProyectosy-RobinsonAndresGonzalezQuintero.pdf"
},
  {
    nombre: "Introduccion Ciencia de Datos",
    img: "../images/Introduccion_Cienca_De_Datos-RobinsonGonzalez.svg",
    pdf: "../archivos/Introduccion_Cienca_De_Datos-RobinsonGonzalez.pdf"
  },
  {
    nombre: "Introduction_ThreatLandscape3",
    img: "../images/Introduction_ThreatLandscape3.svg",
    pdf: "../archivos/Introduction_ThreatLandscape3.pdf"
  },
  {
    nombre: "SQLRelationalMongoDB",
    img: "../images/SQLRelationalMongoDB.svg",
    pdf: "../archivos/SQLRelationalMongoDB.pdf"
  },
  {
    nombre: "GenAIApplicationsMongoDB",
    img: "../images/BuildingGenAIApplicationswithMongoDB.svg",
    pdf: "../archivos/BuildingGenAIApplicationswithMongoDB.pdf"
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


/* ====== Theme Toggle Logic ====== */
const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;
const themeIcon = document.getElementById('theme-icon');

// Comprobar preferencia guardada
const savedTheme = localStorage.getItem('portfolio-theme');
if (savedTheme === 'light') {
    body.classList.add('light-mode');
    updateThemeIcon('light');
} else {
    updateThemeIcon('dark');
}

themeToggleBtn.addEventListener('click', () => {
    body.classList.toggle('light-mode');
    
    if (body.classList.contains('light-mode')) {
        localStorage.setItem('portfolio-theme', 'light');
        updateThemeIcon('light');
    } else {
        localStorage.setItem('portfolio-theme', 'dark');
        updateThemeIcon('dark');
    }
});

function updateThemeIcon(theme) {
    if (theme === 'light') {
        // Icono de Luna para volver al modo oscuro
        themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
    } else {
        // Icono de Sol para cambiar al modo claro
        themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }
}

/* ====== Scroll Animations ====== */
const fadeElements = document.querySelectorAll('.fade-in');

const appearOptions = {
    threshold: 0,
    rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        } else {
            entry.target.classList.remove('visible');
        }
    });
}, appearOptions);

fadeElements.forEach(el => {
    appearOnScroll.observe(el);
});
