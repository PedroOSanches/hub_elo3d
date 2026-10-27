class ProjectRow extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const name = this.getAttribute('name') || 'Projeto';
    const printer = this.getAttribute('printer') || '-';
    const status = this.getAttribute('status') || 'waiting';
    const statusLabel = this.getAttribute('status-label') || 'Status';
    const dueDate = this.getAttribute('due-date') || '-';
    const href = this.getAttribute('href') || '#';

    this.dataset.project = `${name} ${printer}`.toLowerCase();
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="style/components/project_row.css">
      <div class="row" role="row">
        <div role="cell">${name}</div>
        <div role="cell">${printer}</div>
        <div role="cell"><span class="status-dot status-dot--${status}" aria-label="${statusLabel}"></span></div>
        <div role="cell">${dueDate}</div>
        <div role="cell"><a class="project-detail-link" href="${href}" aria-label="Ver ${name}">›</a></div>
      </div>
    `;
  }
}

customElements.define('project-row', ProjectRow);
