async function initGerenciamento() {
  const members = [
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

  const list = document.getElementById('member-list');
  const search = document.getElementById('member-search');
  const addButton = document.querySelector('.team-page__add');

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
    modalStyle.href = 'style/components/membro-modal.css';
    document.head.appendChild(modalStyle);
  }

  const modal = document.getElementById('member-modal');
  const form = document.getElementById('member-form');
  const modalTitle = document.getElementById('member-modal-title');
  const passwordField = document.getElementById('member-password-field');
  const passwordInput = document.getElementById('member-password');
  const submitButton = modal.querySelector('[data-submit-member]');
  let editingMember = null;

  function setButtonText(button, text) {
    const textElement = button?.shadowRoot?.querySelector('.custom-btn span');
    if (textElement) textElement.textContent = text;
  }

  function openMemberModal(member = null) {
    editingMember = member;
    form.reset();
    modalTitle.textContent = member ? 'Editar membro' : 'Adicionar membro';
    setButtonText(submitButton, member ? 'Salvar' : 'Adicionar');
    passwordField.hidden = Boolean(member);
    passwordInput.required = !member;

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
        element.setAttribute('name', member.name);
        element.setAttribute('email', member.email);
        element.setAttribute('phone', member.phone);
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

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const updatedMember = {
      name: data.get('name'),
      email: data.get('email'),
      phone: data.get('phone'),
    };

    if (editingMember) {
      Object.assign(editingMember, updatedMember);
    } else {
      members.push(updatedMember);
    }

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
    const member = members.find((item) => item.name === event.detail.name);
    if (member) openMemberModal(member);
  });

  list.addEventListener('member-delete', (event) => {
    console.info('Excluir membro:', event.detail);
  });

  renderMembers();
}

window.initGerenciamento = initGerenciamento;
