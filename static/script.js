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

const roleText =
    document.getElementById("role-text");

const roles = [
    "Business Analytics",
    "Data Analysis",
    "Communication",
    "Technology"
];

let roleIndex = 0;

function changeRole() {

    if (!roleText) {
        return;
    }

    roleText.classList.add("role-changing");

    setTimeout(() => {

        roleIndex =
            (roleIndex + 1) % roles.length;

        roleText.textContent =
            roles[roleIndex];

        roleText.classList.remove(
            "role-changing"
        );

    }, 350);

}

if (roleText) {

    setInterval(changeRole, 3000);

}


// ------------------------------------------
// 4. THEME TOGGLE
// ------------------------------------------

const themeToggle =
    document.getElementById("theme-toggle");

if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        () => {

            document.body.classList.toggle(
                "light-mode"
            );

            const isLight =
                document.body.classList.contains(
                    "light-mode"
                );

            themeToggle.textContent =
                isLight ? "☀" : "◐";

            localStorage.setItem(
                "theme",
                isLight ? "light" : "dark"
            );

        }
    );

}


// Load saved theme

const savedTheme =
    localStorage.getItem("theme");

if (
    savedTheme === "light" &&
    themeToggle
) {

    document.body.classList.add(
        "light-mode"
    );

    themeToggle.textContent = "☀";

}


// ------------------------------------------
// 5. MOBILE MENU
// ------------------------------------------

const menuToggle =
    document.getElementById("menu-toggle");

const mobileMenu =
    document.getElementById("mobile-menu");

if (menuToggle && mobileMenu) {

    menuToggle.addEventListener(
        "click",
        () => {

            mobileMenu.classList.toggle(
                "open"
            );

            menuToggle.textContent =
                mobileMenu.classList.contains(
                    "open"
                )
                    ? "×"
                    : "☰";

        }
    );


    const mobileLinks =
        mobileMenu.querySelectorAll("a");

    mobileLinks.forEach((link) => {

        link.addEventListener(
            "click",
            () => {

                mobileMenu.classList.remove(
                    "open"
                );

                menuToggle.textContent = "☰";

            }
        );

    });

}


// ------------------------------------------
// 6. CONSOLE
// ------------------------------------------

console.log(
    "Hasan's professional portfolio is running."
);


// ==========================================
// PROJECT CASE STUDY MODAL
// ==========================================

const projectModal =
    document.getElementById("project-modal");

const projectModalClose =
    document.getElementById(
        "project-modal-close"
    );

const projectModalBackdrop =
    document.querySelector(
        ".project-modal-backdrop"
    );

const projectButtons =
    document.querySelectorAll(
        ".project-view"
    );


// Open modal

if (projectModal) {

    projectButtons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                projectModal.classList.add(
                    "active"
                );

                document.body.style.overflow =
                    "hidden";

            }
        );

    });

}


// Close modal

function closeProjectModal() {

    if (!projectModal) {
        return;
    }

    projectModal.classList.remove(
        "active"
    );

    document.body.style.overflow = "";

}


// Close button

if (projectModalClose) {

    projectModalClose.addEventListener(
        "click",
        closeProjectModal
    );

}


// Close backdrop

if (projectModalBackdrop) {

    projectModalBackdrop.addEventListener(
        "click",
        closeProjectModal
    );

}


// Close with Escape

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Escape" &&
            projectModal &&
            projectModal.classList.contains(
                "active"
            )
        ) {

            closeProjectModal();

        }

    }
);


// ==========================================
// 7. FLOATING QUICK MENU
// ==========================================

const quickMenu =
    document.getElementById("quick-menu");

const quickMenuToggle =
    document.getElementById(
        "quick-menu-toggle"
    );


// Only initialize Quick Menu if it exists

if (
    quickMenu &&
    quickMenuToggle
) {

    const quickMenuLinks =
        quickMenu.querySelectorAll(
            ".quick-menu-panel a"
        );


    // --------------------------------------
    // Open / close quick menu
    // --------------------------------------

    quickMenuToggle.addEventListener(
        "click",
        () => {

            const isOpen =
                quickMenu.classList.toggle(
                    "open"
                );

            quickMenuToggle.setAttribute(
                "aria-expanded",
                isOpen ? "true" : "false"
            );

            quickMenuToggle.setAttribute(
                "aria-label",
                isOpen
                    ? "Close quick menu"
                    : "Open quick menu"
            );

        }
    );


    // --------------------------------------
    // Close after selecting a menu item
    // --------------------------------------

    quickMenuLinks.forEach((link) => {

        link.addEventListener(
            "click",
            () => {

                quickMenu.classList.remove(
                    "open"
                );

                quickMenuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                quickMenuToggle.setAttribute(
                    "aria-label",
                    "Open quick menu"
                );

            }
        );

    });


    // --------------------------------------
    // Close when clicking outside
    // --------------------------------------

    document.addEventListener(
        "click",
        (event) => {

            if (
                quickMenu.classList.contains(
                    "open"
                ) &&
                !quickMenu.contains(
                    event.target
                )
            ) {

                quickMenu.classList.remove(
                    "open"
                );

                quickMenuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                quickMenuToggle.setAttribute(
                    "aria-label",
                    "Open quick menu"
                );

            }

        }
    );


    // --------------------------------------
    // Close with Escape
    // --------------------------------------

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape" &&
                quickMenu.classList.contains(
                    "open"
                )
            ) {

                quickMenu.classList.remove(
                    "open"
                );

                quickMenuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                quickMenuToggle.setAttribute(
                    "aria-label",
                    "Open quick menu"
                );

                quickMenuToggle.focus();

            }

        }
    );

}