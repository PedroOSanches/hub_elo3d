async function initProjectsPage() {
  document.getElementById('project-modal-style')?.remove();
  const modalStyle = document.createElement('link');
  modalStyle.id = 'project-modal-style';
  modalStyle.rel = 'stylesheet';
  modalStyle.href = 'style/components/project-modal.css';
  document.head.appendChild(modalStyle);

  document.getElementById('status-modal-style')?.remove();
  const statusModalStyle = document.createElement('link');
  statusModalStyle.id = 'status-modal-style';
  statusModalStyle.rel = 'stylesheet';
  statusModalStyle.href = 'style/components/status-modal.css';
  document.head.appendChild(statusModalStyle);

  const search = document.getElementById('project-search');
  const rows = [...document.querySelectorAll('#projects-list project-row')];
  let modal = document.getElementById('project-modal');

  if (!modal) {
    const response = await fetch('pages/components/project-modal.html');

    if (!response.ok) {
      throw new Error('Não foi possível carregar o modal do projeto.');
    }

    document.getElementById('app').insertAdjacentHTML('beforeend', await response.text());
    window.lucide?.createIcons();
    modal = document.getElementById('project-modal');
  }

  if (!modal) {
    throw new Error('O modal do projeto não foi encontrado após o carregamento.');
  }

  const title = document.getElementById('project-modal-title');
  const dueDate = document.getElementById('project-modal-due-date');
  const printer = document.getElementById('project-modal-printer');
  let statusModal = document.getElementById('status-modal');

  if (!statusModal) {
    const response = await fetch('pages/components/status-modal.html');

    if (!response.ok) {
      throw new Error('Não foi possível carregar o modal de status.');
    }

    document.getElementById('app').insertAdjacentHTML('beforeend', await response.text());
    window.lucide?.createIcons();
    statusModal = document.getElementById('status-modal');
  }

  if (!statusModal) {
    throw new Error('O modal de status não foi encontrado após o carregamento.');
  }

  const closeModal = () => {
    modal.hidden = true;
    document.body.classList.remove('modal-open');
  };

  const openModal = event => {
    const { name, printer: projectPrinter, dueDate: projectDueDate } = event.detail;
    title.textContent = name;
    dueDate.textContent = projectDueDate.replace(/\/\d{4}$/, '');
    printer.textContent = `Equipamento: ${projectPrinter} (FDM, 250x210x210mm)`;
    modal.hidden = false;
    document.body.classList.add('modal-open');
  };

  const closeStatusModal = () => {
    statusModal.hidden = true;
  };

  const openStatusModal = () => {
    statusModal.hidden = false;
  };

  if (search) {
    search.addEventListener('input', () => {
      const query = search.value.trim().toLowerCase();
      rows.forEach(row => {
        row.hidden = query !== '' && !row.dataset.project.includes(query);
      });
    });
  }

  document.addEventListener('project-detail-request', openModal);
  modal.querySelector('[data-open-status]')?.addEventListener('click', openStatusModal);
  modal.querySelectorAll('[data-modal-close]').forEach(element => {
    element.addEventListener('click', closeModal);
  });
  statusModal.querySelectorAll('[data-status-close]').forEach(element => {
    element.addEventListener('click', closeStatusModal);
  });
  statusModal.querySelector('[data-status-save]')?.addEventListener('click', closeStatusModal);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !modal.hidden) closeModal();
    if (event.key === 'Escape' && !statusModal.hidden) closeStatusModal();
  });
}

window.initProjectsPage = initProjectsPage;
