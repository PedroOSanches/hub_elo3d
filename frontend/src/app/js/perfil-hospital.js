async function initPerfilHospital() {
  const $ = (sel) => document.querySelector(sel);

  const modalResponse = await fetch('pages/components/senha-modal.html');
  if (!modalResponse.ok) {
    throw new Error('Não foi possível carregar o modal de senha.');
  }

  document.getElementById('app').insertAdjacentHTML(
    'beforeend',
    await modalResponse.text()
  );

  if (!document.getElementById('senha-modal-style')) {
    const modalStyle = document.createElement('link');
    modalStyle.id = 'senha-modal-style';
    modalStyle.rel = 'stylesheet';
    modalStyle.href = 'style/components/senha-modal.css';
    document.head.appendChild(modalStyle);
  }

  /* ---------- Toast ---------- */
  const toast = $('#toast');
  let toastTimer;
  function showToast(msg) {
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (toast.hidden = true), 3000);
  }

  const members = [
    { nome: 'Ana Carolina da Silva', email: 'anacarolina@aacd.org.br' },
    { nome: 'Roberto Silveira da Costa', email: 'robertosilveira@aacd.org.br' },
  ];

  function iniciais(nome) {
    const p = nome.trim().split(/\s+/);
    return (p[0][0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase();
  }

  function renderMembros() {
    const ul = $('#members');
    ul.replaceChildren(
      ...members.map((m) => {
        const li = document.createElement('li');
        li.className = 'member';
        li.innerHTML = `
          <span class="avatar" aria-hidden="true"></span>
          <div class="member__info">
            <div class="member__name"></div>
            <div class="member__mail"></div>
          </div>`;
        li.querySelector('.avatar').textContent = iniciais(m.nome);
        li.querySelector('.member__name').textContent = m.nome;
        li.querySelector('.member__mail').textContent = m.email;
        return li;
      })
    );
    $('#count-membros').textContent = members.length;
  }
  renderMembros();

  /* ---------- Edição das informações da instituição ---------- */
  const form = $('#form-info');
  const campos = [...form.querySelectorAll('input, textarea')];
  const btnEditar = $('#btn-editar');
  const acoes = $('#edit-actions');
  let backup = {};

  function setEdicao(ativa) {
    form.classList.toggle('is-editing', ativa);
    campos.forEach((c) => (c.readOnly = !ativa));
    if (acoes) acoes.hidden = !ativa;
    if (btnEditar) btnEditar.hidden = ativa;
    if (ativa) campos[0].focus();
  }

  if (btnEditar) {
    btnEditar.addEventListener('click', () => {
      backup = Object.fromEntries(campos.map((c) => [c.name, c.value]));
      setEdicao(true);
    });
  }

  $('#btn-cancelar')?.addEventListener('click', () => {
    campos.forEach((c) => {
      if (backup[c.name] !== undefined) c.value = backup[c.name];
      c.classList.remove('invalid');
    });
    setEdicao(false);
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    campos.forEach((c) => {
      const invalido = !c.checkValidity();
      c.classList.toggle('invalid', invalido);
      if (invalido && ok) { c.focus(); ok = false; }
    });
    if (!ok) return;

    // TODO: enviar para a API (PUT /instituicao)
    const nome = $('#f-nome').value;
    $('#inst-nome').textContent = nome;
    setEdicao(false);
    showToast('Informações atualizadas.');
  });

  /* ---------- Alterar senha ---------- */
  const dlg = $('#dlg-senha');
  const formSenha = $('#form-senha');
  const erro = $('#senha-erro');

  $('#btn-senha').addEventListener('click', () => {
    formSenha.reset();
    erro.hidden = true;
    dlg.showModal();
  });
  $('#senha-cancelar').addEventListener('click', () => dlg.close());

  formSenha.addEventListener('submit', (e) => {
    e.preventDefault();
    const atual = $('#s-atual').value;
    const nova = $('#s-nova').value;
    const conf = $('#s-conf').value;

    let msg = '';
    if (!atual) msg = 'Informe a senha atual.';
    else if (nova.length < 8) msg = 'A nova senha deve ter pelo menos 8 caracteres.';
    else if (nova === atual) msg = 'A nova senha deve ser diferente da atual.';
    else if (nova !== conf) msg = 'A confirmação não confere com a nova senha.';

    if (msg) {
      erro.textContent = msg;
      erro.hidden = false;
      return;
    }

    // TODO: enviar para a API (POST /conta/senha)
    dlg.close();
    showToast('Senha alterada com sucesso.');
  });
}

window.initPerfilHospital = initPerfilHospital;