# E.C.P - Sistema de Gestão Esportiva

## Problema Original
Sistema completo de gestão esportiva para o clube amador Esporte Clube Piedade (E.C.P). Restrito a membros da diretoria. Stack: React + FastAPI + MongoDB.

## Funcionalidades Implementadas
- **Autenticação JWT** (login restrito à diretoria)
- **Dashboard** com KPIs e gráficos (filtros mês/ano)
- **Atletas** CRUD completo (com foto e pé dominante) - 23 atletas cadastrados
- **Treinos** CRUD + controle de presenças - 59 treinos (2024-2026)
- **Partidas** CRUD com cálculo automático de resultado - 30 partidas (2024-2026)
- **Financeiro** CRUD de receitas, despesas e patrocinadores (com filtros mês/ano) - 51 receitas, 58 despesas, 8 patrocinadores
- **Relatórios** exportação PDF/Excel
- **Branding** personalizado E.C.P
- **Dados realistas** populados via seed script (2024-2026)

## Credenciais
- Email: diretoria@ecp.com.br / Senha: ecp2024

## Backlog
- P1: Gerar diagramas como imagens PNG (script em /app/docs/gerar_diagramas.py)
