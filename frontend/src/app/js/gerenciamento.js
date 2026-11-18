async function initGerenciamento() {
  const sessionResponse = await window.apiFetch(
    `${window.ENV.API_BASE_URL}/auth/me`
  );
  if (!sessionResponse.ok) {
    throw new Error('Não foi possível validar a permissão do usuário.');
  }

  const sessionUser = await sessionResponse.json();
  const role = sessionUser.role || window.getUserRole?.() || '';
  const isHospitalUser = role.toLowerCase() === 'user_hospital';
  const currentUserResponse = await window.apiFetch(
    `${window.ENV.API_BASE_URL}/user/get_user/${encodeURIComponent(sessionUser.user_id)}`
  );
  if (!currentUserResponse.ok) {
    throw new Error('Não foi possível carregar os dados da instituição.');
  }
  const currentUser = await currentUserResponse.json();
  const institutionId = currentUser.institution_id || null;
  const institutionAddress = currentUser.address;
  let members = [
    {
      name: 'Ana Carolina da Silva',
      email: 'anacarolina@aacd.org.br',
      phone: '(11) 999999999',
    },
    {
      name: 'Roberto Silveira da Costa',
      email: 'robertosilveira@aacd.org.br',
      phone: '(11) 999999999',
    },
  ];
  const membersResponse = await window.apiFetch(
    `${window.ENV.API_BASE_URL}/user/get_all_users`
  );
  if (!membersResponse.ok) {
    throw new Error('Não foi possível carregar os membros da instituição.');
  }
  const allUsers = await membersResponse.json();
  members = allUsers
    .filter((user) => user.role === 'user_hospital'
      && (!institutionId || user.institution_id === institutionId))
    .map((user) => ({
      userId: user.user_id,
      name: user.name,
      email: user.email,
      phone: user.phone,
    }));

  const list = document.getElementById('member-list');
  const search = document.getElementById('member-search');
  const addButton = document.querySelector('.team-page__add');
  if (isHospitalUser) {
    addButton?.remove();
  }

  const modalResponse = await fetch('pages/components/membro-modal.html');
  if (!modalResponse.ok) {
    throw new Error('Não foi possível carregar o modal de membro.');
  }

  document.getElementById('app').insertAdjacentHTML(
    'beforeend',
    await modalResponse.text()
  );

  if (!document.getElementById('membro-modal-style')) {
    const modalStyle = document.createElement('link');
    modalStyle.id = 'membro-modal-style';
    modalStyle.rel = 'stylesheet';
    modalStyle.href = 'style/components/membro-modal.css?v=3';
    document.head.appendChild(modalStyle);
  }

  const modal = document.getElementById('member-modal');
  const form = document.getElementById('member-form');
  const modalTitle = document.getElementById('member-modal-title');
  const passwordField = document.getElementById('member-password-field');
  const passwordInput = document.getElementById('member-password');
  const emailInput = form.elements.email;
  const message = document.getElementById('member-form-message');
  const submitButton = modal.querySelector('[data-submit-member]');
  let editingMember = null;

  function setButtonText(button, text) {
    const textElement = button?.shadowRoot?.querySelector('.custom-btn span');
    if (textElement) textElement.textContent = text;
  }

  function openMemberModal(member = null) {
    editingMember = member;
    form.reset();
    message.hidden = true;
    message.textContent = '';
    modalTitle.textContent = member ? 'Editar membro' : 'Adicionar membro';
    setButtonText(submitButton, member ? 'Salvar' : 'Adicionar');
    passwordField.hidden = Boolean(member);
    passwordInput.required = !member;
    emailInput.readOnly = Boolean(member);

    if (member) {
      form.elements.name.value = member.name;
      form.elements.email.value = member.email;
      form.elements.phone.value = member.phone;
    }

    modal.showModal();
  }

  function renderMembers(query = '') {
    const normalizedQuery = query.trim().toLowerCase();
    list.replaceChildren(...members
      .filter((member) => `${member.name} ${member.email}`.toLowerCase().includes(normalizedQuery))
      .map((member) => {
        const element = document.createElement('team-member');
        element.setAttribute('user-id', member.userId || '');
        element.setAttribute('name', member.name);
        element.setAttribute('email', member.email);
        element.setAttribute('phone', member.phone);
        if (isHospitalUser) element.setAttribute('readonly', '');
        return element;
      }));
  }

  search.addEventListener('input', () => renderMembers(search.value));

  addButton?.addEventListener('click', () => {
    openMemberModal();
  });

  modal.querySelectorAll('[data-close-member-modal]').forEach((button) => {
    button.addEventListener('click', () => {
      editingMember = null;
      modal.close();
    });
  });

  modal.querySelector('[data-submit-member]')?.addEventListener(
    'click',
    () => form.requestSubmit()
  );

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const updatedMember = {
      name: data.get('name'),
      email: data.get('email'),
      phone: data.get('phone'),
    };

    if (editingMember) {
      if (!editingMember.userId) {
        message.textContent = 'Não foi possível identificar o membro para atualização.';
        message.hidden = false;
        return;
      }

      const response = await window.apiFetch(
        `${window.ENV.API_BASE_URL}/user/update_user`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: editingMember.userId,
            new_name: updatedMember.name,
            new_phone: updatedMember.phone,
          }),
        }
      );

      if (!response.ok) {
        let errorMessage = 'Não foi possível atualizar o membro.';
        try {
          const error = await response.json();
          errorMessage = error.detail
            ? (typeof error.detail === 'string'
              ? error.detail
              : JSON.stringify(error.detail))
            : errorMessage;
        } catch {
          // Keep the generic message when the API does not return JSON.
        }
        message.textContent = errorMessage;
        message.hidden = false;
        return;
      }

      Object.assign(editingMember, {
        name: updatedMember.name,
        phone: updatedMember.phone,
      });
      renderMembers(search.value);
      modal.close();
      editingMember = null;
      return;
    }

    const request = {
      name: data.get('name'),
      email: data.get('email'),
      password: data.get('password'),
      phone: data.get('phone'),
      role: 'user_hospital',
      institution_id: institutionId,
      address: institutionAddress,
    };

    const response = await window.apiFetch(
      `${window.ENV.API_BASE_URL}/user/create`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      }
    );

    if (!response.ok) {
      let errorMessage = 'Não foi possível adicionar o membro.';
      try {
        const error = await response.json();
        errorMessage = error.detail
          ? (typeof error.detail === 'string'
            ? error.detail
            : JSON.stringify(error.detail))
          : errorMessage;
      } catch {
        // Keep the generic message when the API does not return JSON.
      }
      message.textContent = errorMessage;
      message.hidden = false;
      return;
    }

    const createdUser = await response.json();
    members.push({
      ...updatedMember,
      userId: createdUser.user_id,
    });
    renderMembers(search.value);
    modal.close();
    editingMember = null;
  });

  modal.addEventListener('click', (event) => {
    if (event.target === modal) {
      editingMember = null;
      modal.close();
    }
  });

  list.addEventListener('member-edit', (event) => {
    const member = members.find((item) => item.userId === event.detail.userId);
    if (member) openMemberModal(member);
  });

  list.addEventListener('member-delete', async (event) => {
    const member = members.find((item) => item.userId === event.detail.userId);
    if (!member?.userId) {
      message.textContent = 'Não foi possível identificar o membro para exclusão.';
      message.hidden = false;
      return;
    }

    if (!window.confirm(`Deseja excluir o membro ${member.name}?`)) {
      return;
    }

    const response = await window.apiFetch(
      `${window.ENV.API_BASE_URL}/user/delete_user/${encodeURIComponent(member.userId)}`,
      { method: 'DELETE' }
    );

    if (!response.ok) {
      let errorMessage = 'Não foi possível excluir o membro.';
      try {
        const error = await response.json();
        errorMessage = error.detail
          ? (typeof error.detail === 'string'
            ? error.detail
            : JSON.stringify(error.detail))
          : errorMessage;
      } catch {
        // Keep the generic message when the API does not return JSON.
      }
      message.textContent = errorMessage;
      message.hidden = false;
      return;
    }

    members = members.filter((item) => item.userId !== member.userId);
    renderMembers(search.value);
  });

  renderMembers();
}

window.initGerenciamento = initGerenciamento;
