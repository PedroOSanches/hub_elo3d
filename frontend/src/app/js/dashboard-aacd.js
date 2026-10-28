
const etapasProjeto = [
    "Recebido",
    "Produção",
    "Finalização",
    "Entrega"
];

// ==========================================
// DADOS DEMONSTRATIVOS DO DASHBOARD
// ==========================================

const projetos = [
    { id: "016", etapaAtual: "Finalização" },
    { id: "017", etapaAtual: "Produção" },
    { id: "018", etapaAtual: "Recebido" }
];

const indicadores = {
    andamento: 4,
    concluidos: 2,
    disponiveis: 8,
    parceiros: 3
};

const impressoras = {
    disponiveis: 10,
    emUso: 8,
    indisponiveis: 1
};

const atividadesRecentes = [
    {
        projeto: "Órtese de punho #017",
        descricao: "Entrou em produção",
        icone: "atividade-producao.svg"
    },
    {
        projeto: "Adaptador de colher #012",
        descricao: "Projeto concluído",
        icone: "atividade-concluido.svg"
    },
    {
        projeto: "Prótese transtibial #014",
        descricao: "Aguardando parceiro",
        icone: "atividade-aguardando.svg"
    }
];

// ==========================================
// ATUALIZA OS INDICADORES SUPERIORES
// ==========================================

document.querySelectorAll("[data-indicador]").forEach((elemento) => {
    const tipo = elemento.dataset.indicador;

    if (Object.hasOwn(indicadores, tipo)) {
        elemento.textContent = indicadores[tipo];
    }
});

// ==========================================
// ATUALIZA OS INDICADORES DAS IMPRESSORAS
// ==========================================

document.querySelectorAll("[data-impressora]").forEach((elemento) => {
    const tipo = elemento.dataset.impressora;

    if (Object.hasOwn(impressoras, tipo)) {
        elemento.textContent = String(impressoras[tipo]).padStart(2, "0");
    }
});

// ==========================================
// ATUALIZA O PROGRESSO DOS PROJETOS
// ==========================================

const cardsProjetos = document.querySelectorAll(
    ".aacd-dashboard__project-card"
);

cardsProjetos.forEach((card) => {
    const idProjeto = card.dataset.id;

    const projeto = projetos.find(
        (projeto) => projeto.id === idProjeto
    );

    if (!projeto) return;

    const indiceEtapa = etapasProjeto.indexOf(projeto.etapaAtual);

    if (indiceEtapa === -1) return;

    const porcentagem =
        (indiceEtapa / (etapasProjeto.length - 1)) * 100;

    const barra = card.querySelector(
        ".aacd-dashboard__progress"
    );

    if (!barra) return;

    barra.style.setProperty(
        "--progresso",
        porcentagem + "%"
    );

    const etapas = barra.querySelectorAll("li");

    etapas.forEach((etapa, indice) => {
        etapa.classList.remove("completed", "current");
        etapa.removeAttribute("aria-current");

        if (indice < indiceEtapa) {
            etapa.classList.add("completed");
        } else if (indice === indiceEtapa) {
            etapa.classList.add("current");
            etapa.setAttribute("aria-current", "step");
        }
    });
});

// ==========================================
// ATUALIZA AS ATIVIDADES RECENTES
// ==========================================

const listaAtividades = document.querySelector(
    ".aacd-dashboard__activity-list"
);

if (listaAtividades) {
    listaAtividades.replaceChildren();

    atividadesRecentes.forEach((atividade) => {

        const item = document.createElement("li");
        item.className = "aacd-dashboard__activity-item";

        const iconeContainer = document.createElement("span");
        iconeContainer.className = "aacd-dashboard__activity-icon";

        const imagem = document.createElement("img");
        imagem.src = "../assets/icons/" + atividade.icone;
        imagem.alt = "";

        iconeContainer.appendChild(imagem);

        const informacoes = document.createElement("div");
        informacoes.className = "aacd-dashboard__activity-info";

        const nomeProjeto = document.createElement("strong");
        nomeProjeto.textContent = atividade.projeto;

        const descricao = document.createElement("span");
        descricao.textContent = atividade.descricao;

        informacoes.appendChild(nomeProjeto);
        informacoes.appendChild(descricao);

        item.appendChild(iconeContainer);
        item.appendChild(informacoes);

        listaAtividades.appendChild(item);
    });
}
