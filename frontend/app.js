// Configuração base da API
const API_URL = "https://finance-menager-api.onrender.com";
let currentToken = localStorage.getItem("token") || null;
let chartCategoriasInstance = null;
let chartBalancoInstance = null;

// ==========================================
// CONTROLE DE TELAS
// ==========================================
function toggleAuth(type) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabs = document.querySelectorAll('.tab-btn');
    
    document.getElementById('auth-msg').innerText = '';

    if (type === 'login') {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
        tabs[0].classList.add('active');
        tabs[1].classList.remove('active');
    } else {
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
        tabs[0].classList.remove('active');
        tabs[1].classList.add('active');
    }
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

// Inicialização: Se já tem token, vai pro dashboard
if (currentToken) {
    showScreen('dashboard-screen');
    loadDashboard();
} else {
    showScreen('auth-screen');
}

// ==========================================
// AUTENTICAÇÃO
// ==========================================
async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;
    const msgEl = document.getElementById('auth-msg');

    try {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", senha);

        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            localStorage.setItem("token", currentToken);
            showScreen('dashboard-screen');
            loadDashboard();
        } else {
            msgEl.innerText = "Email ou senha incorretos.";
        }
    } catch (error) {
        msgEl.innerText = "Erro ao conectar com o servidor.";
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const nome = document.getElementById('reg-nome').value;
    const email = document.getElementById('reg-email').value;
    const senha = document.getElementById('reg-senha').value;
    const msgEl = document.getElementById('auth-msg');

    try {
        const response = await fetch(`${API_URL}/usuario/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, senha })
        });

        if (response.ok) {
            msgEl.innerText = "Cadastro realizado! Faça o login.";
            msgEl.style.color = "#38a169";
            toggleAuth('login');
        } else {
            const errorData = await response.json();
            msgEl.innerText = errorData.detail || "Erro ao cadastrar.";
        }
    } catch (error) {
        msgEl.innerText = "Erro ao conectar com o servidor.";
    }
}

function logout() {
    currentToken = null;
    localStorage.removeItem("token");
    showScreen('auth-screen');
}

// ==========================================
// DASHBOARD & TRANSAÇÕES
// ==========================================
async function fetchWithAuth(url, options = {}) {
    if (!currentToken) return null;
    
    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${currentToken}`
    };

    const res = await fetch(url, options);
    if (res.status === 401) {
        logout();
        throw new Error("Token expirado");
    }
    return res;
}

async function loadDashboard() {
    await carregarCategorias();
    await carregarResumo();
    await carregarTransacoes();
    await renderizarGraficos();
}

function getQueryParams() {
    const mes = document.getElementById('filter-mes').value;
    const ano = document.getElementById('filter-ano').value;
    let params = new URLSearchParams();
    if (mes) params.append('mes', mes);
    if (ano) params.append('ano', ano);
    const queryString = params.toString();
    return queryString ? `?${queryString}` : '';
}

function mudarFiltroData() {
    loadDashboard();
}

async function carregarResumo() {
    try {
        const res = await fetchWithAuth(`${API_URL}/transacoes/resumo${getQueryParams()}`);
        if (res.ok) {
            const data = await res.json();
            document.getElementById('val-receitas').innerText = `R$ ${data.total_receitas.toFixed(2)}`;
            document.getElementById('val-despesas').innerText = `R$ ${data.total_despesas.toFixed(2)}`;
            document.getElementById('val-saldo').innerText = `R$ ${data.saldo_total.toFixed(2)}`;
        }
    } catch (error) {
        console.error(error);
    }
}

async function carregarTransacoes() {
    try {
        const res = await fetchWithAuth(`${API_URL}/transacoes/${getQueryParams()}`);
        if (res.ok) {
            const transacoes = await res.json();
            const tbody = document.getElementById('transactions-body');
            tbody.innerHTML = '';

            transacoes.reverse().forEach(t => {
                const tr = document.createElement('tr');
                const tipoCor = t.tipo === 'receita' ? '#38a169' : '#e53e3e';
                
                tr.innerHTML = `
                    <td>${t.descricao}</td>
                    <td style="color: ${tipoCor}; font-weight: 500;">
                        ${t.tipo === 'despesa' ? '-' : ''} R$ ${t.valor.toFixed(2)}
                    </td>
                    <td>
                        <button class="edit-btn" onclick="prepararEdicaoTransacao(${t.id}, '${t.descricao}', ${t.valor}, '${t.tipo}', ${t.categoria_id})">Editar</button>
                        <button class="delete-btn" onclick="deletarTransacao(${t.id})">Excluir</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error(error);
    }
}

async function carregarCategorias() {
    try {
        const res = await fetchWithAuth(`${API_URL}/categorias/`);
        if (res.ok) {
            const categorias = await res.json();
            
            // Popula a tabela de categorias
            const tbody = document.getElementById('categories-body');
            tbody.innerHTML = '';
            
            // Popula o select de transações
            const select = document.getElementById('trans-categoria');
            select.innerHTML = '<option value="" disabled selected>Selecione...</option>';

            categorias.forEach(c => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${c.nome}</td>
                    <td>
                        <button class="edit-btn" onclick="prepararEdicaoCategoria(${c.id}, '${c.nome}')">Editar</button>
                        <button class="delete-btn" onclick="deletarCategoria(${c.id})">Excluir</button>
                    </td>
                `;
                tbody.appendChild(tr);

                const option = document.createElement('option');
                option.value = c.id;
                option.innerText = c.nome;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error(error);
    }
}

async function prepararEdicaoCategoria(id, nome) {
    document.getElementById('cat-id-edit').value = id;
    document.getElementById('cat-nome').value = nome;
    document.getElementById('cat-submit-btn').innerText = 'Salvar';
}

async function handleAddCategoria(event) {
    event.preventDefault();
    const nome = document.getElementById('cat-nome').value;
    const idEdit = document.getElementById('cat-id-edit').value;

    try {
        let url = `${API_URL}/categorias/`;
        let method = 'POST';

        if (idEdit) {
            url = `${API_URL}/categorias/${idEdit}`;
            method = 'PUT'; // Assumindo PUT para update
        }

        const res = await fetchWithAuth(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome })
        });

        if (res.ok) {
            document.getElementById('category-form').reset();
            document.getElementById('cat-id-edit').value = '';
            document.getElementById('cat-submit-btn').innerText = 'Add';
            await carregarCategorias();
        } else {
            alert("Erro ao salvar categoria");
        }
    } catch (error) {
        console.error(error);
    }
}

async function deletarCategoria(id) {
    if (confirm("Excluir esta categoria?")) {
        try {
            const res = await fetchWithAuth(`${API_URL}/categorias/${id}`, {
                method: 'DELETE'
            });
            if (res.ok) {
                await carregarCategorias();
            }
        } catch (error) {
            console.error(error);
        }
    }
}

function prepararEdicaoTransacao(id, descricao, valor, tipo, categoria_id) {
    document.getElementById('trans-id-edit').value = id;
    document.getElementById('trans-desc').value = descricao;
    document.getElementById('trans-val').value = valor;
    document.getElementById('trans-tipo').value = tipo;
    document.getElementById('trans-categoria').value = categoria_id;
    document.getElementById('trans-submit-btn').innerText = 'Salvar';
}

async function handleAddTransaction(event) {
    event.preventDefault();
    const descricao = document.getElementById('trans-desc').value;
    const valor = parseFloat(document.getElementById('trans-val').value);
    const tipo = document.getElementById('trans-tipo').value;
    const categoria_id = parseInt(document.getElementById('trans-categoria').value);
    const idEdit = document.getElementById('trans-id-edit').value;

    if (isNaN(categoria_id)) {
        alert("Por favor, selecione uma categoria.");
        return;
    }

    try {
        let url = `${API_URL}/transacoes/`;
        let method = 'POST';

        if (idEdit) {
            url = `${API_URL}/transacoes/${idEdit}`;
            method = 'PATCH'; // Transações usam PATCH
        }

        const res = await fetchWithAuth(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ descricao, valor, tipo, categoria_id })
        });

        if (res.ok) {
            document.getElementById('transaction-form').reset();
            document.getElementById('trans-id-edit').value = '';
            document.getElementById('trans-submit-btn').innerText = 'Adicionar';
            loadDashboard();
        } else {
            alert("Erro ao salvar transação.");
        }
    } catch (error) {
        console.error(error);
    }
}

async function deletarTransacao(id) {
    if (confirm("Tem certeza que deseja excluir esta transação?")) {
        try {
            const res = await fetchWithAuth(`${API_URL}/transacoes/${id}`, {
                method: 'DELETE'
            });
            if (res.ok) {
                loadDashboard();
            }
        } catch (error) {
            console.error(error);
        }
    }
}

// ==========================================
// GRÁFICOS E RELATÓRIOS
// ==========================================
async function renderizarGraficos() {
    try {
        const resTransacoes = await fetchWithAuth(`${API_URL}/transacoes/${getQueryParams()}`);
        const resCategorias = await fetchWithAuth(`${API_URL}/categorias/`);
        
        if (!resTransacoes.ok || !resCategorias.ok) return;
        
        const transacoes = await resTransacoes.json();
        const categorias = await resCategorias.json();
        
        const mapCategorias = {};
        categorias.forEach(c => mapCategorias[c.id] = c.nome);
        
        let despesasPorCategoria = {};
        let totalReceitas = 0;
        let totalDespesas = 0;
        
        transacoes.forEach(t => {
            if (t.tipo === 'despesa') {
                totalDespesas += t.valor;
                const catNome = mapCategorias[t.categoria_id] || "Outros";
                despesasPorCategoria[catNome] = (despesasPorCategoria[catNome] || 0) + t.valor;
            } else {
                totalReceitas += t.valor;
            }
        });
        
        // Gráfico de Categorias (Rosca)
        const ctxCat = document.getElementById('chart-categorias').getContext('2d');
        if (chartCategoriasInstance) chartCategoriasInstance.destroy();
        chartCategoriasInstance = new Chart(ctxCat, {
            type: 'doughnut',
            data: {
                labels: Object.keys(despesasPorCategoria),
                datasets: [{
                    data: Object.values(despesasPorCategoria),
                    backgroundColor: ['#e53e3e', '#dd6b20', '#d69e2e', '#38a169', '#3182ce', '#805ad5']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        // Gráfico de Balanço (Barras)
        const ctxBal = document.getElementById('chart-balanco').getContext('2d');
        if (chartBalancoInstance) chartBalancoInstance.destroy();
        chartBalancoInstance = new Chart(ctxBal, {
            type: 'bar',
            data: {
                labels: ['Receitas', 'Despesas'],
                datasets: [{
                    label: 'Total R$',
                    data: [totalReceitas, totalDespesas],
                    backgroundColor: ['#38a169', '#e53e3e']
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } },
                plugins: { legend: { display: false } }
            }
        });
        
    } catch (error) {
        console.error(error);
    }
}

function exportarParaPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    doc.setFontSize(18);
    doc.text("Relatório de Transações - FinTrack", 14, 20);
    
    doc.autoTable({
        html: '#transactions-table',
        startY: 30,
        theme: 'striped',
        headStyles: { fillColor: [49, 130, 206] },
        columns: [
            { header: 'Descrição', dataKey: 0 },
            { header: 'Valor', dataKey: 1 }
        ]
    });
    
    doc.save('fintrack-relatorio.pdf');
}
