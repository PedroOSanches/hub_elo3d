class LabCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const title = this.getAttribute('title') || 'Laboratório';
    const location = this.getAttribute('location') || '';
    const image = this.getAttribute('image') || '';
    const href = this.getAttribute('href') || '#';
    const rawMaterials = this.getAttribute('materials') || '';
    const css = this.getAttribute('css') || '../style/components/card_rede.css';

    const materialsArray = rawMaterials ? rawMaterials.split(',').map(m => m.trim()) : [];
    const materialsHTML = materialsArray
      .map(m => `<span class="material-tag">${m}</span>`)
      .join('');

    this.shadowRoot.innerHTML = `
      <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
      
      <link rel="stylesheet" href="${css}">

      <a href="${href}" class="card">
        <div class="card-image-wrapper">
          ${image ? `<img src="${image}" alt="${title}">` : ''}
        </div>
        <div class="card-content">
          <h3 class="card-title">${title}</h3>
          ${location ? `
            <div class="card-location">
              <i class="ri-map-pin-line"></i>
              <span>${location}</span>
            </div>
          ` : ''}
          <div class="materials-list">
            ${materialsHTML}
          </div>
        </div>
      </a>
    `;
  }
}

customElements.define('lab-card', LabCard);