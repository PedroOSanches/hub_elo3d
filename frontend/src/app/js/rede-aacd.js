
const parceirosRedeAACD = [
    {
        id: "001",
        nome: "FabLab Mauá",
        cidade: "São Caetano do Sul - SP",
        endereco: "Av. Barão de Mauá, 1681, Jardim Pedroso, São Caetano do Sul - SP",
        anoParceria: 2026,
        telefone: "(11) 4239-3000",
        email: "ana.silva@maua.br",
        impressoras: 8,
        projetosAtivos: 5,
        projetos: [
            { nome: "Órtese de punho", adocao: "24/09/2026", conclusao: "—" },
            { nome: "Suporte de caneta adaptado", adocao: "09/09/2026", conclusao: "—" },
            { nome: "Adaptador de colher", adocao: "15/08/2026", conclusao: "22/09/2026" },
            { nome: "Prótese transtibial", adocao: "12/08/2026", conclusao: "—" }
        ]
    },
    {
        id: "002",
        nome: "Laboratório de Impressão ABC",
        cidade: "São Caetano do Sul - SP",
        endereco: "São Caetano do Sul - SP",
        anoParceria: 2026,
        telefone: "(11) 99999-9999",
        email: "contato@laboratorioabc.com.br",
        impressoras: 3,
        projetosAtivos: 0,
        projetos: [
            { nome: "Órtese de joelho", adocao: "10/08/2026", conclusao: "22/08/2026" },
            { nome: "Adaptador de talher", adocao: "05/09/2026", conclusao: "18/09/2026" }
        ]
    },
    {
        id: "003",
        nome: "FabLab Santo André",
        cidade: "Santo André - SP",
        endereco: "Santo André - SP",
        anoParceria: 2026,
        telefone: "(11) 98888-8888",
        email: "contato@fablabsantoandre.com.br",
        impressoras: 6,
        projetosAtivos: 5,
        projetos: [
            { nome: "Prótese de mão", adocao: "14/09/2026", conclusao: "—" },
            { nome: "Órtese de tornozelo", adocao: "20/09/2026", conclusao: "—" },
            { nome: "Suporte adaptado", adocao: "25/09/2026", conclusao: "—" }
        ]
    },
    {
        id: "004",
        nome: "Centro de Prototipagem Mauá",
        cidade: "São Bernardo do Campo - SP",
        endereco: "São Bernardo do Campo - SP",
        anoParceria: 2026,
        telefone: "(11) 97777-7777",
        email: "contato@prototipagemmaua.com.br",
        impressoras: 5,
        projetosAtivos: 5,
        projetos: [
            { nome: "Órtese de punho", adocao: "01/10/2026", conclusao: "—" },
            { nome: "Corset toracolombar", adocao: "04/10/2026", conclusao: "—" },
            { nome: "Adaptador de escova", adocao: "08/10/2026", conclusao: "—" }
        ]
    }
];

window.initRedeAACD = function () {
    const pagina = document.querySelector(".rede-aacd");
    const lista = document.getElementById("rede-lista-parceiros");
    const busca = document.getElementById("rede-busca");
    const vazio = document.getElementById("rede-sem-resultados");
    const modal = document.getElementById("rede-modal-parceiro");

    if (!pagina || !lista || !busca || !vazio || !modal) return;

    if (pagina.dataset.inicializada === "true") return;
    pagina.dataset.inicializada = "true";

    const conteudoModal = modal.querySelector(".rede-aacd-modal__content");
    const botaoFechar = modal.querySelector(".rede-aacd-modal__close");

    let focoAnterior = null;
    let overflowAnterior = "";

    const icones = {
        localizacao: `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                 aria-hidden="true">
                <path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/>
                <circle cx="12" cy="10" r="2.5"/>
            </svg>
        `,
        calendario: `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                 aria-hidden="true">
                <rect x="3" y="5" width="18" height="16" rx="3"/>
                <path d="M7 3v4M17 3v4M3 10h18"/>
            </svg>
        `,
        telefone: `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                 aria-hidden="true">
                <path d="M6.5 3.5 10 7l-2 3a17 17 0 0 0 6 6l3-2 3.5 3.5
                         a2 2 0 0 1-.5 3A18 18 0 0 1 3.5 4
                         a2 2 0 0 1 3-.5Z"/>
            </svg>
        `
    };

    function criarElemento(tag, classe = "", texto = null) {
        const elemento = document.createElement(tag);

        if (classe) elemento.className = classe;
        if (texto !== null) elemento.textContent = texto;

        return elemento;
    }

    function criarMeta(icone, texto) {
        const linha = criarElemento("div", "rede-aacd__meta-row");
        const simbolo = criarElemento("span");
        const descricao = criarElemento("span", "", texto);

        simbolo.innerHTML = icones[icone];
        simbolo.setAttribute("aria-hidden", "true");

        linha.append(simbolo, descricao);

        return linha;
    }

    function fecharMenus() {
        lista.querySelectorAll(".rede-aacd__menu").forEach(menu => {
            menu.hidden = true;
        });

        lista.querySelectorAll(".rede-aacd__menu-button").forEach(botao => {
            botao.setAttribute("aria-expanded", "false");
        });
    }

    function criarCard(parceiro) {
        const card = criarElemento("article", "rede-aacd__card");
        card.dataset.id = parceiro.id;

        const faixa = criarElemento("div", "rede-aacd__card-accent");

        const nome = criarElemento("div", "rede-aacd__card-name");
        nome.appendChild(criarElemento("h2", "", parceiro.nome));

        const meta = criarElemento("div", "rede-aacd__card-meta");

        meta.append(
            criarMeta("localizacao", parceiro.cidade),
            criarMeta("calendario", `Parceiro desde ${parceiro.anoParceria}`),
            criarMeta("telefone", parceiro.telefone)
        );

        const statusContainer = criarElemento("div", "rede-aacd__card-status");

        const classeStatus = parceiro.projetosAtivos === 0
            ? "rede-aacd__status rede-aacd__status--inactive"
            : "rede-aacd__status";

        const quantidade = String(parceiro.projetosAtivos).padStart(2, "0");

        const status = criarElemento(
            "span",
            classeStatus,
            `${quantidade} projetos ativos`
        );

        statusContainer.appendChild(status);

        const acoes = criarElemento("div", "rede-aacd__card-actions");

        const botaoMenu = criarElemento("button", "rede-aacd__menu-button");
        botaoMenu.type = "button";
        botaoMenu.dataset.action = "menu";
        botaoMenu.dataset.id = parceiro.id;
        botaoMenu.setAttribute("aria-label", `Ações de ${parceiro.nome}`);
        botaoMenu.setAttribute("aria-expanded", "false");
        botaoMenu.setAttribute("aria-haspopup", "true");

        const menu = criarElemento("div", "rede-aacd__menu");
        menu.hidden = true;

        const botaoDetalhes = criarElemento("button", "", "Ver parceiro");
        botaoDetalhes.type = "button";
        botaoDetalhes.dataset.action = "detalhes";
        botaoDetalhes.dataset.id = parceiro.id;

        menu.appendChild(botaoDetalhes);
        acoes.append(botaoMenu, menu);

        card.append(faixa, nome, meta, statusContainer, acoes);

        return card;
    }

    function renderizarParceiros() {
        const termo = busca.value.trim().toLocaleLowerCase("pt-BR");

        const filtrados = parceirosRedeAACD.filter(parceiro => {
            const texto = [
                parceiro.nome,
                parceiro.cidade,
                parceiro.endereco,
                parceiro.email
            ].join(" ").toLocaleLowerCase("pt-BR");

            return texto.includes(termo);
        });

        fecharMenus();
        lista.replaceChildren();

        filtrados.forEach(parceiro => {
            lista.appendChild(criarCard(parceiro));
        });

        vazio.hidden = filtrados.length !== 0;
    }

    function preencherTexto(id, valor) {
        const elemento = document.getElementById(id);

        if (elemento) {
            elemento.textContent = valor ?? "—";
        }
    }

    function abrirModal() {
        focoAnterior = document.activeElement;
        overflowAnterior = document.body.style.overflow;

        modal.hidden = false;
        document.body.style.overflow = "hidden";

        fecharMenus();

        botaoFechar.focus();
    }

    function fecharModal() {
        if (modal.hidden) return;

        modal.hidden = true;
        document.body.style.overflow = overflowAnterior;

        if (focoAnterior && focoAnterior.isConnected) {
            focoAnterior.focus();
        }
    }

    function preencherTabela(projetos) {
        const corpo = document.getElementById("rede-parceiro-projetos");
        const aviso = document.getElementById("rede-parceiro-sem-projetos");

        if (!corpo || !aviso) return;

        corpo.replaceChildren();

        projetos.forEach(projeto => {
            const linha = document.createElement("tr");

            [
                projeto.nome,
                projeto.adocao,
                projeto.conclusao || "—"
            ].forEach(valor => {
                linha.appendChild(criarElemento("td", "", valor));
            });

            corpo.appendChild(linha);
        });

        aviso.hidden = projetos.length > 0;
    }

    function abrirDetalhes(id) {
        const parceiro = parceirosRedeAACD.find(item => item.id === id);

        if (!parceiro) return;

        preencherTexto("rede-parceiro-nome", parceiro.nome);
        preencherTexto("rede-parceiro-endereco", parceiro.endereco);
        preencherTexto(
            "rede-parceiro-impressoras",
            String(parceiro.impressoras).padStart(2, "0")
        );
        preencherTexto("rede-parceiro-telefone", parceiro.telefone);
        preencherTexto("rede-parceiro-email", parceiro.email);

        preencherTabela(parceiro.projetos);

        abrirModal();
    }

    busca.addEventListener("input", renderizarParceiros);

    lista.addEventListener("click", event => {
        const botao = event.target.closest("[data-action]");

        if (!botao || !lista.contains(botao)) return;

        const id = botao.dataset.id;

        if (botao.dataset.action === "detalhes") {
            abrirDetalhes(id);
            return;
        }

        if (botao.dataset.action === "menu") {
            const menu = botao.parentElement.querySelector(".rede-aacd__menu");

            if (!menu) return;

            const deveAbrir = menu.hidden;

            fecharMenus();

            menu.hidden = !deveAbrir;
            botao.setAttribute("aria-expanded", String(deveAbrir));
        }
    });

    document.addEventListener("click", event => {
        if (!pagina.isConnected) return;

        if (!event.target.closest(".rede-aacd__card-actions")) {
            fecharMenus();
        }
    });

    modal.querySelectorAll("[data-rede-fechar]").forEach(elemento => {
        elemento.addEventListener("click", fecharModal);
    });

    document.addEventListener("keydown", event => {
        if (!pagina.isConnected) return;

        if (event.key === "Escape") {
            if (!modal.hidden) {
                fecharModal();
            } else {
                fecharMenus();
            }
        }

        if (event.key !== "Tab" || modal.hidden) return;

        const elementos = Array.from(
            conteudoModal.querySelectorAll(
                'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
            )
        ).filter(elemento => elemento.getClientRects().length > 0);

        if (!elementos.length) {
            event.preventDefault();
            conteudoModal.focus();
            return;
        }

        const primeiro = elementos[0];
        const ultimo = elementos[elementos.length - 1];

        if (event.shiftKey && document.activeElement === primeiro) {
            event.preventDefault();
            ultimo.focus();
        } else if (!event.shiftKey && document.activeElement === ultimo) {
            event.preventDefault();
            primeiro.focus();
        } else if (!conteudoModal.contains(document.activeElement)) {
            event.preventDefault();
            primeiro.focus();
        }
    });

    renderizarParceiros();
};
