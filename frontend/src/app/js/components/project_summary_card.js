class ProjectSummaryCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const variant = this.getAttribute('variant') || 'total';
    const value = this.getAttribute('value') || '0';
    const label = this.getAttribute('label') || '';
    const icon = this.getAttribute('icon') || (variant === 'total' ? '▤' : '');
    const isLucideIcon = /^[a-z0-9-]+$/.test(icon);
    const iconMarkup = isLucideIcon
      ? `<i data-lucide="${icon}"></i>`
      : icon;

    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="style/components/project_summary_card.css">
      <article class="card">
        <div class="icon" aria-hidden="true">${iconMarkup}</div>
        <div><strong>${value}</strong><span>${label}</span></div>
      </article>
    `;

    window.lucide?.createIcons({ root: this.shadowRoot });
  }
}

customElements.define('project-summary-card', ProjectSummaryCard);
