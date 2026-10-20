
const etapasProjeto = [
    "Recebido",
    "Produção",
    "Finalização",
    "Entrega"
];


const projetos = [
    { id: "016", etapaAtual: "Finalização" },
    { id: "017", etapaAtual: "Produção" },
    { id: "018", etapaAtual: "Recebido" }
];


const cardsProjetos = document.querySelectorAll(
    ".aacd-dashboard__project-card"
);


cardsProjetos.forEach((card, indice) => {
    const projeto = projetos[indice];

    if (!projeto) return;

    
    const indiceEtapa = etapasProjeto.indexOf(projeto.etapaAtual);

    if (indiceEtapa === -1) return;

    
    const porcentagem =
        (indiceEtapa / (etapasProjeto.length - 1)) * 100;

  
    const barra = card.querySelector(".aacd-dashboard__progress");

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
