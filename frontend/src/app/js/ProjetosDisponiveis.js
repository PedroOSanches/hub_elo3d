const modal = document.getElementById('modal-projeto');
 
const campos = {
    titulo:      document.getElementById('modal-titulo'),
    prazo:       document.getElementById('modal-prazo'),
    material:    document.getElementById('modal-material'),
    processo:    document.getElementById('modal-processo'),
    tipo:        document.getElementById('modal-tipo'),
    equipamento: document.getElementById('modal-equipamento'),
    arquivoNome: document.getElementById('modal-arquivo-nome'),
    arquivoLink: document.getElementById('modal-arquivo'),
};
 
document.querySelectorAll('[data-abrir-modal]').forEach((botao) => {
    botao.addEventListener('click', () => {
        const d = botao.dataset;
 
        campos.titulo.textContent      = d.titulo;
        campos.prazo.textContent       = d.prazo;
        campos.material.textContent    = d.material;
        campos.processo.textContent    = d.processo;
        campos.tipo.textContent        = d.tipo;
        campos.equipamento.textContent = d.equipamento;
        campos.arquivoNome.textContent = d.arquivo;
        campos.arquivoLink.href        = d.arquivoUrl || '#';
 
        modal.showModal();
    });
});
 
modal.querySelector('[data-fechar-modal]').addEventListener('click', () => modal.close());
 
modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.close();
});