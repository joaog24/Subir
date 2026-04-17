# Fluxogramas - E.C.P Manager

## 1. Fluxograma de Autenticação

```mermaid
flowchart TD
    Start([Usuário acessa sistema]) --> Login[Tela de Login]
    Login --> Input[Insere email e senha]
    Input --> Validate{Validar<br/>credenciais}
    
    Validate -->|Inválido| Error[Exibir erro]
    Error --> Login
    
    Validate -->|Válido| Hash[Verificar hash bcrypt]
    Hash -->|Correto| Token[Gerar JWT Token]
    Token --> Store[Armazenar token<br/>localStorage]
    Store --> Redirect[Redirecionar<br/>para Dashboard]
    Redirect --> End([Dashboard])
    
    Hash -->|Incorreto| Error
    
    style Start fill:#28A745,color:#fff
    style End fill:#28A745,color:#fff
    style Error fill:#DC3545,color:#fff
    style Token fill:#FFC107,color:#0A1F51
```

---

## 2. Fluxograma de Cadastro de Atleta

```mermaid
flowchart TD
    Start([Página Atletas]) --> Click[Clicar 'Novo Atleta']
    Click --> Form[Abrir formulário]
    Form --> Fill[Preencher dados:
    - Nome
    - Posição
    - Telefone
    - Pé Dominante]
    
    Fill --> Photo{Deseja adicionar<br/>foto?}
    Photo -->|Sim| Upload[Upload de foto]
    Upload --> Validate
    Photo -->|Não| Validate[Validar formulário]
    
    Validate -->|Inválido| ShowError[Mostrar erros]
    ShowError --> Fill
    
    Validate -->|Válido| Base64{Foto existe?}
    Base64 -->|Sim| Convert[Converter para Base64]
    Convert --> Send
    Base64 -->|Não| Send[Enviar para API]
    
    Send --> API[POST /api/atletas]
    API --> DB[(Salvar no MongoDB)]
    DB --> Success[Exibir toast sucesso]
    Success --> Reload[Recarregar lista]
    Reload --> Close[Fechar modal]
    Close --> End([Lista atualizada])
    
    API -->|Erro| APIError[Exibir erro API]
    APIError --> Form
    
    style Start fill:#0A1F51,color:#fff
    style End fill:#28A745,color:#fff
    style ShowError fill:#DC3545,color:#fff
    style Success fill:#28A745,color:#fff
```

---

## 3. Fluxograma de Registro de Presença

```mermaid
flowchart TD
    Start([Página Treinos]) --> Select[Selecionar treino]
    Select --> ClickPresenca[Clicar 'N presentes']
    ClickPresenca --> Load[Carregar lista de atletas]
    Load --> API1[GET /api/presencas/treino/:id]
    
    API1 --> Display[Exibir lista com checkboxes]
    Display --> Mark[Marcar/desmarcar presenças]
    Mark --> Save[Clicar 'Salvar']
    
    Save --> Prepare[Preparar payload:
    treino_id
    presencas[]]
    Prepare --> API2[POST /api/presencas/bulk]
    
    API2 --> Delete[Deletar presenças antigas]
    Delete --> Insert[Inserir novas presenças]
    Insert --> Success[Toast: Sucesso]
    Success --> Close[Fechar modal]
    Close --> Reload[Recarregar treinos]
    Reload --> Update[Atualizar contador]
    Update --> End([Lista atualizada])
    
    API2 -->|Erro| Error[Exibir erro]
    Error --> Display
    
    style Start fill:#0A1F51,color:#fff
    style End fill:#28A745,color:#fff
    style Success fill:#28A745,color:#fff
    style Error fill:#DC3545,color:#fff
```

---

## 4. Fluxograma de Dashboard com Filtros

```mermaid
flowchart TD
    Start([Acessar Dashboard]) --> Auth{Token válido?}
    Auth -->|Não| Login[Redirecionar Login]
    Auth -->|Sim| Load[Carregar Dashboard]
    
    Load --> GetStats[GET /api/dashboard/stats]
    GetStats --> GetCharts[GET /api/dashboard/charts]
    
    GetCharts --> Display[Exibir:
    - 6 KPIs
    - 3 Gráficos]
    
    Display --> Wait[Aguardar interação]
    
    Wait --> Filter{Usuário filtra?}
    Filter -->|Não| Wait
    Filter -->|Sim| SelectPeriod[Selecionar mês/ano]
    
    SelectPeriod --> UpdateStats[GET /api/dashboard/stats?mes=X&ano=Y]
    UpdateStats --> Aggregate[MongoDB Aggregation:
    - Filtrar por período
    - Calcular somas
    - Contar resultados]
    
    Aggregate --> UpdateUI[Atualizar:
    - KPIs
    - Gráficos]
    UpdateUI --> Wait
    
    Wait --> Export{Exportar?}
    Export -->|Sim| SelectType[Selecionar tipo]
    SelectType --> ExportAPI[GET /api/export/:format/:tipo]
    ExportAPI --> Download[Baixar arquivo]
    Download --> Wait
    Export -->|Não| Wait
    
    style Start fill:#0A1F51,color:#fff
    style Display fill:#28A745,color:#fff
    style Aggregate fill:#FFC107,color:#0A1F51
```

---

## 5. Fluxograma de Exportação de Relatórios

```mermaid
flowchart TD
    Start([Página Relatórios]) --> Select[Selecionar relatório:
    - Atletas
    - Treinos
    - Partidas
    - Financeiro]
    
    Select --> Format{Escolher formato}
    Format -->|Excel| Excel[Clicar 'Excel']
    Format -->|PDF| PDF[Clicar 'PDF']
    
    Excel --> APIExcel[GET /api/export/excel/:tipo]
    PDF --> APIPDF[GET /api/export/pdf/:tipo]
    
    APIExcel --> QueryExcel[Query MongoDB]
    APIPDF --> QueryPDF[Query MongoDB]
    
    QueryExcel --> GenerateExcel[Gerar arquivo:
    - OpenPyXL
    - Criar planilha
    - Adicionar dados
    - Formatar células]
    
    QueryPDF --> GeneratePDF[Gerar arquivo:
    - ReportLab
    - Criar documento
    - Adicionar tabela
    - Estilizar]
    
    GenerateExcel --> StreamExcel[Stream response]
    GeneratePDF --> StreamPDF[Stream response]
    
    StreamExcel --> DownloadExcel[Download .xlsx]
    StreamPDF --> DownloadPDF[Download .pdf]
    
    DownloadExcel --> Success[Toast: Sucesso]
    DownloadPDF --> Success
    
    Success --> End([Arquivo salvo])
    
    QueryExcel -->|Erro| Error[Exibir erro]
    QueryPDF -->|Erro| Error
    Error --> Select
    
    style Start fill:#0A1F51,color:#fff
    style End fill:#28A745,color:#fff
    style GenerateExcel fill:#28A745,color:#fff
    style GeneratePDF fill:#DC3545,color:#fff
```

---

## 6. Fluxograma de Gestão Financeira

```mermaid
flowchart TD
    Start([Página Financeiro]) --> Load[Carregar dados]
    Load --> Summary[Exibir cards:
    - Receitas
    - Despesas
    - Saldo]
    
    Summary --> SelectTab{Selecionar aba}
    
    SelectTab -->|Despesas| TabDespesas[Aba Despesas]
    SelectTab -->|Patrocínio| TabPatr[Aba Patrocínio]
    SelectTab -->|Receitas| TabReceitas[Aba Receitas]
    
    TabDespesas --> ActionD{Ação?}
    TabPatr --> ActionP{Ação?}
    TabReceitas --> ActionR{Ação?}
    
    ActionD -->|Nova| FormDespesa[Formulário Despesa]
    ActionP -->|Novo| FormPatr[Formulário Patrocinador]
    ActionR -->|Nova| FormReceita[Formulário Receita]
    
    FormDespesa --> SaveD[POST /api/despesas]
    FormPatr --> SaveP[POST /api/patrocinadores]
    FormReceita --> SaveR[POST /api/recebimentos]
    
    SaveD --> UpdateD[Atualizar lista]
    SaveP --> UpdateP[Atualizar lista]
    SaveR --> UpdateR[Atualizar lista]
    
    UpdateD --> Recalc[Recalcular saldo]
    UpdateP --> Load
    UpdateR --> Recalc
    
    Recalc --> UpdateCards[Atualizar cards]
    UpdateCards --> End([Dados atualizados])
    
    style Start fill:#0A1F51,color:#fff
    style End fill:#28A745,color:#fff
    style Recalc fill:#FFC107,color:#0A1F51
```
