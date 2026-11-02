const modalContato = document.getElementById('modal-contato');
const formContato  = document.getElementById('form-contato');

const valoresContato = document
    .querySelector('section[aria-labelledby="titulo-contato"]')
    .querySelectorAll('dd');

document.querySelector('[data-editar="contato"]').addEventListener('click', () => {
    formContato.nome.value     = valoresContato[0].textContent.trim();
    formContato.email.value    = valoresContato[1].textContent.trim();
    formContato.telefone.value = valoresContato[2].textContent.trim();

    modalContato.showModal();
});

formContato.addEventListener('submit', (e) => {
    e.preventDefault();


    valoresContato[0].textContent = formContato.nome.value;
    valoresContato[1].textContent = formContato.email.value;
    valoresContato[2].textContent = formContato.telefone.value;

    modalContato.close();
});

modalContato.querySelectorAll('[data-fechar]').forEach((botao) => {
    botao.addEventListener('click', () => modalContato.close());
});

modalContato.addEventListener('click', (e) => {
    if (e.target === modalContato) modalContato.close();
});