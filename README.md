# ⚽ E.C.P Manager - Sistema de Gerenciamento Esportivo

Sistema web completo de gerenciamento para o **Esporte Clube Piedade** (E.C.P), desenvolvido com React, FastAPI e MongoDB.

![Status](https://img.shields.io/badge/status-ativo-success)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Sobre o Projeto

Sistema profissional de gestão esportiva desenvolvido especificamente para o Esporte Clube Piedade, permitindo o gerenciamento completo de atletas, treinos, partidas e finanças do clube.

### 🎨 Identidade Visual

- **Cores Oficiais**: Azul Royal (#0A1F51, #002B8C), Amarelo Dourado (#FFC107) e Branco
- **Logo**: Escudo oficial do E.C.P integrado
- **Design**: Moderno, profissional e responsivo

## ✨ Funcionalidades

### 🏃 Gestão de Atletas
- ✅ Cadastro completo de atletas com foto
- ✅ Indicador visual de pé dominante (esquerdo/direito/ambidestro)
- ✅ Posições, telefones e status
- ✅ Interface em cards com avatares
- ✅ Sistema de busca e filtros

### 🏋️ Gestão de Treinos
- ✅ Registro de treinos (data, local, observações)
- ✅ Controle de presença por atleta
- ✅ Histórico completo de treinos
- ✅ Estatísticas de frequência

### 🏆 Gestão de Partidas
- ✅ Registro de jogos e resultados
- ✅ Cálculo automático de vitória/empate/derrota
- ✅ Histórico de confrontos
- ✅ Badges coloridos por resultado

### 💰 Gestão Financeira
- ✅ Controle de receitas e despesas
- ✅ Gerenciamento de patrocinadores
- ✅ Cards com totalizadores (receitas, despesas, saldo)
- ✅ Categorização de movimentações

### 📊 Dashboard e Relatórios
- ✅ KPIs principais do clube
- ✅ Gráficos interativos (Recharts)
  - Receitas vs Despesas
  - Treinos por mês
  - Resultados de partidas
- ✅ Filtros por mês e ano
- ✅ Exportação para Excel e PDF

### 🔐 Autenticação
- ✅ Sistema de login com JWT
- ✅ Controle de sessão
- ✅ Proteção de rotas

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **MongoDB** - Banco de dados NoSQL
- **Motor** - Driver async do MongoDB
- **PyJWT** - Autenticação JWT
- **Bcrypt** - Hash de senhas
- **OpenPyXL** - Exportação Excel
- **ReportLab** - Geração de PDFs

### Frontend
- **React** - Biblioteca JavaScript
- **React Router** - Roteamento
- **Shadcn UI** - Componentes UI
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos
- **Lucide Icons** - Ícones
- **Sonner** - Notificações toast

## 📦 Estrutura do Projeto

```
ecp-manager/
├── backend/
│   ├── server.py           # API FastAPI
│   ├── requirements.txt    # Dependências Python
│   └── .env               # Variáveis de ambiente
├── frontend/
│   ├── src/
│   │   ├── pages/         # Páginas da aplicação
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Serviços API
│   │   ├── App.js         # Componente principal
│   │   └── index.js       # Entry point
│   ├── package.json       # Dependências Node
│   └── tailwind.config.js # Configuração Tailwind
└── README.md              # Este arquivo
```

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- MongoDB

### Backend

```bash
# Navegar para a pasta backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (.env)
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecp_manager
JWT_SECRET=sua_chave_secreta

# Iniciar servidor
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Frontend

```bash
# Navegar para a pasta frontend
cd frontend

# Instalar dependências
yarn install

# Configurar variáveis de ambiente (.env)
REACT_APP_BACKEND_URL=http://localhost:8001

# Iniciar aplicação
yarn start
```

## 🔑 Credenciais Padrão

**Email:** diretoria@ecp.com.br  
**Senha:** ecp2024

> ⚠️ **Importante**: Altere estas credenciais em produção!

## 📱 Páginas do Sistema

1. **Login** - Tela de autenticação com fundo do campo do clube
2. **Dashboard** - Visão geral com KPIs e gráficos
3. **Atletas** - Gestão de atletas com fotos e pé dominante
4. **Treinos** - Controle de treinos e presenças
5. **Partidas** - Registro de jogos e resultados
6. **Financeiro** - Gestão de receitas, despesas e patrocinadores
7. **Relatórios** - Exportação de dados em Excel/PDF

## 🔑 Credenciais de Teste

**Email:** diretoria@ecp.com.br  
**Senha:** ecp2024

---

**⚽ Esporte Clube Piedade - Gestão Profissional para o seu Clube!**
