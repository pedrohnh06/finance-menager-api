# Finance Manager API 💰

Uma API REST moderna para gerenciamento financeiro pessoal, construída com **FastAPI** e **Python**. Este projeto permite que usuários gerenciem suas categorias de gastos e receitas, acompanhem transações detalhadas e obtenham resumos financeiros inteligentes.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web super rápido e moderno.
- **SQLAlchemy**: ORM para manipulação do banco de dados relacional.
- **SQLite**: Banco de dados leve (ideal para desenvolvimento).
- **Pydantic**: Validação de dados e serialização (Schemas).
- **Uvicorn**: Servidor web ASGI.
- **Passlib & Python-Jose**: Criptografia de senhas e JWT (JSON Web Tokens).

## ✨ Funcionalidades (Atuais e em Desenvolvimento)

- [x] **Categorias**: Criar, listar, editar e excluir categorias (ex: Alimentação, Lazer).
- [x] **Transações**: Registro de receitas e despesas com vínculo a categorias.
- [x] **Filtros e Consultas**: Buscar transações por tipo ou categoria específica.
- [x] **Resumo Financeiro**: Rota inteligente que calcula automaticamente o total de receitas, despesas e saldo.
- [x] **Segurança Básica**: Criptografia irreversível de senhas usando `bcrypt`.
- [ ] **Autenticação**: Login com geração de Token JWT (Em andamento).
- [ ] **Proteção de Rotas**: Usuário acessa apenas as suas próprias transações.

## 📁 Estrutura do Projeto

```
finance-menager-api/
├── src/
│   ├── routers/
│   │   ├── categorias.py    # Rotas de Categorias
│   │   ├── transacoes.py    # Rotas de Transações
│   │   └── usuario.py       # Rotas de Usuário (Cadastro)
│   ├── auth.py              # Lógica de segurança e JWT
│   ├── database.py          # Configuração do SQLite e SQLAlchemy
│   ├── main.py              # Ponto de entrada da API
│   ├── models.py            # Modelos do Banco de Dados
│   └── schemas.py           # Modelos do Pydantic (Validação)
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
- No Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Inicie o servidor**
```bash
uvicorn src.main:app --reload
```

**5. Acesse a Documentação Interativa (Swagger)**
Abra seu navegador e acesse: `http://127.0.0.1:8000/docs`

---
*Projeto construído como jornada de aprendizado em Arquitetura de APIs com Python e FastAPI.*
