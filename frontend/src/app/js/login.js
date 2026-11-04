const parceiro = {};

const api = {
  async login(dados) {
    console.log('login', { email: dados.email });
    return { ok: true, mensagem: 'Login enviado (conectar à API).' };
  },
  async cadastrar(dados) {
    console.log('cadastro', dados);
    return { ok: true, mensagem: 'Cadastro enviado (conectar à API).' };
  },
};

function initLoginPage() {
  const rotas = {
    '/login': { id: 'view-login', titulo: 'Login - Hub Elo3D' },
    '/cadastro': { id: 'view-parceiro', titulo: 'Cadastro - Elo3D' },
    '/cadastro/instituicao': { id: 'view-instituicao', titulo: 'Cadastro da instituição - Elo3D' },
  };
  const caminho = window.location.pathname.replace(/\/+$/, '') || '/login';
  const rota = rotas[caminho] || rotas['/login'];

  if (caminho === '/cadastro/instituicao' && !parceiro.email) {
    window.history.replaceState({}, '', '/cadastro');
    window.initLoginPage();
    return;
  }

  Object.values(rotas).forEach(({ id }) => {
    document.getElementById(id).hidden = id !== rota.id;
  });
  document.body.dataset.view = rota.id.replace('view-', '');
  document.title = rota.titulo;
  window.scrollTo(0, 0);

  const formLogin = document.getElementById('form-login');
  if (!formLogin) return;
  if (formLogin.dataset.initialized === 'true') return;
  formLogin.dataset.initialized = 'true';

  const mensagem = (form, texto, ok = false) => {
    const elemento = form.querySelector('.form-msg');
    elemento.textContent = texto || '';
    elemento.classList.toggle('ok', ok);
  };
  const dadosDo = form => Object.fromEntries(new FormData(form));
  const valido = form => {
    if (form.checkValidity()) return true;
    form.reportValidity();
    return false;
  };
  const enviando = async (form, callback) => {
    const botao = form.querySelector('button[type="submit"]');
    botao.disabled = true;
    try {
      return await callback();
    } catch (error) {
      console.error(error);
      mensagem(form, 'Não foi possível concluir. Tente novamente.');
      return null;
    } finally {
      botao.disabled = false;
    }
  };

  formLogin.addEventListener('submit', async event => {
    event.preventDefault();
    mensagem(formLogin, '');
    if (!valido(formLogin)) return;
    const resposta = await enviando(formLogin, () => api.login(dadosDo(formLogin)));
    if (resposta) mensagem(formLogin, resposta.mensagem, resposta.ok);
  });

  const formParceiro = document.getElementById('form-parceiro');
  formParceiro.addEventListener('submit', event => {
    event.preventDefault();
    mensagem(formParceiro, '');
    if (!valido(formParceiro)) return;

    const dados = dadosDo(formParceiro);
    if (dados.senha !== dados.confirma) {
      mensagem(formParceiro, 'As senhas não conferem.');
      document.getElementById('cad-confirma').focus();
      return;
    }

    parceiro.email = dados.email;
    parceiro.senha = dados.senha;
    window.history.pushState({}, '', '/cadastro/instituicao');
    window.initLoginPage();
  });

  const cep = document.getElementById('inst-cep');
  cep.addEventListener('input', async () => {
    const digitos = cep.value.replace(/\D/g, '').slice(0, 8);
    cep.value = digitos.length > 5 ? `${digitos.slice(0, 5)}-${digitos.slice(5)}` : digitos;
    if (digitos.length !== 8) return;

    const resposta = await fetch(`https://viacep.com.br/ws/${digitos}/json/`);
    const endereco = await resposta.json();
    if (endereco.erro) return;
    if (endereco.logradouro) document.getElementById('inst-endereco').value = endereco.logradouro;
    if (endereco.bairro) document.getElementById('inst-bairro').value = endereco.bairro;
    if (endereco.localidade) document.getElementById('inst-cidade').value = `${endereco.localidade}/${endereco.uf}`;
  });

  const telefone = document.getElementById('inst-telefone');
  telefone.addEventListener('input', () => {
    const digitos = telefone.value.replace(/\D/g, '').slice(0, 11);
    if (digitos.length > 10) telefone.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 7)}-${digitos.slice(7)}`;
    else if (digitos.length > 6) telefone.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 6)}-${digitos.slice(6)}`;
    else if (digitos.length > 2) telefone.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`;
    else telefone.value = digitos;
  });

  const formInstituicao = document.getElementById('form-instituicao');
  formInstituicao.addEventListener('submit', async event => {
    event.preventDefault();
    mensagem(formInstituicao, '');
    if (!valido(formInstituicao)) return;
    const resposta = await enviando(formInstituicao, () => api.cadastrar({ ...parceiro, ...dadosDo(formInstituicao) }));
    if (resposta) mensagem(formInstituicao, resposta.mensagem, resposta.ok);
  });
}

window.initLoginPage = initLoginPage;
