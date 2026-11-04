class TeamMember extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  static get observedAttributes() {
    return ['name', 'email', 'phone', 'initials'];
  }

  attributeChangedCallback() {
    if (this.isConnected) this.render();
  }

  render() {
    const name = this.getAttribute('name') || '';
    const email = this.getAttribute('email') || '';
    const phone = this.getAttribute('phone') || '';
    const initials = this.getAttribute('initials') || this.getInitials(name);

    this.innerHTML = `
      <article class="member-card">
        <div class="member-card__accent" aria-hidden="true"></div>
        <div class="member-card__name">${this.escape(name)}</div>
        <div class="member-card__details">
          <div><span aria-hidden="true">@</span> ${this.escape(email)}</div>
          <div>
            <span class="member-card__phone-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M5 4h3l2 5-2 2c1.2 2.4 3.1 4.3 5.5 5.5l2-2 5 2v3c0 1.1-.9 2-2 2C10.7 21.5 2.5 13.3 2.5 5c0-1.1.9-2 2-2"/></svg>
            </span>
            ${this.escape(phone)}
          </div>
        </div>
        <div class="member-card__actions">
          <button type="button" class="member-card__action" data-action="edit" aria-label="Editar ${this.escape(name)}">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 16.5-.8 3.8 3.8-.8L18.7 7.8a2.1 2.1 0 0 0-3-3L4 16.5Z"/><path d="m14.5 6.5 3 3"/></svg>
          </button>
          <button type="button" class="member-card__action" data-action="delete" aria-label="Excluir ${this.escape(name)}">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7l1-3h4l1 3"/></svg>
          </button>
        </div>
      </article>
    `;

    this.querySelectorAll('[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        this.dispatchEvent(new CustomEvent(`member-${button.dataset.action}`, {
          bubbles: true,
          detail: { name, email, phone, initials },
        }));
      });
    });
  }

  getInitials(name) {
    return name.trim().split(/\s+/).slice(0, 2).map((part) => part[0]).join('').toUpperCase();
  }

  escape(value) {
    return value.replace(/[&<>"']/g, (character) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
    }[character]));
  }
}

customElements.define('team-member', TeamMember);
