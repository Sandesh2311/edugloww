
class CustomNavbar extends HTMLElement {
    connectedCallback() {
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    width: 100%;
                    position: sticky;
                    top: 0;
                    z-index: 50;
                    background-color: white;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                
                nav {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 1rem 1.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .dark :host {
                    background-color: #1f2937;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
                }

                .logo {
                    font-size: 1.25rem;
                    font-weight: bold;
                    color: #111827;
                    text-decoration: none;
                }

                .dark .logo {
                    color: #f3f4f6;
                }

                .logo span {
                    color: #4f46e5;
                }

                .nav-links {
                    display: flex;
                    gap: 1.5rem;
                    align-items: center;
                }

                .nav-link {
                    color: #4b5563;
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s;
                }

                .dark .nav-link {
                    color: #d1d5db;
                }

                .nav-link:hover {
                    color: #4f46e5;
                }

                .theme-toggle {
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 0.5rem;
                    border-radius: 50%;
                    transition: background-color 0.2s;
                }

                .theme-toggle:hover {
                    background-color: rgba(0, 0, 0, 0.05);
                }

                .dark .theme-toggle:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }

                .login-btn {
                    background-color: #4f46e5;
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 0.375rem;
                    font-weight: 500;
                    transition: background-color 0.2s;
                }

                .login-btn:hover {
                    background-color: #4338ca;
                }

                @media (max-width: 768px) {
                    .nav-links {
                        display: none;
                    }
                }
            </style>

            <nav>
                <a href="index.html" class="logo">
                    <span>Edu</span>Glow
                </a>

                <div class="nav-links">
                    <a href="index.html" class="nav-link">Home</a>
                    <a href="#" class="nav-link">Tutors</a>
                    <a href="#" class="nav-link">Courses</a>
                    <a href="#" class="nav-link">About</a>
                    
                    <button class="theme-toggle" id="theme-toggle">
                        <i data-feather="moon" class="hidden dark:block"></i>
                        <i data-feather="sun" class="dark:hidden"></i>
                    </button>

                    <a href="login.html" class="login-btn">Login</a>
                </div>
            </nav>
        `;

        // Theme toggle functionality
        const themeToggle = this.shadowRoot.getElementById('theme-toggle');
        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
        });
    }
}

customElements.define('custom-navbar', CustomNavbar);
