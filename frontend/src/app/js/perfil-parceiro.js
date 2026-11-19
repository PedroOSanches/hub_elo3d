async function initPerfilParceiro() {
    const userResponse = await window.apiFetch(
        `${window.ENV.API_BASE_URL}/auth/me`
    );
    if (!userResponse.ok) {
        throw new Error('Não foi possível identificar o usuário autenticado.');
    }

    const sessionUser = await userResponse.json();
    const response = await window.apiFetch(
        `${window.ENV.API_BASE_URL}/user/get_user/${encodeURIComponent(sessionUser.user_id)}`
    );
    if (!response.ok) {
        throw new Error('Não foi possível carregar os dados do usuário.');
    }

    const user = await response.json();
    const userId = user.user_id;
    const originalEmail = user.email || '';
    const address = user.address || {};
    const values = {
        address: [address.street, address.number].filter(Boolean).join(', '),
        neighborhood: address.neighborhood || '',
        'city-state': [address.city, address.state].filter(Boolean).join(' - '),
        cep: address.cep || '',
        name: user.name || '',
        email: originalEmail,
        phone: user.phone || '',
    };

    document.querySelectorAll('[data-profile-field]').forEach((element) => {
        const field = element.dataset.profileField;
        element.textContent = values[field] || 'Não informado';
    });

    const valoresContato = document
        .querySelector('section[aria-labelledby="titulo-contato"]')
        .querySelectorAll('dd');

    const updateUser = async (payload) => {
        const updateResponse = await window.apiFetch(
            `${window.ENV.API_BASE_URL}/user/update_user`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, ...payload }),
            }
        );

        const body = await updateResponse.json().catch(() => ({}));
        if (!updateResponse.ok) {
            const detail = Array.isArray(body.detail)
                ? body.detail.map((item) => item.msg).join(' ')
                : body.detail || body.message;
            throw new Error(detail || 'Não foi possível atualizar o perfil.');
        }

        return body;
    };

    const normalizePhone = (value) => {
        const digits = value.replace(/\D/g, '');
        return digits.startsWith('55') ? `+${digits}` : `+55${digits}`;
    };

    const showUpdateError = (error) => {
        console.error(error);
        window.alert(error instanceof Error
            ? error.message
            : 'Não foi possível atualizar o perfil.');
    };

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
    formContato.email.disabled = true;
    modalContato.querySelector('[data-email-bloqueado]').addEventListener(
        'click',
        () => window.alert('O e-mail não pode ser alterado.')
    );

    document.querySelector('[data-open-contato]').addEventListener('click', () => {
        formContato.nome.value = valoresContato[0].textContent.trim();
        formContato.email.value = valoresContato[1].textContent.trim();
        formContato.telefone.value = valoresContato[2].textContent.trim();
        modalContato.showModal();
    });

    formContato.addEventListener('submit', async (event) => {
        event.preventDefault();
        try {
            const updatedUser = await updateUser({
                new_name: formContato.nome.value.trim(),
                new_phone: normalizePhone(formContato.telefone.value),
            });
            valoresContato[0].textContent = updatedUser.name;
            valoresContato[1].textContent = originalEmail;
            valoresContato[2].textContent = updatedUser.phone;
            modalContato.close();
        } catch (error) {
            showUpdateError(error);
        }
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

    formEndereco.addEventListener('submit', async (event) => {
        event.preventDefault();
        const [city, state = ''] = formEndereco.cidade.value
            .split(/\s*-\s*/, 2)
            .map((value) => value.trim());

        try {
            const updatedUser = await updateUser({
                address: {
                    new_street: formEndereco.endereco.value.trim(),
                    new_number: address.number || '',
                    new_neighborhood: formEndereco.bairro.value.trim(),
                    new_city: city,
                    new_state: state,
                    new_cep: formEndereco.cep.value.trim(),
                },
            });
            const updatedAddress = updatedUser.address;
            valoresEndereco[3].textContent = updatedAddress.cep;
            valoresEndereco[0].textContent =
                `${updatedAddress.street}, ${updatedAddress.number}`;
            valoresEndereco[1].textContent = updatedAddress.neighborhood;
            valoresEndereco[2].textContent =
                `${updatedAddress.city} - ${updatedAddress.state}`;
            modalEndereco.close();
        } catch (error) {
            showUpdateError(error);
        }
    });

    modalEndereco.addEventListener('click', (event) => {
        if (event.target === modalEndereco) modalEndereco.close();
    });
}

window.initPerfilParceiro = initPerfilParceiro;