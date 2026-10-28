


const projetosAACDLista = [
    {
        id: "014",
        nome: "Órtese de punho",
        categoria: "Órtese",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 3,
        cidade: "São Caetano do Sul - SP",
        dataTexto: "Cadastrado há 2 horas",
        status: "aguardando",
        etapaAtual: "Recebido",
        descricao: "Órtese de punho personalizada.",
        prazo: "2026-11-09",
        prioridade: "Alta"
    },
    {
        id: "009",
        nome: "Órtese de joelho",
        categoria: "Órtese",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 1,
        cidade: "São Bernardo do Campo - SP",
        dataTexto: "Cadastrado há 4 dias",
        status: "aguardando",
        etapaAtual: "Recebido",
        descricao: "Órtese de joelho sob medida.",
        prazo: "2026-11-15",
        prioridade: "Média"
    },
    {
        id: "020",
        nome: "Suporte de caneta adaptado",
        categoria: "Acessório",
        tecnologia: "FDM",
        material: "PETG",
        quantidade: 5,
        cidade: "São Caetano do Sul - SP",
        dataTexto: "Iniciado em 09/09/26",
        status: "andamento",
        etapaAtual: "Produção",
        descricao: "Suporte adaptado para facilitar a escrita.",
        prazo: "2026-11-12",
        prioridade: "Média",
        parceiro: "FabLab Mauá",
        telefone: "(11) 99999-9999",
        impressora: "Bambu Lab P1S",
        cor: "Branco"
    },
    {
        id: "021",
        nome: "Corset toracolombar",
        categoria: "Órtese",
        tecnologia: "SLS",
        material: "Nylon",
        quantidade: 1,
        cidade: "Rio de Janeiro - RJ",
        dataTexto: "Concluído em 09/08/26",
        status: "concluido",
        etapaAtual: "Entrega",
        descricao: "Órtese toracolombar personalizada.",
        prazo: "2026-08-09",
        prioridade: "Alta",
        parceiro: "FabLab Mauá",
        impressora: "Impressora SLS",
        cor: "Branco"
    },
    {
        id: "018",
        nome: "Órtese de punho",
        categoria: "Órtese",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 2,
        cidade: "São Caetano do Sul - SP",
        dataTexto: "Iniciado em 26/09/26",
        status: "andamento",
        etapaAtual: "Produção",
        descricao: "Órtese de punho com fabricação personalizada.",
        prazo: "2026-11-09",
        prioridade: "Alta",
        parceiro: "FabLab Mauá",
        telefone: "(11) 99999-9999",
        impressora: "Bambu Lab P1S",
        cor: "Branco",
        historico: [
            {
                data: "28/09/2026",
                titulo: "Início da impressão",
                descricao: "Arquivo validado e parâmetros ajustados para PLA."
            },
            {
                data: "26/09/2026",
                titulo: "Projeto assumido pelo FabLab Mauá",
                descricao: ""
            },
            {
                data: "24/09/2026",
                titulo: "Projeto publicado pela AACD",
                descricao: "Projeto disponibilizado na plataforma."
            }
        ]
    },
    {
        id: "022",
        nome: "Adaptador de talher",
        categoria: "Adaptador",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 4,
        cidade: "São Caetano do Sul - SP",
        dataTexto: "Cadastrado há 6 dias",
        status: "aguardando",
        etapaAtual: "Recebido",
        prazo: "2026-11-20",
        prioridade: "Média"
    },
    {
        id: "023",
        nome: "Prótese de mão",
        categoria: "Prótese",
        tecnologia: "FDM",
        material: "PETG",
        quantidade: 1,
        cidade: "Santo André - SP",
        dataTexto: "Iniciado em 15/10/26",
        status: "andamento",
        etapaAtual: "Finalização",
        prazo: "2026-11-18",
        prioridade: "Alta",
        parceiro: "Laboratório parceiro"
    },
    {
        id: "024",
        nome: "Suporte de copo adaptado",
        categoria: "Acessório",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 3,
        cidade: "São Bernardo do Campo - SP",
        dataTexto: "Cadastrado há 1 dia",
        status: "aguardando",
        etapaAtual: "Recebido",
        prazo: "2026-11-25",
        prioridade: "Baixa"
    },
    {
        id: "025",
        nome: "Adaptador de escova",
        categoria: "Adaptador",
        tecnologia: "FDM",
        material: "PLA",
        quantidade: 2,
        cidade: "São Caetano do Sul - SP",
        dataTexto: "Concluído em 12/10/26",
        status: "concluido",
        etapaAtual: "Entrega",
        prazo: "2026-10-12",
        prioridade: "Média"
    },
    {
        id: "026",
        nome: "Órtese de tornozelo",
        categoria: "Órtese",
        tecnologia: "FDM",
        material: "PETG",
        quantidade: 1,
        cidade: "Santo André - SP",
        dataTexto: "Concluído em 18/10/26",
        status: "concluido",
        etapaAtual: "Entrega",
        prazo: "2026-10-18",
        prioridade: "Alta"
    }
];

const etapasAACDLista = [
    "Recebido",
    "Produção",
    "Finalização",
    "Entrega"
];

const statusAACDLista = {
    aguardando: "Aguardando parceiro",
    andamento: "Em andamento",
    concluido: "Concluído"
};



window.initProjetosAACD = function () {

    const pagina = document.querySelector(".projetos-aacd");
    if (!pagina) return;

    const lista = document.getElementById("lista-projetos");
    const busca = document.getElementById("buscar-projeto");
    const vazio = document.getElementById("projetos-vazio");
    const abas = pagina.querySelectorAll("[data-filter]");

    const modalAdicionar = document.getElementById("modal-adicionar");
    const modalDetalhes = document.getElementById("modal-detalhes");
    const form = document.getElementById("form-adicionar-projeto");

    let filtroAtual = "todos";
    let modalAberto = null;
    let focoAnterior = null;

    const criar = (tag, classe, texto) => {
        const elemento = document.createElement(tag);
        if (classe) elemento.className = classe;
        if (texto !== undefined) elemento.textContent = texto;
        return elemento;
    };

    const formatarData = (data) => {
        if (!data) return "Não informada";
        const partes = data.split("-");
        if (partes.length !== 3) return data;
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
    };

    

    function atualizarContadores() {
        const contagens = {
            todos: projetosAACDLista.length,
            aguardando: projetosAACDLista.filter(
                p => p.status === "aguardando"
            ).length,
            andamento: projetosAACDLista.filter(
                p => p.status === "andamento"
            ).length,
            concluido: projetosAACDLista.filter(
                p => p.status === "concluido"
            ).length
        };

        abas.forEach(aba => {
            const contador = aba.querySelector("span");
            if (contador) {
                contador.textContent = `(${contagens[aba.dataset.filter]})`;
            }
        });
    }

    

    function criarMeta(simbolo, texto) {
        const linha = criar("div", "projetos-aacd__meta-row");
        const icone = criar("span", "", simbolo);
        icone.setAttribute("aria-hidden", "true");

        linha.append(
            icone,
            criar("span", "", texto)
        );

        return linha;
    }

    function criarCard(projeto) {
        const card = criar("article", "projetos-aacd__card");
        card.dataset.id = projeto.id;

        const faixa = criar("div", "projetos-aacd__card-accent");

        const principal = criar("div", "projetos-aacd__card-main");
        principal.append(
            criar("h3", "", projeto.nome),
            criar("span", "projetos-aacd__card-id", `Projeto #${projeto.id}`)
        );

        const tags = criar("div", "projetos-aacd__tags");

        [projeto.tecnologia, projeto.material, projeto.categoria]
            .filter(Boolean)
            .forEach(texto => {
                tags.appendChild(criar("span", "projetos-aacd__tag", texto));
            });

        principal.appendChild(tags);

        const meta = criar("div", "projetos-aacd__card-meta");
        meta.append(
            criarMeta("⌖", projeto.cidade || "Localização não informada"),
            criarMeta("▢", projeto.dataTexto || "Projeto cadastrado"),
            criarMeta("⬡", `${projeto.quantidade} ${projeto.quantidade === 1 ? "unidade" : "unidades"}`)
        );

        const situacao = criar("div", "projetos-aacd__card-status");

        const status = criar(
            "span",
            `projetos-aacd__status projetos-aacd__status--${projeto.status}`,
            statusAACDLista[projeto.status]
        );

        situacao.appendChild(status);

        if (projeto.status !== "aguardando") {
            const link = criar(
                "button",
                "projetos-aacd__status-link",
                projeto.status === "concluido"
                    ? "Ver histórico →"
                    : "Acompanhar →"
            );

            link.type = "button";
            link.dataset.action = "detalhes";
            link.dataset.id = projeto.id;
            situacao.appendChild(link);
        }

        const acoes = criar("div", "projetos-aacd__card-actions");

        const botaoMenu = criar("button", "projetos-aacd__menu-button", "⋮");
        botaoMenu.type = "button";
        botaoMenu.dataset.action = "menu";
        botaoMenu.dataset.id = projeto.id;
        botaoMenu.setAttribute("aria-label", `Ações do projeto ${projeto.id}`);
        botaoMenu.setAttribute("aria-expanded", "false");

        const menu = criar("div", "projetos-aacd__menu");
        menu.hidden = true;

        const verDetalhes = criar("button", "", "Ver detalhes");
        verDetalhes.type = "button";
        verDetalhes.dataset.action = "detalhes";
        verDetalhes.dataset.id = projeto.id;

        menu.appendChild(verDetalhes);
        acoes.append(botaoMenu, menu);

        card.append(faixa, principal, meta, situacao, acoes);

        return card;
    }

    function renderizarProjetos() {
        const pesquisa = busca.value.trim().toLocaleLowerCase("pt-BR");

        const filtrados = projetosAACDLista.filter(projeto => {
            const correspondeStatus =
                filtroAtual === "todos" || projeto.status === filtroAtual;

            const correspondeBusca =
                `${projeto.nome} ${projeto.id} ${projeto.categoria}`
                    .toLocaleLowerCase("pt-BR")
                    .includes(pesquisa);

            return correspondeStatus && correspondeBusca;
        });

        lista.replaceChildren();

        filtrados.forEach(projeto => {
            lista.appendChild(criarCard(projeto));
        });

        vazio.hidden = filtrados.length > 0;
        atualizarContadores();
    }

    abas.forEach(aba => {
        aba.addEventListener("click", () => {
            filtroAtual = aba.dataset.filter;

            abas.forEach(item => {
                item.classList.toggle("active", item === aba);
                item.setAttribute("aria-pressed", String(item === aba));
            });

            renderizarProjetos();
        });
    });

    busca.addEventListener("input", renderizarProjetos);

    

    function abrirModal(modal) {
        if (!modal) return;

        focoAnterior = document.activeElement;
        modal.hidden = false;
        modalAberto = modal;
        document.body.style.overflow = "hidden";

        modal.querySelector(".projetos-modal__content")?.focus();
    }

    function fecharModal() {
        if (!modalAberto) return;

        modalAberto.hidden = true;
        modalAberto = null;
        document.body.style.overflow = "";

        if (focoAnterior?.isConnected) {
            focoAnterior.focus();
        }
    }

    document.getElementById("btn-novo-projeto")
        ?.addEventListener("click", () => {
            form.reset();
            atualizarContadorDescricao();
            document.getElementById("nome-arquivo").textContent = "";
            abrirModal(modalAdicionar);
        });

    document.querySelectorAll("[data-close-modal]").forEach(botao => {
        botao.addEventListener("click", fecharModal);
    });

    

    function preencherTexto(id, valor) {
        const elemento = document.getElementById(id);
        if (elemento) elemento.textContent = valor ?? "—";
    }

    function abrirDetalhes(id) {
        const projeto = projetosAACDLista.find(p => p.id === id);
        if (!projeto) return;

        preencherTexto("detalhe-id", `Projeto #${projeto.id}`);
        preencherTexto("detalhe-nome", projeto.nome);

        const status = document.getElementById("detalhe-status");
        status.textContent = statusAACDLista[projeto.status];
        status.className =
            `projetos-details__status projetos-details__status--${projeto.status}`;

        preencherTexto("detalhe-parceiro", projeto.parceiro || "Aguardando parceiro");
        preencherTexto("detalhe-localizacao", projeto.cidade);
        preencherTexto("detalhe-contato", projeto.telefone || "Contato não informado");

        preencherTexto("detalhe-impressora", projeto.impressora || "Não definida");
        preencherTexto("detalhe-tecnologia", `Tecnologia: ${projeto.tecnologia || "—"}`);
        preencherTexto("detalhe-material", `Material: ${projeto.material || "—"}`);
        preencherTexto("detalhe-cor", `Cor: ${projeto.cor || "Não informada"}`);
        preencherTexto("detalhe-previsao", formatarData(projeto.prazo));

        const progresso = document.getElementById("detalhe-progresso");
        const indiceAtual = etapasAACDLista.indexOf(projeto.etapaAtual);

        const porcentagem =
            indiceAtual >= 0
                ? indiceAtual / (etapasAACDLista.length - 1) * 100
                : 0;

        progresso.style.setProperty("--progresso", `${porcentagem}%`);

        progresso.querySelectorAll("li").forEach((etapa, indice) => {
            etapa.classList.remove("completed", "current");
            etapa.removeAttribute("aria-current");

            if (indice < indiceAtual) {
                etapa.classList.add("completed");
            } else if (indice === indiceAtual) {
                etapa.classList.add("current");
                etapa.setAttribute("aria-current", "step");
            }
        });

        const listaHistorico = document.getElementById("detalhe-historico");
        listaHistorico.replaceChildren();

        const historico = projeto.historico || [{
            data: formatarData(projeto.prazo),
            titulo: "Projeto cadastrado na plataforma",
            descricao: "Histórico detalhado ainda não disponível."
        }];

        historico.forEach(evento => {
            const item = criar("li");
            const data = criar("span", "projetos-details__history-date", evento.data);
            const info = criar("div", "projetos-details__history-info");

            info.append(
                criar("strong", "", evento.titulo),
                criar("span", "", evento.descricao)
            );

            item.append(data, info);
            listaHistorico.appendChild(item);
        });

        abrirModal(modalDetalhes);
    }

    

    lista.addEventListener("click", event => {
        const botao = event.target.closest("[data-action]");
        if (!botao) return;

        const id = botao.dataset.id;

        if (botao.dataset.action === "detalhes") {
            abrirDetalhes(id);
            return;
        }

        if (botao.dataset.action === "menu") {
            const menu = botao.parentElement.querySelector(".projetos-aacd__menu");
            const abrir = menu.hidden;

            lista.querySelectorAll(".projetos-aacd__menu").forEach(m => {
                m.hidden = true;
            });

            lista.querySelectorAll(".projetos-aacd__menu-button").forEach(b => {
                b.setAttribute("aria-expanded", "false");
            });

            menu.hidden = !abrir;
            botao.setAttribute("aria-expanded", String(abrir));
        }
    });

    document.addEventListener("click", event => {
        if (!pagina.isConnected) return;
        if (event.target.closest(".projetos-aacd__card-actions")) return;

        lista.querySelectorAll(".projetos-aacd__menu").forEach(menu => {
            menu.hidden = true;
        });

        lista.querySelectorAll(".projetos-aacd__menu-button").forEach(botao => {
            botao.setAttribute("aria-expanded", "false");
        });
    });

    

    const descricao = document.getElementById("projeto-descricao");
    const contador = document.getElementById("contador-descricao");
    const arquivoInput = document.getElementById("projeto-arquivo");

    function atualizarContadorDescricao() {
        contador.textContent = `${descricao.value.length}/280 caracteres`;
    }

    descricao.addEventListener("input", atualizarContadorDescricao);

    arquivoInput.addEventListener("change", () => {
        const arquivo = arquivoInput.files[0];

        document.getElementById("nome-arquivo").textContent =
            arquivo ? arquivo.name : "";
    });

    form.addEventListener("submit", event => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const dados = new FormData(form);

        const proximoId = String(
            Math.max(...projetosAACDLista.map(p => Number(p.id))) + 1
        ).padStart(3, "0");

        const novoProjeto = {
            id: proximoId,
            nome: String(dados.get("nome")).trim(),
            quantidade: Number(dados.get("quantidade")),
            categoria: String(dados.get("categoria")),
            material: String(dados.get("material")).trim(),
            tecnologia: "FDM",
            descricao: String(dados.get("descricao")).trim(),
            informacoesTecnicas: String(dados.get("informacoesTecnicas")),
            prazo: String(dados.get("prazo")),
            prioridade: String(dados.get("prioridade")),
            cidade: "Localização não informada",
            dataTexto: "Cadastrado agora",
            status: "aguardando",
            etapaAtual: "Recebido",
            arquivoNome: arquivoInput.files[0]?.name || null
        };

        projetosAACDLista.unshift(novoProjeto);

        filtroAtual = "todos";
        busca.value = "";

        abas.forEach(aba => {
            const ativa = aba.dataset.filter === "todos";
            aba.classList.toggle("active", ativa);
            aba.setAttribute("aria-pressed", String(ativa));
        });

        renderizarProjetos();
        fecharModal();
        form.reset();
        atualizarContadorDescricao();

        alert(`Projeto #${novoProjeto.id} adicionado nesta demonstração!`);
    });

    

    pagina.querySelectorAll("[data-filter]").forEach(aba => {
        aba.setAttribute(
            "aria-pressed",
            String(aba.dataset.filter === filtroAtual)
        );
    });

    document.addEventListener("keydown", event => {
        if (!modalAberto || event.key !== "Escape") return;
        fecharModal();
    });

    
    document.addEventListener("keydown", event => {
        if (!modalAberto || event.key !== "Tab") return;

        const elementos = Array.from(
            modalAberto.querySelectorAll(
                "button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), a[href]"
            )
        ).filter(elemento => elemento.getClientRects().length > 0);

        if (!elementos.length) return;

        const primeiro = elementos[0];
        const ultimo = elementos[elementos.length - 1];

        if (event.shiftKey && document.activeElement === primeiro) {
            event.preventDefault();
            ultimo.focus();
        } else if (!event.shiftKey && document.activeElement === ultimo) {
            event.preventDefault();
            primeiro.focus();
        } else if (!elementos.includes(document.activeElement)) {
            event.preventDefault();
            primeiro.focus();
        }
    });

    renderizarProjetos();
};
