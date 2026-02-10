class SearchCard extends HTMLElement {
    connectedCallback() {
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    background-color: white;
                    border-radius: 1rem;
                    padding: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                }
                
                .search-container {
                    display: flex;
                    gap: 0.5rem;
                    background-color: #f3f4f6;
                    padding: 0.5rem;
                    border-radius: 0.75rem;
                }
                
                .search-input {
                    flex: 1;
                    padding: 0.75rem;
                    border: none;
                    background: transparent;
                    font-size: 0.9375rem;
                }
                
                .search-input:focus {
                    outline: none;
                }
                
                .search-select {
                    padding: 0.75rem;
                    border: none;
                    background: transparent;
                    font-size: 0.9375rem;
                    color: #4b5563;
                    border-right: 1px solid #e5e7eb;
                }
                
                .search-button {
                    background-color: #6366f1;
                    color: white;
                    padding: 0.75rem 1.25rem;
                    border: none;
                    border-radius: 0.5rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                
                .search-button:hover {
                    background-color: #4f46e5;
                }
                
                @media (max-width: 640px) {
                    .search-container {
                        flex-direction: column;
                    }
                    
                    .search-select {
                        border-right: none;
                        border-bottom: 1px solid #e5e7eb;
                    }
                }
            </style>
            
            <div class="search-container">
                <input 
                    type="text" 
                    class="search-input" 
                    placeholder="Subject (e.g. Math, English)" 
                    aria-label="Search by subject"
                >
                <select class="search-select" aria-label="Select location">
                    <option value="">Location</option>
                    <option value="delhi">Delhi</option>
                    <option value="mumbai">Mumbai</option>
                    <option value="bengaluru">Bengaluru</option>
                    <option value="kolkata">Kolkata</option>
                </select>
                <button class="search-button">
                    Search
                </button>
            </div>
        `;
    }
}

customElements.define('custom-search-card', SearchCard);