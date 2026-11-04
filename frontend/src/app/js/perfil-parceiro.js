async function initPerfilParceiro() {
    const valoresContato = document
        .querySelector('section[aria-labelledby="titulo-contato"]')
        .querySelectorAll('dd');

    const contactResponse = await fetch('pages/components/contato-modal.html');
    if (!contactResponse.ok) {
        throw new Error('Não foi possível carregar o modal de contato.');
    }

    document.getElementById('app').insertAdjacentHTML(
        'beforeend',
        await contactResponse.text()
    );

    if (!document.getElementById('contato-modal-style')) {
        const contactStyle = document.createElement('link');
        contactStyle.id = 'contato-modal-style';
        contactStyle.rel = 'stylesheet';
        contactStyle.href = 'style/components/contato-modal.css';
        document.head.appendChild(contactStyle);
    }

    const modalContato = document.getElementById('modal-contato');
    const formContato = document.getElementById('form-contato');

    document.querySelector('[data-open-contato]').addEventListener('click', () => {
        formContato.nome.value = valoresContato[0].textContent.trim();
        formContato.email.value = valoresContato[1].textContent.trim();
        formContato.telefone.value = valoresContato[2].textContent.trim();
        modalContato.showModal();
    });

    formContato.addEventListener('submit', (event) => {
        event.preventDefault();
        valoresContato[0].textContent = formContato.nome.value;
        valoresContato[1].textContent = formContato.email.value;
        valoresContato[2].textContent = formContato.telefone.value;
        modalContato.close();
    });

    modalContato.querySelectorAll('[data-fechar-contato]').forEach((button) => {
        button.addEventListener('click', () => modalContato.close());
    });

    modalContato.querySelector('[data-salvar-contato]')?.addEventListener(
        'click',
        () => formContato.requestSubmit()
    );

    modalContato.addEventListener('click', (event) => {
        if (event.target === modalContato) modalContato.close();
    });

    const addressResponse = await fetch('pages/components/endereco-modal.html');
    if (!addressResponse.ok) {
        throw new Error('Não foi possível carregar o modal de endereço.');
    }

    document.getElementById('app').insertAdjacentHTML(
        'beforeend',
        await addressResponse.text()
    );

    if (!document.getElementById('endereco-modal-style')) {
        const addressStyle = document.createElement('link');
        addressStyle.id = 'endereco-modal-style';
        addressStyle.rel = 'stylesheet';
        addressStyle.href = 'style/components/endereco-modal.css';
        document.head.appendChild(addressStyle);
    }

    const modalEndereco = document.getElementById('modal-endereco');
    const formEndereco = document.getElementById('form-endereco');
    const valoresEndereco = document
        .querySelector('section[aria-labelledby="titulo-endereco"]')
        .querySelectorAll('dd');

    const abrirEndereco = () => {
        formEndereco.cep.value = valoresEndereco[3].textContent.trim();
        formEndereco.endereco.value = valoresEndereco[0].textContent.trim();
        formEndereco.bairro.value = valoresEndereco[1].textContent.trim();
        formEndereco.cidade.value = valoresEndereco[2].textContent.trim();
        modalEndereco.showModal();
    };

    document.querySelector('[data-open-endereco]').addEventListener('click', abrirEndereco);
    modalEndereco.querySelectorAll('[data-fechar-endereco]').forEach((button) => {
        button.addEventListener('click', () => modalEndereco.close());
    });
    modalEndereco.querySelector('[data-salvar-endereco]')?.addEventListener(
        'click',
        () => formEndereco.requestSubmit()
    );

    formEndereco.addEventListener('submit', (event) => {
        event.preventDefault();
        valoresEndereco[3].textContent = formEndereco.cep.value;
        valoresEndereco[0].textContent = formEndereco.endereco.value;
        valoresEndereco[1].textContent = formEndereco.bairro.value;
        valoresEndereco[2].textContent = formEndereco.cidade.value;
        modalEndereco.close();
    });

    modalEndereco.addEventListener('click', (event) => {
        if (event.target === modalEndereco) modalEndereco.close();
    });
}

window.initPerfilParceiro = initPerfilParceiro;