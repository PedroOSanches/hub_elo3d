const app = document.getElementById("app");
const ROUTER_API_BASE_URL =
    window.ENV?.API_BASE_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000/api`;
let refreshPromise = null;
let sessionRedirectInProgress = false;

const routes = {
  "/": {
    page: "pages/home.html",
    title: "Elo3D Hub",
    style: null,
    background: "#F6E8DA",
  },
  "/como-funciona": {
    page: "pages/home.html",
    title: "Como funciona - Elo3D Hub",
    style: null,
    background: "#F6E8DA",
    target: "como-funciona",
  },
  "/rede": {
    page: "pages/home.html",
    title: "Rede - Elo3D Hub",
    style: null,
    background: "#F6E8DA",
    target: "rede",
  },
  "/quem-somos": {
    page: "pages/home.html",
    title: "Quem somos - Elo3D Hub",
    style: null,
    background: "#F6E8DA",
    target: "quem-somos",
  },
  "/login": {
    page: "pages/login.html",
    title: "Login - Hub Elo3D",
    style: "style/login.css",
    background: "#F4F0E5",
  },
  "/cadastro": {
    page: "pages/login.html",
    title: "Cadastro - Elo3D",
    style: "style/login.css",
    background: "#F4F0E5",
  },
  "/cadastro/instituicao": {
    page: "pages/login.html",
    title: "Cadastro da instituição - Elo3D",
    style: "style/login.css",
    background: "#F4F0E5",
  },
  "/meus-projetos": {
    page: "pages/meus-projetos.html",
    title: "Meus Projetos - Elo3D",
    style: "style/meus-projetos.css?v=2",
    background: "#F6F0E4",
  },
  "/projetos-disponiveis": {
    page: "pages/ProjetosDisponiveis.html",
    title: "Projetos Disponíveis - Elo3D",
    style: "style/ProjetosDisponiveis.css",
    background: "#F6F0E4",
  },
  "/dashboard-aacd": {
    page: "pages/dashboard-aacd.html",
    title: "Dashboard AACD - Elo3D Hub",
    style: "style/dashboard-aacd.css",
    background: "#F4F0E5",
  },
  "/dashboard-parceiro": {
    page: "pages/dashboard-parceiro.html",
    title: "Dashboard - Elo3D Hub",
    style: "style/dashboard-parceiro.css",
    background: "#F4F0E5",
  },
  "/perfil": {
    page: "pages/perfil-parceiro.html",
    title: "Perfil - Elo3D Hub",
    style: "style/perfil-parceiro.css",
    background: "#F4F0E5",
  },
  "/perfil-hospital": {
    page: "pages/perfil-hospital.html",
    title: "Perfil - Elo3D Hub",
    style: "style/perfil-hospital.css",
    background: "#F4F0E5",
  },
  "/gerenciamento": {
    page: "pages/gerenciamento.html",
    title: "Membros da equipe - Elo3D Hub",
    style: "style/gerenciamento.css",
    background: "#F4F0E5",
  },
  "/minhas-impressoras": {
    page: "pages/MinhasImpressoras.html",
    title: "Minhas Impressoras - Elo3D Hub",
    style: "style/MinhasImpressoras.css",
    background: "#F4F0E5",
  },
  "/projetos-aacd": {
    page: "pages/projetos-aacd.html",
    title: "Projetos AACD - Elo3D Hub",
    style: "style/projetos-aacd.css",
    background: "#F4F0E5",
  },
  "/rede-aacd": {
    page: "pages/rede-aacd.html",
    title: "Projetos AACD - Elo3D Hub",
    style: "style/rede-aacd.css",
    background: "#F4F0E5",
  },
};

const publicRoutes = new Set([
  "/",
  "/como-funciona",
  "/rede",
  "/quem-somos",
  "/login",
  "/cadastro",
  "/cadastro/instituicao",
]);

function getUserRole() {
  const savedUser = localStorage.getItem("elo3d-user");

  if (savedUser) {
    try {
      const user = JSON.parse(savedUser);
      if (user?.role) return user.role;
    } catch (error) {
      console.error("Usuário salvo inválido:", error);
    }
  }

  return localStorage.getItem("elo3d-role") || "hospital_user";
}

function getDashboardRoute() {
  const role = getUserRole().toLowerCase();
  return role === "admin" || role === "user"
    ? "/dashboard-parceiro"
    : "/dashboard-aacd";
}

function getCurrentRoute() {
  return window.location.pathname.replace(/\/+$/, "") || "/";
}

function showAuthMessage(title, text) {
  let message = document.getElementById("auth-route-message");

  if (!message) {
    message = document.createElement("div");
    message.id = "auth-route-message";
    message.setAttribute("role", "alert");
    message.setAttribute("aria-live", "assertive");
    document.body.appendChild(message);
  }

  message.innerHTML = `
    <strong>${title}</strong>
    <span>${text}</span>
  `;

  Object.assign(message.style, {
    alignItems: "center",
    background: "#fff4e5",
    border: "1px solid #e6a23c",
    borderRadius: "12px",
    boxShadow: "0 8px 24px rgba(67, 45, 28, 0.18)",
    color: "#6b4218",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
    left: "50%",
    maxWidth: "calc(100% - 32px)",
    padding: "16px 22px",
    position: "fixed",
    textAlign: "center",
    top: "24px",
    transform: "translateX(-50%)",
    width: "360px",
    zIndex: "9999",
  });

  Object.assign(message.querySelector("strong").style, {
    color: "#8a4b08",
    fontSize: "16px",
  });
  Object.assign(message.querySelector("span").style, {
    fontSize: "14px",
    lineHeight: "1.4",
  });

  clearTimeout(showAuthMessage.timeoutId);
  message.hidden = false;
  message.style.display = "flex";
  showAuthMessage.timeoutId = setTimeout(() => {
    message.hidden = true;
    message.style.display = "none";
  }, 3000);
}

function handleExpiredSession() {
  localStorage.removeItem("elo3d-user");
  localStorage.removeItem("elo3d-role");
  showAuthMessage(
    "Sessão expirada",
    "Faça login novamente para continuar."
  );

  if (!publicRoutes.has(getCurrentRoute()) && !sessionRedirectInProgress) {
    sessionRedirectInProgress = true;
    window.history.replaceState({}, "", "/login");
    renderRoute().finally(() => {
      sessionRedirectInProgress = false;
      showAuthMessage(
        "Sessão expirada",
        "Faça login novamente para continuar."
      );
    });
  }
}

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = fetch(`${ROUTER_API_BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Não foi possível renovar a sessão.");
        }
      })
      .finally(() => {
        refreshPromise = null;
      });
  }

  return refreshPromise;
}

async function apiFetch(url, options = {}) {
  const { retryOnUnauthorized = true, ...requestOptions } = options;
  const response = await fetch(url, {
    ...requestOptions,
    credentials: "include",
  });

  if (response.status !== 401) {
    return response;
  }

  if (!retryOnUnauthorized) {
    handleExpiredSession();
    return response;
  }

  try {
    await refreshAccessToken();
    return apiFetch(url, {
      ...requestOptions,
      retryOnUnauthorized: false,
    });
  } catch (error) {
    console.error("Não foi possível renovar o token:", error);
    handleExpiredSession();
    return response;
  }
}

window.apiFetch = apiFetch;

function showLoginRequiredMessage() {
  showAuthMessage(
    "Acesso restrito",
    "Você precisa estar logado para acessar esta página."
  );
}

function loadRouteStyle(stylePath) {
  document.getElementById("route-style")?.remove();

  if (!stylePath) {
    return;
  }

  const style = document.createElement("link");
  style.id = "route-style";
  style.rel = "stylesheet";
  style.href = stylePath;
  document.head.appendChild(style);
}

window.initDashboardParceiro = async function () {
  await customElements.whenDefined("card-dashboard");

  const impressoras = [
    { nome: "Nome da impressora", status: "Em produção" },
    { nome: "Nome da impressora", status: "Pausa" },
    { nome: "Nome da impressora", status: "Pausa" },
    { nome: "Nome da impressora", status: "Online" },
  ];

  const prazos = [
    { badgeText: "3/10", nome: "Nome do projeto", status: "Em produção" },
    { badgeText: "4/10", nome: "Nome do projeto", status: "Finalizada" },
    { badgeText: "4/10", nome: "Nome do projeto", status: "Finalizada" },
  ];

  const compImpressoras = document.getElementById("card-impressoras");
  const compPrazos = document.getElementById("card-prazos");

  if (compImpressoras) compImpressoras.setItems(impressoras);
  if (compPrazos) compPrazos.setItems(prazos);
};

async function renderRoute() {
  const currentRoute = getCurrentRoute();

  const route =
    currentRoute === "/dashboard" || currentRoute === "/dashboard-aacd"
      ? routes[getDashboardRoute()]
      : routes[currentRoute] || routes["/"];

  try {
    const response = await fetch(route.page);

    if (!response.ok) {
      throw new Error(`Não foi possível carregar a página: ${route.page}`);
    }

    app.innerHTML = await response.text();
    loadRouteStyle(route.style);
    document.title = route.title;
    document.body.style.backgroundColor = route.background;
    window.lucide?.createIcons();

    if (route.target) {
      document.getElementById(route.target)?.scrollIntoView();
    } else {
      window.scrollTo(0, 0);
    }

    if (route.page === "pages/login.html") {
      window.initLoginPage?.();
    }

    if (route.page === "pages/perfil-parceiro.html") {
      await window.initPerfilParceiro?.();
    }

    if (route.page === "pages/perfil-hospital.html") {
      window.initPerfilHospital?.();
    }

    if (route.page === "pages/gerenciamento.html") {
      if (!document.getElementById("team-member-style")) {
        const teamMemberStyle = document.createElement("link");
        teamMemberStyle.id = "team-member-style";
        teamMemberStyle.rel = "stylesheet";
        teamMemberStyle.href = "style/components/team_member.css";
        document.head.appendChild(teamMemberStyle);
      }

      await customElements.whenDefined("team-member");
      window.initGerenciamento?.();
    }

    if (route.page === "pages/meus-projetos.html") {
      await window.initProjectsPage?.();
    }

    if (route.page === "pages/MinhasImpressoras.html") {
      await window.initMinhasImpressoras?.();
    }

    if (route.page === "pages/ProjetosDisponiveis.html") {
      await window.initProjetosDisponiveis?.();
    }

    if (route.page === "pages/dashboard-aacd.html") {
      window.initDashboardAACD?.();
    }

    if (route.page === "pages/dashboard-parceiro.html") {
      window.initDashboardParceiro?.();
      await window.initProjectsPage?.();
    }

    if (route.page === "pages/projetos-aacd.html") {
      window.initProjetosAACD?.();
    }

    if (route.page === "pages/rede-aacd.html") {
      window.initRedeAACD?.();
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

document.addEventListener("click", async (event) => {
  if (event.defaultPrevented) {
    return;
  }

  const link = event
    .composedPath()
    .find((element) => element instanceof HTMLAnchorElement);

  if (
    !link ||
    link.origin !== window.location.origin ||
    !link.pathname.startsWith("/")
  ) {
    return;
  }

  if (link.hash && link.pathname === window.location.pathname) {
    return;
  }

  event.preventDefault();

  window.history.pushState({}, "", `${link.pathname}${link.search}`);
  renderRoute();
});

async function logout() {
  try {
    const response = await fetch(`${ROUTER_API_BASE_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("A API não conseguiu encerrar a sessão.");
    }
  } catch (error) {
    console.error("Não foi possível fazer logout:", error);
  } finally {
    localStorage.removeItem("elo3d-user");
    localStorage.removeItem("elo3d-role");
    window.history.pushState({}, "", "/");
    await renderRoute();
  }
}

document.addEventListener("app-logout", logout);
document.addEventListener("click", (event) => {
  if (event.target.closest("[data-logout]")) {
    logout();
  }
});

window.addEventListener("popstate", renderRoute);
renderRoute();
