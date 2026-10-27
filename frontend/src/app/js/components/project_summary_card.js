class ProjectSummaryCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const variant = this.getAttribute('variant') || 'total';
    const value = this.getAttribute('value') || '0';
    const label = this.getAttribute('label') || '';
    const icon = variant === 'total' ? '▤' : '';

    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="style/components/project_summary_card.css">
      <article class="card">
        <div class="icon" aria-hidden="true">${icon}</div>
        <div><strong>${value}</strong><span>${label}</span></div>
      </article>
    `;
  }
}

customElements.define('project-summary-card', ProjectSummaryCard);
