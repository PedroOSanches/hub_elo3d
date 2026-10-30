class CardDashboard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.pendingItems = [];
  }

  async connectedCallback() {
    const titulo = this.getAttribute('titulo') || '';
    const linkTexto = this.getAttribute('link-texto') || 'Ver mais';
    const linkUrl = this.getAttribute('link-url') || '#';

    try {
      const response = await fetch('style/components/card-dashboard.css');
      const cssText = await response.text();

      this.shadowRoot.innerHTML = `
        <style>${cssText}</style>
        <div class="card-outer">
          <div class="header">
            <h2>${titulo}</h2>
            <a href="${linkUrl}">${linkTexto}</a>
          </div>
          <div class="card-inner" id="items-container">
            <!-- Os itens serão inseridos aqui -->
          </div>
        </div>
      `;

      if (this.pendingItems.length) {
        this.setItems(this.pendingItems);
      }
    } catch (error) {
      console.error('Erro ao carregar o CSS do componente:', error);
    }
  }

  setItems(items) {
    this.pendingItems = items;

    const container = this.shadowRoot.querySelector('#items-container');
    if (!container) return;

    container.innerHTML = items.map(item => {
      const badgeHTML = item.badgeText
        ? `<div class="badge-date">${item.badgeText}</div>`
        : `<div class="badge-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v7H6z"></path>
              <path d="M18 12h.01"></path>
            </svg>
          </div>`;

      const statusClass = item.status
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '-');

      return `
        <div class="list-item">
          ${badgeHTML}
          <div class="info">
            <span class="nome">${item.nome}</span>
            <span class="status ${statusClass}">${item.status}</span>
          </div>
        </div>
      `;
    }).join('');
  }
}

customElements.define('card-dashboard', CardDashboard);