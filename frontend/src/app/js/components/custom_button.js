class CustomButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const text = this.getAttribute('text') || 'Entrar';
    const href = this.getAttribute('href') || '#';
    const icon = this.getAttribute('icon') || '';

    let iconHTML = '';
    if (icon) {
      if (icon.startsWith('ri-')) {
        iconHTML = `<i class="${icon}"></i>`;
      } else {
        iconHTML = `<span class="icon-text">${icon}</span>`;
      }
    }

    this.shadowRoot.innerHTML = `
      <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
      <style>
        .custom-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px; /* Espaço entre o texto e o ícone */
          width: 100%;
          height: 55px;
          background-color: #A10029;
          color: #ffffff;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          font-size: 18px;
          font-weight: 600;
          text-decoration: none;
          border-radius: 25px;
          box-sizing: border-box;
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

      <a href="${href}" class="custom-btn">
        <span>${text}</span>
        ${iconHTML}
      </a>
    `;
  }
}

customElements.define('app-button', CustomButton);