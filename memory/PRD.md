# E.C.P - Sistema de Gestão Esportiva

## Problema Original
Sistema completo de gestão esportiva para o clube amador Esporte Clube Piedade (E.C.P). Restrito a membros da diretoria. Stack: React + FastAPI + MongoDB.

## Funcionalidades Implementadas
- **Autenticação JWT** (login restrito à diretoria)
- **Dashboard** com KPIs e gráficos (filtros mês/ano)
- **Atletas** CRUD completo (com foto e pé dominante)
- **Treinos** CRUD + controle de presenças
- **Partidas** CRUD com cálculo automático de resultado
- **Financeiro** CRUD de receitas, despesas e patrocinadores (com filtros mês/ano - igual Dashboard)
- **Relatórios** exportação PDF/Excel
- **Branding** personalizado E.C.P (cores, logo, fundo estádio)
- **Diagramas** arquivos Mermaid .md em /app/docs/

## Módulos e Status
| Módulo | Status |
|--------|--------|
| Auth (JWT) | Completo |
| Dashboard + filtros | Completo |
| Atletas CRUD + foto + pé | Completo |
| Treinos CRUD + presenças | Completo |
| Partidas CRUD | Completo |
| Financeiro CRUD + filtros mês/ano | Completo |
| Relatórios PDF/Excel | Completo |
| Branding E.C.P | Completo |
| Diagramas .md | Completo |
| Diagramas .png | Pendente (script criado, não executado) |

## Credenciais
- Email: diretoria@ecp.com.br / Senha: ecp2024

## Backlog
- P1: Gerar diagramas como imagens PNG (script em /app/docs/gerar_diagramas.py)
