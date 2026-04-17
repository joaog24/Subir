# Diagrama de Arquitetura do Sistema - E.C.P Manager

```mermaid
graph TB
    %% Cliente
    subgraph "Camada de Apresentação"
        Browser[🌐 Navegador Web]
    end
    
    %% Frontend
    subgraph "Frontend - React"
        React[⚛️ React 18]
        Router[React Router]
        UI[Shadcn UI + Tailwind]
        Charts[Recharts]
        State[Estado Local]
        API_Service[API Service]
    end
    
    %% Kubernetes Ingress
    subgraph "Kubernetes Cluster"
        Ingress[🌐 Ingress Controller]
        
        subgraph "Pod E.C.P Manager"
            Supervisor[Supervisor]
            
            subgraph "Frontend Service"
                Frontend[Node.js + React<br/>Porta 3000]
            end
            
            subgraph "Backend Service"
                Backend[FastAPI<br/>Porta 8001]
                Auth[JWT Auth]
                Routes[API Routes]
                Models[Pydantic Models]
                Aggregations[MongoDB Aggregations]
                Export[Excel/PDF Export]
            end
        end
        
        subgraph "Database"
            MongoDB[(🗄️ MongoDB<br/>localhost:27017)]
        end
    end
    
    %% Fluxo de Dados
    Browser -->|HTTPS| Ingress
    Ingress -->|/| Frontend
    Ingress -->|/api/*| Backend
    
    React --> Router
    React --> UI
    React --> Charts
    React --> State
    React --> API_Service
    
    API_Service -->|HTTP Requests| Backend
    Backend -->|Motor AsyncIO| MongoDB
    
    Supervisor -.->|Gerencia| Frontend
    Supervisor -.->|Gerencia| Backend
    
    Backend --> Auth
    Backend --> Routes
    Backend --> Models
    Backend --> Aggregations
    Backend --> Export
    
    Auth -.->|Valida| Routes
    Routes --> Models
    Routes --> Aggregations
    Routes --> Export
    Aggregations --> MongoDB
    
    %% Storage
    subgraph "Armazenamento"
        Fotos[Fotos Base64<br/>MongoDB]
    end
    
    MongoDB -.->|Armazena| Fotos
    
    %% Environment
    subgraph "Configuração"
        Env_Front[.env Frontend<br/>REACT_APP_BACKEND_URL]
        Env_Back[.env Backend<br/>MONGO_URL<br/>DB_NAME<br/>JWT_SECRET]
    end
    
    Frontend -.->|Usa| Env_Front
    Backend -.->|Usa| Env_Back
    
    style Browser fill:#4A90E2,color:#fff
    style Frontend fill:#61DAFB,color:#000
    style Backend fill:#009688,color:#fff
    style MongoDB fill:#47A248,color:#fff
    style Ingress fill:#326CE5,color:#fff
    style Supervisor fill:#FF6B6B,color:#fff
```

## Componentes da Arquitetura

### 1. Camada de Apresentação
- **Navegador Web**: Interface do usuário
- **Responsivo**: Mobile, Tablet, Desktop

### 2. Frontend (React)
- **React 18**: Framework UI
- **React Router**: Roteamento SPA
- **Shadcn UI**: Componentes acessíveis
- **Tailwind CSS**: Estilização
- **Recharts**: Visualizações de dados
- **Axios**: Cliente HTTP

### 3. Kubernetes Infrastructure
- **Ingress Controller**: Roteamento de tráfego
  - `/` → Frontend (porta 3000)
  - `/api/*` → Backend (porta 8001)
- **Supervisor**: Gerenciamento de processos
- **Hot Reload**: Desenvolvimento ágil

### 4. Backend (FastAPI)
- **FastAPI**: Framework Python assíncrono
- **JWT Authentication**: Autenticação segura
- **Pydantic**: Validação de dados
- **Motor**: Driver MongoDB assíncrono
- **Aggregation Pipelines**: Queries otimizadas
- **OpenPyXL + ReportLab**: Exportações

### 5. Banco de Dados
- **MongoDB**: NoSQL database
- **Collections**:
  - usuarios
  - atletas
  - treinos
  - presencas
  - partidas
  - patrocinadores
  - recebimentos
  - despesas

### 6. Segurança
- **JWT Tokens**: Autenticação stateless
- **Bcrypt**: Hash de senhas
- **CORS**: Configurado para produção
- **HTTPS**: Kubernetes Ingress TLS

### 7. Performance
- **Aggregation Pipelines**: Processamento no banco
- **Async/Await**: I/O não bloqueante
- **Connection Pooling**: MongoDB Motor
- **Hot Reload**: Desenvolvimento rápido

## Fluxo de Requisição

1. **Usuário** acessa via navegador
2. **Ingress** roteia para frontend ou backend
3. **Frontend** faz requisições HTTP para backend
4. **Backend** valida JWT token
5. **Backend** executa aggregation pipeline no MongoDB
6. **MongoDB** retorna dados processados
7. **Backend** formata resposta (Pydantic)
8. **Frontend** atualiza UI com dados

## Escalabilidade

- **Horizontal**: Múltiplos pods no Kubernetes
- **Vertical**: Recursos ajustáveis por pod
- **Database**: MongoDB com replica set
- **Cache**: Potencial para Redis (futuro)
