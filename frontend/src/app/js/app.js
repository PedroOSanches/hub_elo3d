const app = document.getElementById('app');

const routes = {
  '/': {
    page: 'pages/home.html',
    title: 'Elo3D Hub',
    style: null,
    background: '#F6E8DA',
  },
  '/como-funciona': {
    page: 'pages/home.html',
    title: 'Como funciona - Elo3D Hub',
    style: null,
    background: '#F6E8DA',
    target: 'como-funciona',
  },
  '/rede': {
    page: 'pages/home.html',
    title: 'Rede - Elo3D Hub',
    style: null,
    background: '#F6E8DA',
    target: 'rede',
  },
  '/quem-somos': {
    page: 'pages/home.html',
    title: 'Quem somos - Elo3D Hub',
    style: null,
    background: '#F6E8DA',
    target: 'quem-somos',
  },
  '/login': {
    page: 'pages/login.html',
    title: 'Login - Hub Elo3D',
    style: 'style/login.css',
    background: '#F4F0E5',
  },
  '/cadastro': {
    page: 'pages/login.html',
    title: 'Cadastro - Elo3D',
    style: 'style/login.css',
    background: '#F4F0E5',
  },
  '/cadastro/instituicao': {
    page: 'pages/login.html',
    title: 'Cadastro da instituição - Elo3D',
    style: 'style/login.css',
    background: '#F4F0E5',
  },
  '/meus-projetos': {
    page: 'pages/meus-projetos.html',
    title: 'Meus Projetos - Elo3D',
    style: 'style/meus-projetos.css?v=2',
    background: '#F6F0E4',
  },
  '/projetos-disponiveis': {
    page: 'pages/ProjetosDisponiveis.html',
    title: 'Projetos Disponíveis - Elo3D',
    style: 'style/ProjetosDisponiveis.css',
    background: '#F6F0E4',
  },
};

function getCurrentRoute() {
  return window.location.pathname.replace(/\/+$/, '') || '/';
}

function loadRouteStyle(stylePath) {
  document.getElementById('route-style')?.remove();

  if (!stylePath) {
    return;
  }

  const style = document.createElement('link');
  style.id = 'route-style';
  style.rel = 'stylesheet';
  style.href = stylePath;
  document.head.appendChild(style);
}

async function renderRoute() {
  const route = routes[getCurrentRoute()] || routes['/'];

  try {
    const response = await fetch(route.page);

    if (!response.ok) {
      throw new Error(`Não foi possível carregar a página: ${route.page}`);
    }

    app.innerHTML = await response.text();
    loadRouteStyle(route.style);
    document.title = route.title;
    document.body.style.backgroundColor = route.background;
    if (route.target) {
      document.getElementById(route.target)?.scrollIntoView();
    } else {
      window.scrollTo(0, 0);
    }
    if (route.page === 'pages/login.html') {
      window.initLoginPage?.();
    }
    if (route.page === 'pages/meus-projetos.html') {
      window.initProjectsPage?.();
    }
  } catch (error) {
    console.error(error);
    app.innerHTML = `
      <main class="route-error">
        <h1>Não foi possível carregar esta página.</h1>
        <a href="/">Voltar para o início</a>
      </main>`;
  }
}

document.addEventListener('click', event => {
  const link = event.composedPath().find(element => element instanceof HTMLAnchorElement);
  if (!link || link.origin !== window.location.origin || !link.pathname.startsWith('/')) {
    return;
  }

  if (link.hash && link.pathname === window.location.pathname) {
    return;
  }

  event.preventDefault();
  window.history.pushState({}, '', `${link.pathname}${link.search}`);
  renderRoute();
});

window.addEventListener('popstate', renderRoute);
renderRoute();
