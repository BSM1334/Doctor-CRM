// ========== LANGUAGE TOGGLE FUNCTIONALITY ==========

document.addEventListener('DOMContentLoaded', function () {
    const htmlRoot = document.getElementById('html-root');
    const langToggleBtn = document.getElementById('lang-toggle-btn');
    const langToggleText = document.getElementById('lang-toggle-text');
    const body = document.body;

    // Initialize language from Django's rendered lang attribute
    let currentLanguage = htmlRoot.getAttribute('lang') || 'en';

    // Apply language formatting based on Django's rendered language
    applyLanguage(currentLanguage);


    // Apply language settings
    function applyLanguage(lang) {
        currentLanguage = lang;

        if (lang === 'ar') {
            // Arabic settings
            htmlRoot.setAttribute('lang', 'ar');
            htmlRoot.setAttribute('dir', 'rtl');
            body.style.direction = 'rtl';
            body.style.textAlign = 'right';

            // Update button text to show EN option
            if (langToggleText) {
                langToggleText.textContent = 'EN';
            }

            // Update all text direction classes
            updateTextAlignment('rtl');

            // Apply Cairo font for Arabic
            document.documentElement.style.setProperty('--font-family', "'Cairo', sans-serif");

        } else {
            // English settings
            htmlRoot.setAttribute('lang', 'en');
            htmlRoot.setAttribute('dir', 'ltr');
            body.style.direction = 'ltr';
            body.style.textAlign = 'left';

            // Update button text to show AR option
            if (langToggleText) {
                langToggleText.textContent = 'AR';
            }

            // Update all text direction classes
            updateTextAlignment('ltr');

            // Apply Poppins font for English
            document.documentElement.style.setProperty('--font-family', "'Poppins', sans-serif");
        }

        // Trigger animation
        body.classList.remove('fade-in');
        void body.offsetWidth; // Trigger reflow
        body.classList.add('fade-in');
    }

    // Update text alignment throughout the page
    function updateTextAlignment(dir) {
        const textElements = document.querySelectorAll(
            'p, span, a, h1, h2, h3, h4, h5, h6, td, th, li, label, input, textarea, button'
        );

        textElements.forEach(element => {
            if (dir === 'rtl') {
                element.style.textAlign = 'right';
            } else {
                element.style.textAlign = 'left';
            }
        });

        // Update margin and padding for icons based on direction
        const icons = document.querySelectorAll('i.fa');
        icons.forEach(icon => {
            const parent = icon.parentElement;
            if (dir === 'rtl') {
                icon.style.marginLeft = '0.5rem';
                icon.style.marginRight = '0';
            } else {
                icon.style.marginRight = '0.5rem';
                icon.style.marginLeft = '0';
            }
        });

        // Update form elements
        const formControls = document.querySelectorAll('.form-control, .form-select');
        formControls.forEach(control => {
            if (dir === 'rtl') {
                control.style.textAlign = 'right';
                control.style.paddingRight = '1rem';
                control.style.paddingLeft = '0.5rem';
            } else {
                control.style.textAlign = 'left';
                control.style.paddingLeft = '1rem';
                control.style.paddingRight = '0.5rem';
            }
        });
    }

    // Listen for changes from other tabs/windows
    window.addEventListener('storage', function (event) {
        if (event.key === 'preferredLanguage' && event.newValue) {
            applyLanguage(event.newValue);
        }
    });
});

// ========== ADDITIONAL UTILITIES ==========

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation to buttons
document.querySelectorAll('button, [type="submit"]').forEach(button => {
    button.addEventListener('click', function () {
        if (!this.disabled) {
            const originalHtml = this.innerHTML;
            this.disabled = true;

            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = originalHtml;
            }, 2000);
        }
    });
});

// Format currency for table cells with currency class
function formatCurrency(value, locale = 'en-US') {
    const currentLang = localStorage.getItem('preferredLanguage') || 'en';
    locale = currentLang === 'ar' ? 'ar-SA' : 'en-US';

    if (typeof value === 'number') {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    }
    return value;
}

// Format dates for table cells with date class
function formatDate(dateString, locale = 'en-US') {
    const currentLang = localStorage.getItem('preferredLanguage') || 'en';
    locale = currentLang === 'ar' ? 'ar-SA' : 'en-US';

    const date = new Date(dateString);
    return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
}

// Global functions for formatting
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;

// Prevent multiple form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
        const submitButtons = this.querySelectorAll('button[type="submit"], [type="submit"]');
        submitButtons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.6';
            btn.style.cursor = 'not-allowed';
        });
    });
});
