const API_URL = "http://127.0.0.1:8000";

window.modoAtual = 'login';     
window.perfilAtual = 'cliente';  

// --- FUNÇÕES GLOBAIS DE INTERFACE ---
window.abrirModalAuth = function(modo = 'login', perfil = 'cliente') {
    const modal = document.getElementById("auth-modal");
    if (modal) {
        modal.classList.add("open");
        document.body.classList.add("modal-open");
        window.mudarModoAuth(modo);
        window.mudarTipoPerfil(perfil);
    }
};

window.fecharModalAuth = function() {
    const modal = document.getElementById("auth-modal");
    if (modal) {
        modal.classList.remove("open");
        document.body.classList.remove("modal-open");
    }
};

window.mudarModoAuth = function(modo) {
    window.modoAtual = modo;
    const tabLogin = document.getElementById("tab-modo-login");
    const tabCadastro = document.getElementById("tab-modo-cadastro");
    
    // Campos exclusivos do cadastro
    const campoNome = document.getElementById("campo-auth-nome");
    const campoTelefone = document.getElementById("campo-auth-telefone");
    const campoLocalizacao = document.getElementById("campo-auth-localizacao");
    
    const inputNome = document.getElementById("auth-nome");
    const inputTelefone = document.getElementById("auth-telefone");
    const inputLocalizacao = document.getElementById("auth-localizacao");
    
    const btnEnviar = document.getElementById("btn-auth-enviar");
    const titulo = document.getElementById("auth-modal-title");

    if (modo === 'login') {
        if (tabLogin) tabLogin.classList.add("active");
        if (tabCadastro) tabCadastro.classList.remove("active");
        
        // Esconde campos extras
        if (campoNome) campoNome.style.display = "none";
        if (campoTelefone) campoTelefone.style.display = "none";
        if (campoLocalizacao) campoLocalizacao.style.display = "none";
        
        if (inputNome) inputNome.required = false;
        if (inputTelefone) inputTelefone.required = false;
        if (inputLocalizacao) inputLocalizacao.required = false;
        
        if (titulo) titulo.textContent = "Entrar na Conta";
        if (btnEnviar) btnEnviar.textContent = "Entrar no Sistema";
    } else {
        if (tabLogin) tabLogin.classList.remove("active");
        if (tabCadastro) tabCadastro.classList.add("active");
        
        // Mostra campos extras
        if (campoNome) campoNome.style.display = "grid";
        if (campoTelefone) campoTelefone.style.display = "grid";
        if (campoLocalizacao) campoLocalizacao.style.display = "grid";
        
        if (inputNome) inputNome.required = true;
        if (inputTelefone) inputTelefone.required = true;
        if (inputLocalizacao) inputLocalizacao.required = true;
        
        if (titulo) titulo.textContent = "Criar Nova Conta";
        if (btnEnviar) btnEnviar.textContent = "Concluir Cadastro";
    }
};

window.mudarTipoPerfil = function(perfil) {
    window.perfilAtual = perfil;
    const tabCliente = document.getElementById("tab-tipo-cliente");
    const tabPrestador = document.getElementById("tab-tipo-prestador");
    const labelEmail = document.getElementById("label-auth-email");

    if (perfil === 'cliente') {
        if (tabCliente) tabCliente.classList.add("active");
        if (tabPrestador) tabPrestador.classList.remove("active");
        if (labelEmail) labelEmail.textContent = "E-mail pessoal";
    } else {
        if (tabCliente) tabCliente.classList.remove("active");
        if (tabPrestador) tabPrestador.classList.add("active");
        if (labelEmail) labelEmail.textContent = "E-mail corporativo";
    }
};

// Gerencia o que aparece na seção Hero dependendo se o prestador tá logado
window.checarSessao = function() {
    const prestadorId = localStorage.getItem("prestador_id");
    const prestadorNome = localStorage.getItem("prestador_nome");
    
    const painel = document.getElementById("painel-prestador");
    const displayNome = document.getElementById("nome-prestador-logado");
    const formBuscaPadrao = document.getElementById("hero-search");
    const textoDescricao = document.getElementById("hero-desc-texto");
    
    // Elementos do Topo (Header)
    const btnEntrar = document.getElementById("btn-entrar");
    const btnCadastrarTopo = document.getElementById("btn-cadastrar-topo");
    const btnSairTopo = document.getElementById("btn-sair-topo");

    if (prestadorId && prestadorNome) {
        if (displayNome) displayNome.textContent = prestadorNome;
        if (painel) painel.style.display = "block";
        
        // Esconde a busca normal e o texto auxiliar para dar lugar ao bloco de cadastro do prestador
        if (formBuscaPadrao) formBuscaPadrao.style.display = "none";
        if (textoDescricao) textoDescricao.style.display = "none";
        
        // Atualiza botões do topo (Entrar/Cadastrar somem, Sair aparece)
        if (btnEntrar) btnEntrar.style.display = "none";
        if (btnCadastrarTopo) btnCadastrarTopo.style.display = "none";
        if (btnSairTopo) btnSairTopo.style.display = "block";
    } else {
        if (painel) painel.style.display = "none";
        if (formBuscaPadrao) formBuscaPadrao.style.display = "flex";
        if (textoDescricao) textoDescricao.style.display = "block";
        
        // Restaura botões padrão do topo
        if (btnEntrar) btnEntrar.style.display = "block";
        if (btnCadastrarTopo) btnCadastrarTopo.style.display = "block";
        if (btnSairTopo) btnSairTopo.style.display = "none";
    }
};

// --- INICIALIZAÇÃO E EVENTOS DE FORMULÁRIO ---
document.addEventListener("DOMContentLoaded", () => {
    window.checarSessao();

    const formAuth = document.getElementById("form-auth-sistema");
    if (formAuth) {
        formAuth.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const nome = document.getElementById("auth-nome")?.value || "";
            const telefone = document.getElementById("auth-telefone")?.value || "";
            const localizacao = document.getElementById("auth-localizacao")?.value || "";
            const email = document.getElementById("auth-email")?.value || "";
            const senha = document.getElementById("auth-senha")?.value || "";

            let endpoint = "";
            
            if (window.perfilAtual === 'prestador') {
                endpoint = window.modoAtual === 'login' ? `${API_URL}/prestadores/login/` : `${API_URL}/prestadores/`;
            } else {
                endpoint = window.modoAtual === 'login' ? `${API_URL}/clientes/login/` : `${API_URL}/clientes/`;
            }

            const bodyData = window.modoAtual === 'login' 
                ? { email, senha } 
                : { nome, telefone, localizacao, email, senha };

            try {
                let response = await fetch(endpoint, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(bodyData)
                });

                if (response.status === 405 && window.modoAtual === 'login') {
                    const fallbackEndpoint = endpoint.slice(0, -1);
                    response = await fetch(fallbackEndpoint, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(bodyData)
                    });
                }

                if (response.ok) {
                    const dados = await response.json();
                    
                    if (window.modoAtual === 'login') {
                        if (window.perfilAtual === 'prestador') {
                            localStorage.setItem("prestador_id", dados.id);
                            localStorage.setItem("prestador_nome", dados.nome);
                            alert(`Bem-vindo, prestador ${dados.nome}!`);
                        } else {
                            localStorage.setItem("cliente_id", dados.id);
                            localStorage.setItem("cliente_nome", dados.nome);
                            alert(`Bem-vindo, ${dados.nome}!`);
                        }
                        window.fecharModalAuth();
                        window.location.reload();
                    } else {
                        alert("Sua conta foi criada com sucesso! Faça seu login agora.");
                        window.mudarModoAuth('login'); 
                    }
                } else {
                    const erro = await response.json();
                    
                    if (erro.detail && typeof erro.detail === 'object') {
                        const mensagens = erro.detail.map(err => `${err.loc.join('.')} -> ${err.msg}`).join('\n');
                        alert(`Erro de validação no backend:\n${mensagens}`);
                    } else {
                        alert(`Falha na operação: ${erro.detail || JSON.stringify(erro)}`);
                    }
                }
            } catch (error) {
                console.error(error);
                alert("Erro ao conectar com o servidor.");
            }
        });
    }

    // Cadastro de novos serviços
    const formCriarServico = document.getElementById("form-criar-servico");
    if (formCriarServico) {
        formCriarServico.addEventListener("submit", async (e) => {
            e.preventDefault();
            const prestadorId = localStorage.getItem("prestador_id");

            if (!prestadorId) {
                alert("Sessão expirada. Faça login novamente.");
                return;
            }

            const novoServico = {
                descricao: document.getElementById("servico-descricao").value,
                preco: parseFloat(document.getElementById("servico-preco").value),
                tempo_estimado: document.getElementById("servico-tempo").value,
                status: "Ativo",
                prestador_id: parseInt(prestadorId),
                quantavaliacao: 0
            };

            try {
                const response = await fetch(`${API_URL}/servicos/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(novoServico)
                });

                if (response.ok) {
                    alert("Serviço publicado!");
                    formCriarServico.reset();
                } else {
                    const erro = await response.json();
                    alert(`Erro: ${erro.detail}`);
                }
            } catch (error) {
                console.error(error);
            }
        });
    }

    const btnLogout = document.getElementById("btn-logout");
    if (btnLogout) {
        btnLogout.addEventListener("click", () => {
            localStorage.clear();
            alert("Desconectado.");
            window.location.reload();
        });
    }
});