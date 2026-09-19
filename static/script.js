// ==========================================
// HASAN'S PORTFOLIO
// INTERACTIVE JAVASCRIPT
// ==========================================


// ------------------------------------------
// 1. SCROLL REVEAL
// ------------------------------------------

const sections = document.querySelectorAll(".section");

const observer = new IntersectionObserver(
    (entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }

        });

    },
    {
        threshold: 0.15
    }
);

sections.forEach((section) => {

    section.classList.add("hidden");

    observer.observe(section);

});


// ------------------------------------------
// 2. ACTIVE NAVIGATION
// ------------------------------------------

const navLinks = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", () => {

    let currentSection = "";

    sections.forEach((section) => {

        const sectionTop = section.offsetTop - 180;

        if (window.scrollY >= sectionTop) {
            currentSection = section.getAttribute("id");
        }

    });

    navLinks.forEach((link) => {

        link.classList.remove("active");

        if (link.getAttribute("href") === `#${currentSection}`) {
            link.classList.add("active");
        }

    });

});


// ------------------------------------------
// 3. ROTATING ROLE TEXT
// ------------------------------------------

const roleText = document.getElementById("role-text");

const roles = [
    "Business Analytics",
    "Data Analysis",
    "Communication",
    "Technology"
];

let roleIndex = 0;

setInterval(() => {

    roleText.style.opacity = "0";

    setTimeout(() => {

        roleIndex =
            (roleIndex + 1) % roles.length;

        roleText.textContent =
            roles[roleIndex];

        roleText.style.opacity = "1";

    }, 300);

}, 3000);


// ------------------------------------------
// 4. THEME TOGGLE
// ------------------------------------------

const themeToggle =
    document.getElementById("theme-toggle");

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("light-mode");

    const isLight =
        document.body.classList.contains("light-mode");

    themeToggle.textContent =
        isLight ? "☀" : "◐";

    localStorage.setItem(
        "theme",
        isLight ? "light" : "dark"
    );

});


// Load saved theme

const savedTheme =
    localStorage.getItem("theme");

if (savedTheme === "light") {

    document.body.classList.add("light-mode");

    themeToggle.textContent = "☀";

}


// ------------------------------------------
// 5. MOBILE MENU
// ------------------------------------------

const menuToggle =
    document.getElementById("menu-toggle");

const mobileMenu =
    document.getElementById("mobile-menu");


menuToggle.addEventListener("click", () => {

    mobileMenu.classList.toggle("open");

    menuToggle.textContent =
        mobileMenu.classList.contains("open")
            ? "×"
            : "☰";

});


const mobileLinks =
    mobileMenu.querySelectorAll("a");

mobileLinks.forEach((link) => {

    link.addEventListener("click", () => {

        mobileMenu.classList.remove("open");

        menuToggle.textContent = "☰";

    });

});


// ------------------------------------------
// 6. CONSOLE
// ------------------------------------------

console.log(
    "Hasan's professional portfolio is running."
);

/* =========================================================
   PROJECT CASE STUDY MODAL
   ========================================================= */

const projectModal = document.getElementById("project-modal");
const projectModalClose = document.getElementById("project-modal-close");
const projectModalBackdrop = document.querySelector(
    ".project-modal-backdrop"
);

const projectButtons = document.querySelectorAll(
    ".project-view"
);


/* Open modal */

projectButtons.forEach(button => {

    button.addEventListener("click", () => {

        projectModal.classList.add("active");

        document.body.style.overflow = "hidden";

    });

});


/* Close modal */

function closeProjectModal() {

    projectModal.classList.remove("active");

    document.body.style.overflow = "";

}


projectModalClose.addEventListener(
    "click",
    closeProjectModal
);


projectModalBackdrop.addEventListener(
    "click",
    closeProjectModal
);


/* Close with Escape */

document.addEventListener("keydown", (event) => {

    if (
        event.key === "Escape" &&
        projectModal.classList.contains("active")
    ) {
        closeProjectModal();
    }

});