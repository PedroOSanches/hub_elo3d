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
    const compact = this.hasAttribute('compact');

    this.dataset.project = `${name} ${printer}`.toLowerCase();
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="style/components/project_row.css">
      <div class="row${compact ? ' row--compact' : ''}" role="row">
        <div role="cell">${name}</div>
        <div role="cell">${printer}</div>
        ${compact ? '' : `<div role="cell"><span class="status-dot status-dot--${status}" aria-label="${statusLabel}"></span></div>`}
        <div role="cell">${dueDate}</div>
        ${compact ? '' : `<div role="cell">
          <button class="project-detail-link" type="button" aria-label="Ver ${name}">›</button>
        </div>`}
      </div>
    `;

    const detailLink = this.shadowRoot.querySelector('.project-detail-link');
    detailLink?.addEventListener('click', event => {
      event.preventDefault();
      this.dispatchEvent(new CustomEvent('project-detail-request', {
        bubbles: true,
        composed: true,
        detail: { name, printer, status, statusLabel, dueDate }
      }));
    });
  }
}

customElements.define('project-row', ProjectRow);
