class CustomFooter extends HTMLElement {
    connectedCallback() {
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    width: 100%;
                    background-color: #1f2937;
                    color: #f3f4f6;
                }
                
                .footer-container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 3rem 1.5rem;
                }
                
                .footer-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 2rem;
                    margin-bottom: 2rem;
                }
                
                .footer-logo {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    margin-bottom: 1rem;
                }
                
                .footer-logo-icon {
                    width: 2.5rem;
                    height: 2.5rem;
                    border-radius: 0.75rem;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 1.125rem;
                }
                
                .footer-logo-text {
                    font-weight: 700;
                    font-size: 1.125rem;
                }
                
                .footer-description {
                    color: #9ca3af;
                    font-size: 0.875rem;
                    line-height: 1.5;
                    margin-bottom: 1.5rem;
                }
                
                .footer-heading {
                    font-weight: 600;
                    font-size: 1rem;
                    margin-bottom: 1rem;
                    color: white;
                }
                
                .footer-links {
                    display: flex;
                    flex-direction: column;
                    gap: 0.75rem;
                }
                
                .footer-link {
                    color: #9ca3af;
                    text-decoration: none;
                    font-size: 0.875rem;
                    transition: color 0.2s;
                }
                
                .footer-link:hover {
                    color: #6366f1;
                }
                
                .social-links {
                    display: flex;
                    gap: 1rem;
                }
                
                .social-link {
                    color: #9ca3af;
                    transition: color 0.2s;
                }
                
                .social-link:hover {
                    color: #6366f1;
                }
                
                .footer-bottom {
                    border-top: 1px solid #374151;
                    padding-top: 2rem;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 1rem;
                    text-align: center;
                }
                
                .copyright {
                    color: #9ca3af;
                    font-size: 0.875rem;
                }
                
                @media (min-width: 768px) {
                    .footer-bottom {
                        flex-direction: row;
                        justify-content: space-between;
                        text-align: left;
                    }
                }
            </style>
            
            <div class="footer-container">
                <div class="footer-grid">
                    <div>
                        <div class="footer-logo">
                            <div class="footer-logo-icon">TT</div>
                            <div class="footer-logo-text">TutorTrail</div>
                        </div>
                        <p class="footer-description">
                            Find the perfect tutor for your learning journey. 
                            Verified professionals for any subject, any level.
                        </p>
                        <div class="social-links">
                            <a href="#" class="social-link" aria-label="Facebook">
                                <i data-feather="facebook"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="Twitter">
                                <i data-feather="twitter"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="Instagram">
                                <i data-feather="instagram"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="LinkedIn">
                                <i data-feather="linkedin"></i>
                            </a>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="footer-heading">Company</h3>
                        <div class="footer-links">
                            <a href="#" class="footer-link">About Us</a>
                            <a href="#" class="footer-link">Careers</a>
                            <a href="#" class="footer-link">Blog</a>
                            <a href="#" class="footer-link">Press</a>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="footer-heading">Support</h3>
                        <div class="footer-links">
                            <a href="#" class="footer-link">Help Center</a>
                            <a href="#" class="footer-link">Safety</a>
                            <a href="#" class="footer-link">Community Guidelines</a>
                            <a href="#" class="footer-link">Contact Us</a>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="footer-heading">Legal</h3>
                        <div class="footer-links">
                            <a href="#" class="footer-link">Terms of Service</a>
                            <a href="#" class="footer-link">Privacy Policy</a>
                            <a href="#" class="footer-link">Cookie Policy</a>
                        </div>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <p class="copyright">
                        © <span id="current-year"></span> TutorTrail. All rights reserved.
                    </p>
                    <div class="flex gap-4">
                        <a href="#" class="footer-link">Privacy</a>
                        <a href="#" class="footer-link">Terms</a>
                        <a href="#" class="footer-link">Sitemap</a>
                    </div>
                </div>
            </div>
        `;
    }
}

customElements.define('custom-footer', CustomFooter);