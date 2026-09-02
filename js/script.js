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
  },

  {
    nombre: "Working-OpenAI-API",
    img: "../images/Working-OpenAI-API.svg",
    pdf: "../archivos/Working-OpenAI-API.pdf"
  },
  {
    nombre: "IBM Web Development Fundamentals",
    img: "../images/IBM_Web_Development_Fundamentals.svg",
    pdf: "../archivos/IBM_Web_Development_Fundamentals.pdf"
  },
  {
    nombre: "Fundamentos de Analisis de Datos",
    img: "../images/FundamentosdeAnalisisdeDatos-cisco.svg",
    pdf: "../archivos/FundamentosdeAnalisisdeDatos-cisco.pdf"
  },
  {
    nombre: "Hacker Etico",
    img: "../images/Hacker-etico-RobinsonAndresGonzalezQuintero.svg",
    pdf: "../archivos/Hacker-etico-RobinsonAndresGonzalezQuintero.pdf"
  },
  {
    nombre: "SCRUM - Desarrollo De Software",
    img: "../images/SCRUM-DesarrolloDeSoftware-SENA-RobinsonAndresGonzalezQuintero.svg",
    pdf: "../archivos/SCRUM-DesarrolloDeSoftware-SENA-RobinsonAndresGonzalezQuintero.pdf"
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
const titles = ["Software Developer", "FullStack Developer"];
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

// Comprobar preferencia guardada — claro es el tema por defecto
const savedTheme = localStorage.getItem('portfolio-theme');
if (savedTheme === 'dark') {
    // El usuario eligió oscuro explícitamente
    updateThemeIcon('dark');
} else {
    // Sin preferencia guardada O preferencia clara → modo claro
    body.classList.add('light-mode');
    updateThemeIcon('light');
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


const youtubeVideos = {
    "Guia Hack The Box": [
        {
            title: "Hack The Box - DANCING",
            id: "WwFDe4LTZG4",
            description: "Nmap + SMB + OpenVPN"
        },
        {
          title: "Hack The Box - REDEEMER",
          id: "PcALijuacOc",
          description: "Nmap + redis + bd"
        },
        {
          title: "Hack The Box - APPOINTMENT",
          id: "pzOYBZVSIXk",
          description: "Nmap + Web + SQL Injection"
        },
        {
          title: "Hack The Box - SEQUEL",
          id: "EETtRw4ZOXg",
          description: "Nmap + MariaDB client + SQL"
        },
        {
          title: "Hack The Box - CROCODILE",
          id: "V4DNP-C6mTY",
          description: "Nmap + FTP + Gobuster + Web"
        },
    ],
        "Hacking Ético": [
        {
            title: "CamPhish + Kali Linux",
            id: "5amBajP26bw",
            description: "Kali Linux + CamPhish + Ngrok + Cloudflared + Js"
        }
    ]
};

function getYtThumbnail(videoId) {
    return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
}

/* --- Carrusel: cuántas tarjetas se ven según el viewport --- */
function getCardsPerView() {
    if (window.innerWidth <= 500) return 1;
    if (window.innerWidth <= 900) return 2;
    return 3;
}

/* --- Instancias de carrusel activos (para resize) --- */
const ytCarouselInstances = [];

function renderYtCatalog() {
    const catalog = document.getElementById('ytCatalog');
    if (!catalog) return;

    Object.entries(youtubeVideos).forEach(([category, videos]) => {
        const row = document.createElement('div');
        row.classList.add('yt-category-row');

        /* Header de categoría */
        const header = document.createElement('div');
        header.classList.add('yt-category-header');
        header.innerHTML = `
            <h3 class="yt-category-title">${category}</h3>
            <span class="yt-category-count">${videos.length} video${videos.length !== 1 ? 's' : ''}</span>
        `;
        row.appendChild(header);

        /* Wrapper: recorta el overflow */
        const wrapper = document.createElement('div');
        wrapper.classList.add('yt-carousel-wrapper');

        /* Track: el que se mueve con translateX */
        const track = document.createElement('div');
        track.classList.add('yt-carousel');

        /* Tarjetas */
        videos.forEach(video => {
            const card = document.createElement('a');
            card.classList.add('yt-video-card');
            card.href = `https://www.youtube.com/watch?v=${video.id}`;
            card.target = '_blank';
            card.rel = 'noopener noreferrer';
            card.innerHTML = `
                <div class="yt-thumbnail-wrap">
                    <img src="${getYtThumbnail(video.id)}" alt="${video.title}" class="yt-thumbnail" loading="lazy">
                    <div class="yt-play-overlay">
                        <div class="yt-play-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="white">
                                <polygon points="5 3 19 12 5 21 5 3"/>
                            </svg>
                        </div>
                    </div>
                </div>
                <div class="yt-card-info">
                    <p class="yt-card-title">${video.title}</p>
                    <p class="yt-card-desc">${video.description}</p>
                </div>
            `;
            track.appendChild(card);
        });

        wrapper.appendChild(track);

        /* Flechas de navegación */
        const btnPrev = document.createElement('button');
        btnPrev.classList.add('yt-arrow', 'yt-arrow--prev');
        btnPrev.setAttribute('aria-label', 'Anterior');
        btnPrev.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>`;

        const btnNext = document.createElement('button');
        btnNext.classList.add('yt-arrow', 'yt-arrow--next');
        btnNext.setAttribute('aria-label', 'Siguiente');
        btnNext.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`;

        /* Estado del carrusel */
        let currentIndex = 0;

        function updateCarousel() {
            const perView   = getCardsPerView();
            const maxIndex  = Math.max(0, videos.length - perView);
            const cardEls   = track.querySelectorAll('.yt-video-card');
            const gap       = 20;

            if (cardEls.length === 0) return;

            /* Ancho de una tarjeta = (contenedor - gaps) / perView */
            const wrapperW   = wrapper.offsetWidth;
            const cardWidth  = (wrapperW - gap * (perView - 1)) / perView;

            /* Aplicar ancho a cada tarjeta */
            cardEls.forEach(c => {
                c.style.minWidth = cardWidth + 'px';
                c.style.maxWidth = cardWidth + 'px';
            });

            /* Clamp currentIndex */
            currentIndex = Math.min(currentIndex, maxIndex);

            /* Mover track */
            const offset = currentIndex * (cardWidth + gap);
            track.style.transform = `translateX(-${offset}px)`;

            /* Estado de las flechas */
            const showArrows = videos.length > perView;
            btnPrev.style.display = showArrows ? 'flex' : 'none';
            btnNext.style.display = showArrows ? 'flex' : 'none';

            btnPrev.disabled = currentIndex === 0;
            btnNext.disabled = currentIndex >= maxIndex;

            btnPrev.classList.toggle('yt-arrow--disabled', currentIndex === 0);
            btnNext.classList.toggle('yt-arrow--disabled', currentIndex >= maxIndex);
        }

        btnPrev.addEventListener('click', () => {
            const perView = getCardsPerView();
            currentIndex = Math.max(0, currentIndex - perView);
            updateCarousel();
        });

        btnNext.addEventListener('click', () => {
            const perView  = getCardsPerView();
            const maxIndex = Math.max(0, videos.length - perView);
            currentIndex   = Math.min(maxIndex, currentIndex + perView);
            updateCarousel();
        });

        /* Contenedor externo con flechas laterales */
        const carouselOuter = document.createElement('div');
        carouselOuter.classList.add('yt-carousel-outer');
        carouselOuter.appendChild(btnPrev);
        carouselOuter.appendChild(wrapper);
        carouselOuter.appendChild(btnNext);

        row.appendChild(carouselOuter);
        catalog.appendChild(row);

        /* Guardar instancia para el resize global */
        ytCarouselInstances.push(updateCarousel);

        /* Primera renderización */
        updateCarousel();
    });
}

renderYtCatalog();

/* Recalcular todos los carruseles si el viewport cambia */
window.addEventListener('resize', () => {
    ytCarouselInstances.forEach(fn => fn());
});
