# E.C.P - Sistema de Gestão Esportiva

## Problema Original
Sistema completo de gestão esportiva para o clube amador Esporte Clube Piedade (E.C.P). Restrito a membros da diretoria. Stack: React + FastAPI + MongoDB.

## Funcionalidades Implementadas
- **Autenticação JWT** (login restrito à diretoria)
- **Dashboard** com KPIs coloridos e gráficos (filtros mês/ano)
- **Atletas** CRUD completo (com foto e pé dominante) - 23 atletas
- **Treinos** CRUD + controle de presenças - 59 treinos (2024-2026)
- **Partidas** CRUD com filtros por resultado (Vitória/Empate/Derrota), mês e ano - 30 partidas
- **Financeiro** CRUD de receitas, despesas e patrocinadores (com filtros mês/ano)
- **Relatórios** exportação PDF/Excel com filtros de período (mês/ano específico, ano ou todos)
- **Branding** personalizado E.C.P
- **Dados realistas** populados via seed (2024-2026)

## Credenciais
- Email: diretoria@ecp.com.br / Senha: ecp2024

## Backlog
- P2: Gerar diagramas como imagens PNG (script em /app/docs/gerar_diagramas.py)
