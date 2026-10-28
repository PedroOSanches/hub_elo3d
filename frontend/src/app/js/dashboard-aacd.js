
const etapasProjetoAACD = [
    "Recebido",
    "Produção",
    "Finalização",
    "Entrega"
];



const projetosAACD = [
    { id: "016", etapaAtual: "Finalização" },
    { id: "017", etapaAtual: "Produção" },
    { id: "018", etapaAtual: "Recebido" }
];

const indicadoresAACD = {
    andamento: 4,
    concluidos: 2,
    disponiveis: 8,
    parceiros: 3
};

const impressorasAACD = {
    disponiveis: 10,
    emUso: 8,
    indisponiveis: 1
};

const atividadesAACD = [
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



window.initDashboardAACD = function () {

    
    document.querySelectorAll("[data-indicador]").forEach((elemento) => {
        const tipo = elemento.dataset.indicador;

        if (Object.hasOwn(indicadoresAACD, tipo)) {
            elemento.textContent = indicadoresAACD[tipo];
        }
    });

    // Atualiza os indicadores das impressoras
    document.querySelectorAll("[data-impressora]").forEach((elemento) => {
        const tipo = elemento.dataset.impressora;

        if (Object.hasOwn(impressorasAACD, tipo)) {
            elemento.textContent = String(impressorasAACD[tipo]).padStart(2, "0");
        }
    });

    
    const cardsProjetos = document.querySelectorAll(
        ".aacd-dashboard__project-card"
    );

    cardsProjetos.forEach((card) => {
        const idProjeto = card.dataset.id;

        const projeto = projetosAACD.find(
            (projeto) => projeto.id === idProjeto
        );

        if (!projeto) return;

        const indiceEtapa = etapasProjetoAACD.indexOf(projeto.etapaAtual);

        if (indiceEtapa === -1) return;

        const porcentagem =
            (indiceEtapa / (etapasProjetoAACD.length - 1)) * 100;

        const barra = card.querySelector(
            ".aacd-dashboard__progress"
        );

        if (!barra) return;

        barra.style.setProperty("--progresso", porcentagem + "%");

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

    
    const listaAtividades = document.querySelector(
        ".aacd-dashboard__activity-list"
    );

    if (listaAtividades) {
        listaAtividades.replaceChildren();

        atividadesAACD.forEach((atividade) => {
            const item = document.createElement("li");
            item.className = "aacd-dashboard__activity-item";

            const iconeContainer = document.createElement("span");
            iconeContainer.className = "aacd-dashboard__activity-icon";

            const imagem = document.createElement("img");
            imagem.src = "assets/icons/" + atividade.icone;
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
};
