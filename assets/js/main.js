// Dark Mode Theme Management
class ThemeManager {
    constructor() {
        this.themeToggle = null;
        this.themeIcon = null;
        this.currentTheme = this.getStoredTheme() || this.getPreferredTheme();
        
        this.init();
    }

    init() {
        // Apply initial theme
        this.applyTheme(this.currentTheme);
        
        // Wait for DOM to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupToggle());
        } else {
            this.setupToggle();
        }

        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addListener((e) => {
            if (!this.getStoredTheme()) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    setupToggle() {
        this.themeToggle = document.querySelector('.theme-toggle');

        if (this.themeToggle) {
            this.updateToggleIcon();
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    getPreferredTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    getStoredTheme() {
        return localStorage.getItem('theme');
    }

    setStoredTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
    }

    updateToggleIcon() {
        if (this.themeToggle) {
            this.themeToggle.setAttribute('aria-checked', String(this.currentTheme === 'dark'));
        }
    }

    setTheme(theme) {
        this.applyTheme(theme);
        this.setStoredTheme(theme);
        this.updateToggleIcon();
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// Mobile menu: a real button, so keyboard and screen-reader users can open it
(() => {
    const button = document.querySelector('.nav-toggle-label');
    const menu = document.getElementById('nav-menu');
    if (!button || !menu) return;
    const isOpen = () => button.getAttribute('aria-expanded') === 'true';
    const setOpen = (open) => {
        button.setAttribute('aria-expanded', String(open));
        menu.classList.toggle('is-open', open);
    };
    button.addEventListener('click', () => setOpen(!isOpen()));
    // Nav links are mostly same-page anchors, so close the menu after a tap
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isOpen()) { setOpen(false); button.focus(); }
    });
})();

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.offsetTop;
                const offsetPosition = elementPosition - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add active class to navigation links based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinkElements = document.querySelectorAll('.nav-link[href^="#"]');
    
    function updateActiveNavLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinkElements.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveNavLink);

    // Blog post read tracking — fires once when reader scrolls past 75% of article
    var postContent = document.querySelector('article.post .post-content');
    if (postContent) {
        var postReadFired = false;
        window.addEventListener('scroll', function() {
            if (postReadFired) return;
            var rect = postContent.getBoundingClientRect();
            var scrolledThrough = -rect.top / (rect.height - window.innerHeight);
            if (scrolledThrough >= 0.75) {
                postReadFired = true;
                if (typeof window.posthog !== 'undefined') {
                    window.posthog.capture('post_read', {
                        title: document.title,
                        path: window.location.pathname,
                        scroll_depth: 75
                    });
                }
            }
        });
    }
});