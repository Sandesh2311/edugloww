class TutorCard extends HTMLElement {
    static get observedAttributes() {
        return ['name', 'subject', 'level', 'rating', 'price', 'city', 'image', 'id'];
    }

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    render() {
        const name = this.getAttribute('name') || '';
        const subject = this.getAttribute('subject') || '';
        const level = this.getAttribute('level') || '';
        const rating = parseFloat(this.getAttribute('rating')) || 0;
        const price = this.getAttribute('price') || '';
        const city = this.getAttribute('city') || '';
        const image = this.getAttribute('image') || '';
        const id = this.getAttribute('id') || '';

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    background-color: white;
                    border-radius: 0.75rem;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                    transition: transform 0.2s, box-shadow 0.2s;
                }
                
                :host(:hover) {
                    transform: translateY(-4px);
                    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
                }
                
                .tutor-image {
                    width: 100%;
                    height: 160px;
                    object-fit: cover;
                }
                
                .tutor-content {
                    padding: 1.25rem;
                }
                
                .tutor-name {
                    font-weight: 600;
                    font-size: 1.125rem;
                    margin-bottom: 0.25rem;
                    color: #111827;
                }
                
                .tutor-details {
                    color: #6b7280;
                    font-size: 0.875rem;
                    margin-bottom: 0.5rem;
                }
                
                .tutor-meta {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 1rem;
                }
                
                .tutor-price {
                    font-weight: 600;
                    color: #111827;
                }
                
                .tutor-city {
                    color: #6b7280;
                    font-size: 0.75rem;
                }
                
                .tutor-rating {
                    display: flex;
                    align-items: center;
                    gap: 0.25rem;
                    color: #f59e0b;
                    font-weight: 500;
                }
                
                .tutor-tags {
                    display: flex;
                    gap: 0.5rem;
                    margin-bottom: 1rem;
                    flex-wrap: wrap;
                }
                
                .tutor-tag {
                    background-color: #eef2ff;
                    color: #4338ca;
                    padding: 0.25rem 0.5rem;
                    border-radius: 9999px;
                    font-size: 0.75rem;
                    font-weight: 500;
                }
                
                .tutor-actions {
                    display: flex;
                    gap: 0.75rem;
                }
                
                .tutor-button {
                    flex: 1;
                    padding: 0.5rem;
                    border-radius: 0.5rem;
                    font-weight: 500;
                    font-size: 0.875rem;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .tutor-button-outline {
                    border: 1px solid #e5e7eb;
                    background: transparent;
                    color: #4b5563;
                }
                
                .tutor-button-outline:hover {
                    background-color: #f9fafb;
                }
                
                .tutor-button-primary {
                    background-color: #6366f1;
                    color: white;
                    border: none;
                }
                
                .tutor-button-primary:hover {
                    background-color: #4f46e5;
                }
            </style>
            
            <img src="${image}" alt="${name}" class="tutor-image">
            
            <div class="tutor-content">
                <h3 class="tutor-name">${name}</h3>
                <p class="tutor-details">${subject}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">${level}</p>
<div class="tutor-meta">
                    <div>
                        <div class="tutor-price">${price}</div>
                        <div class="tutor-city">${city}</div>
                    </div>
                    <div class="tutor-rating">
                        <i data-feather="star" class="w-4 h-4 fill-current"></i>
                        ${rating}
                    </div>
                </div>
                <div class="tutor-tags">
                    <span class="tutor-tag">Verified</span>
                    ${level.split(',').map(skill => skill.trim()).filter(skill => skill).map(skill => `
                        <span class="tutor-tag">${skill}</span>
                    `).join('')}
                </div>
                <div class="tutor-actions">
                    <button class="tutor-button tutor-button-outline" data-action="contact" data-id="${id}">
                        Contact
                    </button>
                    <button class="tutor-button tutor-button-primary" data-action="book" data-id="${id}">
                        Book
                    </button>
                </div>
            </div>
        `;

        const contactBtn = this.shadowRoot.querySelector('[data-action="contact"]');
        const bookBtn = this.shadowRoot.querySelector('[data-action="book"]');
        if (contactBtn) {
            contactBtn.addEventListener('click', () => {
                window.contactTutor(String(id));
            });
        }
        if (bookBtn) {
            bookBtn.addEventListener('click', () => {
                window.bookTutor(String(id));
            });
        }
    }
}

customElements.define('custom-tutor-card', TutorCard);

// Global functions for button actions
window.contactTutor = function(id) {
    alert(`Contact request sent for tutor ID: ${id}`);
};

window.bookTutor = function(id) {
    alert(`Booking initiated for tutor ID: ${id}`);
};
