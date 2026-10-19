class CustomNavbar extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const logo = this.getAttribute('logo');
    const logoAlt = this.getAttribute('logo-alt') || 'HUB Elo3D Logo';
    const profileHref = this.getAttribute('profile-href') || '#perfil';
    const css = this.getAttribute('css') || '../../style/components/navbar.css';
    const icon = this.getAttribute('icon');
    const firstText = this.getAttribute('first-text');
    const firstHref = this.getAttribute('first-href');
    const secondText = this.getAttribute('second-text');
    const secondHref = this.getAttribute('second-href');
    const thirdText = this.getAttribute('third-text');
    const thirdHref = this.getAttribute('third-href');

    if (
      !logo ||
      !icon ||
      !firstText ||
      !firstHref ||
      !secondText ||
      !secondHref ||
      !thirdText ||
      !thirdHref
    ) {
      console.error(
        'O componente app-navbar precisa dos atributos "logo", "icon", ' +
        '"first-text", "first-href", "second-text", "second-href", ' +
        '"third-text" e "third-href".'
      );
      return;
    }

    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="${css}">

      <nav class="navbar" aria-label="Navegação principal">
        <a href="#" class="nav-logo">
          <img src="${logo}" alt="${logoAlt}">
        </a>
        <a href="${firstHref}" class="nav-item dark-first">${firstText}</a>
        <a href="${secondHref}" class="nav-item light">${secondText}</a>
        <a href="${thirdHref}" class="nav-item dark">${thirdText}</a>
        <div class="nav-user">
          <a href="${profileHref}" class="user-btn" title="Perfil" aria-label="Perfil">
            <span
              class="icon-image"
              style="--icon-image: url('${icon}');">
            </span>
          </a>
        </div>
      </nav>
    `;
  }
}

customElements.define('app-navbar', CustomNavbar);