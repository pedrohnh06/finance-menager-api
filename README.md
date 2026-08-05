# Finance Manager API 💰

Uma API REST moderna para gerenciamento financeiro pessoal, construída com **FastAPI** e **Python**. Este projeto permite que usuários gerenciem suas categorias de gastos e receitas, acompanhem transações detalhadas e obtenham resumos financeiros inteligentes — tudo protegido por autenticação JWT.

🌍 **Deploy da Aplicação**: [https://fintrack-app-meo7.onrender.com](https://fintrack-app-meo7.onrender.com)  
⚙️ **Documentação da API (Swagger)**: [https://finance-menager-api.onrender.com/docs](https://finance-menager-api.onrender.com/docs)

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web super rápido e moderno.
- **SQLAlchemy**: ORM para manipulação do banco de dados relacional.
- **PostgreSQL / SQLite**: Banco de dados flexível (Postgres na nuvem via Supabase, SQLite para testes locais).
- **Pydantic**: Validação de dados e serialização (Schemas).
- **Uvicorn**: Servidor web ASGI.
- **Passlib (bcrypt)**: Criptografia irreversível de senhas.
- **Python-Jose (JWT)**: Geração e validação de tokens de autenticação.

## ✨ Funcionalidades

- [x] **Categorias**: CRUD completo (Criar, Listar, Editar, Excluir).
- [x] **Transações**: Registro de receitas e despesas vinculadas a categorias.
- [x] **Filtros e Consultas**: Buscar transações por tipo ou categoria.
- [x] **Resumo Financeiro**: Cálculo automático de receitas, despesas e saldo.
- [x] **Cadastro de Usuários**: Com criptografia de senha (bcrypt).
- [x] **Login com JWT**: Geração de token de acesso com expiração.
- [x] **Proteção de Rotas**: Todas as rotas exigem autenticação.
- [x] **Isolamento de Dados**: Cada usuário acessa apenas seus próprios dados.

## 📡 Endpoints da API

### 🔓 Rotas Públicas
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Mensagem de boas-vindas |
| `POST` | `/usuario/` | Cadastrar novo usuário |
| `POST` | `/login/` | Fazer login e receber token JWT |

### 🔒 Rotas Protegidas (Requerem Token JWT)

**Categorias**
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/categorias/` | Criar categoria |
| `GET` | `/categorias/` | Listar categorias do usuário |
| `PUT` | `/categorias/{id}` | Atualizar categoria |
| `DELETE` | `/categorias/{id}` | Excluir categoria |

**Transações**
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/transacoes/` | Criar transação |
| `GET` | `/transacoes/` | Listar transações (com filtros opcionais) |
| `GET` | `/transacoes/resumo` | Resumo financeiro (receitas, despesas, saldo) |
| `PATCH` | `/transacoes/{id}` | Atualizar transação parcialmente |
| `DELETE` | `/transacoes/{id}` | Excluir transação |

## 📁 Estrutura do Projeto

```
finance-menager-api/
├── src/
│   ├── routers/
│   │   ├── categorias.py    # Rotas de Categorias
│   │   ├── transacoes.py    # Rotas de Transações
│   │   ├── login.py         # Rota de Login (JWT)
│   │   └── usuario.py       # Rota de Cadastro
│   ├── auth.py              # Lógica de segurança, hash e JWT
│   ├── database.py          # Configuração do SQLite e SQLAlchemy
│   ├── main.py              # Ponto de entrada da API
│   ├── models.py            # Modelos do Banco de Dados
│   └── schemas.py           # Schemas Pydantic (Validação)
├── .gitignore
├── requirements.txt         # Dependências do projeto
└── README.md
```

## 🛠️ Como rodar o projeto localmente

**1. Clone o repositório**
```bash
git clone https://github.com/pedrohnh06/finance-menager-api.git
cd finance-menager-api
```

**2. Crie e ative o Ambiente Virtual (.venv)**
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows (PowerShell)
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais (veja `src/database.py` e `src/auth.py` para detalhes de chave secreta e conexão).
Exemplo:
```env
SECRET_KEY="sua-chave-secreta"
DATABASE_URL="postgresql://... (seu link do banco)"
```

**5. Inicie o servidor**
```bash
uvicorn src.main:app --reload
```

**5. Acesse a Documentação Interativa (Swagger)**

Abra seu navegador e acesse: `http://127.0.0.1:8000/docs`

## 🔐 Como autenticar no Swagger

1. Crie um usuário em `POST /usuario/`
2. Clique no botão **Authorize** (🔒) no topo da página
3. Informe o email no campo `username` e a senha no campo `password`
4. Clique em **Authorize** — pronto, todas as rotas protegidas estarão liberadas!

---
*Projeto construído como jornada de aprendizado em Arquitetura de APIs com Python e FastAPI.*
