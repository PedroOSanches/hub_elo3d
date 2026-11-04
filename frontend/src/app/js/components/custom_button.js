class CustomButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const text = this.getAttribute('text') || 'Entrar';
    const href = this.getAttribute('href') || '#';
    const icon = this.getAttribute('icon') || '';
    const type = this.getAttribute('type') || 'link';

    let iconHTML = '';
    if (icon) {
      if (icon.startsWith('ri-')) {
        iconHTML = `<i class="${icon}"></i>`;
      } else {
        iconHTML = `<span class="icon-text">${icon}</span>`;
      }
    }

    const buttonMarkup = type !== 'link'
      ? `<button type="${type}" class="custom-btn"><span>${text}</span>${iconHTML}</button>`
      : `<a href="${href}" class="custom-btn"><span>${text}</span>${iconHTML}</a>`;

    this.shadowRoot.innerHTML = `
      <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
      <style>
        :host {
          display: block;
        }

        .custom-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px; /* Espaço entre o texto e o ícone */
          width: 100%;
          height: var(--app-button-height, 55px);
          background-color: var(--app-button-background, #A10029);
          color: var(--app-button-color, #ffffff);
          border: 2px solid var(--app-button-border, var(--app-button-background, #A10029));
          font-family: 'Sora', sans-serif;
          font-size: var(--app-button-font-size, 18px);
          font-weight: 600;
          text-decoration: none;
          border-radius: var(--app-button-radius, 25px);
          box-sizing: border-box;
          appearance: none;
          transition: opacity 0.2s ease, transform 0.1s ease;
          cursor: pointer;
        }

        .custom-btn:hover {
          opacity: 0.95;
          transform: scale(1.01);
        }

        i, .icon-text {
          font-size: 20px;
          display: flex;
          align-items: center;
        }
      </style>

      ${buttonMarkup}
    `;
  }
}

customElements.define('app-button', CustomButton);