const modalDetalhes = document.getElementById('modal-detalhes');
const modalForm = document.getElementById('modal-form');
const form = document.getElementById('form-impressora');

const ESTADOS = {
    online:   { texto: 'Online',      ponto: 'ponto--disponivel' },
    producao: { texto: 'Em produção', ponto: 'ponto--uso' },
    pausada:  { texto: 'Pausada',     ponto: 'ponto--pausada' },
};

let impressoraAtual = null; 

const mm = (n) => `${n} mm`;

function abrirDetalhes(botao) {
    const d = botao.dataset;
    impressoraAtual = botao;

    const estado = ESTADOS[d.estado];
    const total = (d.largura * d.altura * d.profundidade) / 1000; 

    document.getElementById('detalhes-titulo').textContent = d.nome;
    document.getElementById('det-tecnologia').textContent  = d.tecnologia;
    document.getElementById('det-modelo').textContent      = d.modelo;
    document.getElementById('det-estado').textContent      = estado.texto;
    document.getElementById('det-ponto').className         = `ponto ${estado.ponto}`;
    document.getElementById('det-filamentos').textContent  = d.filamentos;
    document.getElementById('det-largura').textContent     = mm(d.largura);
    document.getElementById('det-altura').textContent      = mm(d.altura);
    document.getElementById('det-profundidade').textContent = mm(d.profundidade);
    document.getElementById('det-total').textContent       = `${total.toLocaleString('pt-BR')} cm³`;

    modalDetalhes.showModal();
}

document.querySelectorAll('[data-abrir-detalhes]').forEach((botao) => {
    botao.addEventListener('click', () => abrirDetalhes(botao));
});

const resumoFilamentos = document.getElementById('resumo-filamentos');
const checksFilamentos = form.querySelectorAll('input[name="filamentos"]');

function atualizarResumoFilamentos() {
    const marcados = [...checksFilamentos].filter((c) => c.checked).map((c) => c.value);
    resumoFilamentos.textContent = marcados.length ? marcados.join(', ') : 'Selecione os filamentos';
}
checksFilamentos.forEach((c) => c.addEventListener('change', atualizarResumoFilamentos));

function abrirForm(modo, botao) {
    const editando = modo === 'editar';

    form.reset();
    document.getElementById('dropdown-filamentos').open = false;

    document.getElementById('form-titulo').textContent = editando ? 'Editar impressora' : 'Adicionar impressora';
    document.getElementById('btn-enviar').textContent  = editando ? 'Salvar alterações' : '+ Adicionar impressora';
    form.dataset.modo = modo;

    if (editando) {
        const d = botao.dataset;
        const lista = d.filamentos.split(',').map((f) => f.trim());

        form.nome.value         = d.nome;
        form.tecnologia.value   = d.tecnologia;
        form.modelo.value       = d.modelo;
        form.estado.value       = d.estado;
        form.largura.value      = d.largura;
        form.altura.value       = d.altura;
        form.profundidade.value = d.profundidade;
        checksFilamentos.forEach((c) => { c.checked = lista.includes(c.value); });
    }

    atualizarResumoFilamentos();
    modalForm.showModal();
}

document.querySelector('[data-abrir-form="adicionar"]').addEventListener('click', () => abrirForm('adicionar'));

document.getElementById('btn-editar').addEventListener('click', () => {
    modalDetalhes.close();
    abrirForm('editar', impressoraAtual);
});

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const dados = {
        nome: form.nome.value,
        tecnologia: form.tecnologia.value,
        modelo: form.modelo.value,
        estado: form.estado.value,
        filamentos: [...checksFilamentos].filter((c) => c.checked).map((c) => c.value),
        largura: form.largura.value,
        altura: form.altura.value,
        profundidade: form.profundidade.value,
    };
    
    console.log(form.dataset.modo, dados);

    modalForm.close();
});

document.getElementById('btn-excluir').addEventListener('click', () => {
    if (confirm('Tem certeza que deseja excluir esta impressora?')) {
        console.log('excluir', impressoraAtual.dataset.nome);
        modalDetalhes.close();
    }
});

document.querySelectorAll('.modal').forEach((modal) => {
    modal.querySelector('[data-fechar]').addEventListener('click', () => modal.close());

    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.close();
    });
});