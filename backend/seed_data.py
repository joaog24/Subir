"""
Script para popular o banco de dados do E.C.P com dados realistas (2024-2026).
Executa via: python3 /app/backend/seed_data.py
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def make_id():
    """Gera ID único baseado em timestamp"""
    import time, random
    return str(time.time() + random.random())

async def seed():
    now = datetime.now(timezone.utc).isoformat()

    # ========== ATLETAS ==========
    existing_atletas = await db.atletas.count_documents({})
    print(f"Atletas existentes: {existing_atletas}")

    novos_atletas = [
        {"nome": "Lucas Ferreira", "posicao": "Goleiro", "telefone": "(21) 99101-2233", "pe_dominante": "direito", "ativo": True},
        {"nome": "Marcos Vinícius", "posicao": "Lateral-Direito", "telefone": "(21) 99202-3344", "pe_dominante": "direito", "ativo": True},
        {"nome": "Rafael Souza", "posicao": "Lateral-Esquerdo", "telefone": "(21) 99303-4455", "pe_dominante": "esquerdo", "ativo": True},
        {"nome": "Thiago Mendes", "posicao": "Zagueiro", "telefone": "(21) 99404-5566", "pe_dominante": "direito", "ativo": True},
        {"nome": "André Luiz", "posicao": "Zagueiro", "telefone": "(21) 99505-6677", "pe_dominante": "esquerdo", "ativo": True},
        {"nome": "Felipe Costa", "posicao": "Volante", "telefone": "(21) 99606-7788", "pe_dominante": "direito", "ativo": True},
        {"nome": "Bruno Henrique", "posicao": "Meio-campo", "telefone": "(21) 99707-8899", "pe_dominante": "ambidestro", "ativo": True},
        {"nome": "Diego Almeida", "posicao": "Meio-campo", "telefone": "(21) 99808-9900", "pe_dominante": "esquerdo", "ativo": True},
        {"nome": "Gustavo Ribeiro", "posicao": "Meia-Atacante", "telefone": "(21) 99909-0011", "pe_dominante": "direito", "ativo": True},
        {"nome": "Leandro Silva", "posicao": "Atacante", "telefone": "(21) 98101-1122", "pe_dominante": "direito", "ativo": True},
        {"nome": "Matheus Rocha", "posicao": "Atacante", "telefone": "(21) 98202-2233", "pe_dominante": "esquerdo", "ativo": True},
        {"nome": "Vinícius Ramos", "posicao": "Ponta-Direita", "telefone": "(21) 98303-3344", "pe_dominante": "direito", "ativo": True},
        {"nome": "Caio Nascimento", "posicao": "Ponta-Esquerda", "telefone": "(21) 98404-4455", "pe_dominante": "esquerdo", "ativo": True},
        {"nome": "Gabriel Martins", "posicao": "Volante", "telefone": "(21) 98505-5566", "pe_dominante": "direito", "ativo": True},
        {"nome": "Rodrigo Pereira", "posicao": "Goleiro", "telefone": "(21) 98606-6677", "pe_dominante": "direito", "ativo": True},
        {"nome": "Henrique Barros", "posicao": "Lateral-Direito", "telefone": "(21) 98707-7788", "pe_dominante": "direito", "ativo": False},
        {"nome": "Patrick Azevedo", "posicao": "Meio-campo", "telefone": "(21) 98808-8899", "pe_dominante": "direito", "ativo": False},
        {"nome": "Eduardo Nunes", "posicao": "Atacante", "telefone": "(21) 98909-9900", "pe_dominante": "ambidestro", "ativo": True},
    ]

    for a in novos_atletas:
        exists = await db.atletas.find_one({"nome": a["nome"]})
        if not exists:
            a["id"] = make_id()
            a["foto"] = None
            a["criado_em"] = now
            await db.atletas.insert_one(a)
            print(f"  + Atleta: {a['nome']}")

    # ========== PATROCINADORES ==========
    novos_patrocinadores = [
        {"nome": "Materiais São Jorge", "tipo": "Comércio Local", "contato": "(21) 3333-1010", "ativo": True},
        {"nome": "Auto Peças Piedade", "tipo": "Comércio Local", "contato": "(21) 3333-2020", "ativo": True},
        {"nome": "Restaurante Sabor da Serra", "tipo": "Alimentação", "contato": "(21) 3333-3030", "ativo": True},
        {"nome": "Farmácia Popular Piedade", "tipo": "Saúde", "contato": "(21) 3333-4040", "ativo": True},
        {"nome": "Imobiliária Nova Casa", "tipo": "Imobiliária", "contato": "(21) 3333-5050", "ativo": False},
        {"nome": "Academia Força Total", "tipo": "Esporte", "contato": "(21) 3333-6060", "ativo": True},
        {"nome": "Mercado Bom Preço", "tipo": "Supermercado", "contato": "(21) 3333-7070", "ativo": True},
    ]

    for p in novos_patrocinadores:
        exists = await db.patrocinadores.find_one({"nome": p["nome"]})
        if not exists:
            p["id"] = make_id()
            p["criado_em"] = now
            await db.patrocinadores.insert_one(p)
            print(f"  + Patrocinador: {p['nome']}")

    # Buscar IDs dos patrocinadores para vincular receitas
    all_patrs = await db.patrocinadores.find({"ativo": True}, {"_id": 0}).to_list(100)
    patr_ids = [p["id"] for p in all_patrs]

    # ========== TREINOS (2024-2026) ==========
    treinos_data = [
        # 2024
        ("2024-01-15", "Campo do Piedade"), ("2024-01-22", "Campo do Piedade"),
        ("2024-02-05", "Campo do Piedade"), ("2024-02-19", "Quadra Coberta"),
        ("2024-03-04", "Campo do Piedade"), ("2024-03-18", "Campo do Piedade"),
        ("2024-04-08", "Campo do Piedade"), ("2024-04-22", "Quadra Coberta"),
        ("2024-05-06", "Campo do Piedade"), ("2024-05-20", "Campo do Piedade"),
        ("2024-06-03", "Campo do Piedade"), ("2024-06-17", "Campo do Piedade"),
        ("2024-07-01", "Campo do Piedade"), ("2024-07-15", "Quadra Coberta"),
        ("2024-08-05", "Campo do Piedade"), ("2024-08-19", "Campo do Piedade"),
        ("2024-09-02", "Campo do Piedade"), ("2024-09-16", "Campo do Piedade"),
        ("2024-10-07", "Campo do Piedade"), ("2024-10-21", "Quadra Coberta"),
        ("2024-11-04", "Campo do Piedade"), ("2024-11-18", "Campo do Piedade"),
        ("2024-12-02", "Campo do Piedade"), ("2024-12-16", "Quadra Coberta"),
        # 2025
        ("2025-01-13", "Campo do Piedade"), ("2025-01-27", "Campo do Piedade"),
        ("2025-02-10", "Campo do Piedade"), ("2025-02-24", "Quadra Coberta"),
        ("2025-03-10", "Campo do Piedade"), ("2025-03-24", "Campo do Piedade"),
        ("2025-04-07", "Campo do Piedade"), ("2025-04-21", "Quadra Coberta"),
        ("2025-05-05", "Campo do Piedade"), ("2025-05-19", "Campo do Piedade"),
        ("2025-06-02", "Campo do Piedade"), ("2025-06-16", "Campo do Piedade"),
        ("2025-07-07", "Campo do Piedade"), ("2025-07-21", "Quadra Coberta"),
        ("2025-08-04", "Campo do Piedade"), ("2025-08-18", "Campo do Piedade"),
        ("2025-09-01", "Campo do Piedade"), ("2025-09-15", "Campo do Piedade"),
        ("2025-10-06", "Campo do Piedade"), ("2025-10-20", "Quadra Coberta"),
        ("2025-11-03", "Campo do Piedade"), ("2025-11-17", "Campo do Piedade"),
        ("2025-12-01", "Campo do Piedade"), ("2025-12-15", "Quadra Coberta"),
        # 2026
        ("2026-01-12", "Campo do Piedade"), ("2026-01-26", "Campo do Piedade"),
        ("2026-02-09", "Campo do Piedade"), ("2026-02-23", "Quadra Coberta"),
        ("2026-03-09", "Campo do Piedade"), ("2026-03-23", "Campo do Piedade"),
        ("2026-04-06", "Campo do Piedade"), ("2026-04-20", "Quadra Coberta"),
    ]

    observacoes_list = [
        "Treino tático com foco em marcação",
        "Trabalho físico e corrida intervalada",
        "Treino de finalização",
        "Coletivo preparatório para o jogo",
        "Aquecimento e treino de passes",
        "Treino de bola parada",
        "Trabalho de posse de bola",
        "Treino regenerativo pós-jogo",
        "Aprioramento de jogadas ensaiadas",
        "Treino de resistência e força",
    ]

    import random
    for i, (data, local) in enumerate(treinos_data):
        exists = await db.treinos.find_one({"data": data, "local": local})
        if not exists:
            obs = observacoes_list[i % len(observacoes_list)]
            treino = {
                "id": make_id(),
                "data": data,
                "local": local,
                "observacoes": obs,
                "criado_em": now,
            }
            await db.treinos.insert_one(treino)
            print(f"  + Treino: {data} - {local}")

    # ========== PARTIDAS (2024-2026) ==========
    partidas_data = [
        # 2024
        ("2024-02-11", "Atlético Madureira", "Campo do Piedade", 2, 1),
        ("2024-03-10", "São Cristóvão FC", "Campo Adversário", 1, 1),
        ("2024-04-14", "União de Bangu", "Campo do Piedade", 3, 0),
        ("2024-05-12", "Cosmos FC", "Campo Adversário", 0, 2),
        ("2024-06-09", "Realengo AC", "Campo do Piedade", 4, 1),
        ("2024-07-14", "Guaratiba EC", "Campo Adversário", 2, 2),
        ("2024-08-11", "Pedra de Guaratiba", "Campo do Piedade", 1, 0),
        ("2024-09-08", "Campo Grande FC", "Campo Adversário", 1, 3),
        ("2024-10-13", "Bangu AC Sub-23", "Campo do Piedade", 2, 0),
        ("2024-11-10", "Santa Cruz RJ", "Campo Adversário", 3, 2),
        ("2024-12-08", "Paciência FC", "Campo do Piedade", 0, 0),
        # 2025
        ("2025-01-19", "Atlético Madureira", "Campo Adversário", 1, 2),
        ("2025-02-16", "São Cristóvão FC", "Campo do Piedade", 2, 0),
        ("2025-03-16", "União de Bangu", "Campo Adversário", 0, 1),
        ("2025-04-13", "Cosmos FC", "Campo do Piedade", 3, 1),
        ("2025-05-18", "Realengo AC", "Campo Adversário", 2, 2),
        ("2025-06-15", "Guaratiba EC", "Campo do Piedade", 1, 0),
        ("2025-07-13", "Pedra de Guaratiba", "Campo Adversário", 2, 1),
        ("2025-08-10", "Campo Grande FC", "Campo do Piedade", 4, 2),
        ("2025-09-14", "Bangu AC Sub-23", "Campo Adversário", 0, 1),
        ("2025-10-12", "Santa Cruz RJ", "Campo do Piedade", 3, 3),
        ("2025-11-09", "Paciência FC", "Campo Adversário", 2, 0),
        ("2025-12-07", "Sepetiba FC", "Campo do Piedade", 1, 1),
        # 2026
        ("2026-01-18", "Atlético Madureira", "Campo do Piedade", 3, 0),
        ("2026-02-15", "São Cristóvão FC", "Campo Adversário", 2, 1),
        ("2026-03-15", "União de Bangu", "Campo do Piedade", 1, 0),
        ("2026-04-12", "Cosmos FC", "Campo Adversário", 2, 2),
    ]

    for data, adv, local, gc, ga in partidas_data:
        exists = await db.partidas.find_one({"data": data, "adversario": adv})
        if not exists:
            if gc > ga:
                res = "Vitória"
            elif gc < ga:
                res = "Derrota"
            else:
                res = "Empate"
            partida = {
                "id": make_id(),
                "data": data,
                "adversario": adv,
                "local": local,
                "gols_clube": gc,
                "gols_adversario": ga,
                "resultado": res,
                "criado_em": now,
            }
            await db.partidas.insert_one(partida)
            print(f"  + Partida: {data} vs {adv} ({gc}x{ga})")

    # ========== RECEBIMENTOS / RECEITAS (2024-2026) ==========
    receitas_data = [
        # 2024
        ("2024-01-10", "Mensalidade dos sócios - Janeiro", 850.00, None),
        ("2024-02-10", "Mensalidade dos sócios - Fevereiro", 780.00, None),
        ("2024-03-10", "Mensalidade dos sócios - Março", 900.00, None),
        ("2024-03-20", "Patrocínio trimestral", 1500.00, 0),
        ("2024-04-10", "Mensalidade dos sócios - Abril", 820.00, None),
        ("2024-05-10", "Mensalidade dos sócios - Maio", 870.00, None),
        ("2024-06-10", "Mensalidade dos sócios - Junho", 750.00, None),
        ("2024-06-25", "Patrocínio trimestral", 1500.00, 1),
        ("2024-07-10", "Mensalidade dos sócios - Julho", 680.00, None),
        ("2024-07-20", "Renda de jogo beneficente", 2200.00, None),
        ("2024-08-10", "Mensalidade dos sócios - Agosto", 830.00, None),
        ("2024-09-10", "Mensalidade dos sócios - Setembro", 900.00, None),
        ("2024-09-30", "Patrocínio trimestral", 1500.00, 2),
        ("2024-10-10", "Mensalidade dos sócios - Outubro", 850.00, None),
        ("2024-11-10", "Mensalidade dos sócios - Novembro", 790.00, None),
        ("2024-12-10", "Mensalidade dos sócios - Dezembro", 920.00, None),
        ("2024-12-20", "Patrocínio trimestral", 1500.00, 3),
        ("2024-12-28", "Renda torneio de fim de ano", 3500.00, None),
        # 2025
        ("2025-01-10", "Mensalidade dos sócios - Janeiro", 950.00, None),
        ("2025-02-10", "Mensalidade dos sócios - Fevereiro", 880.00, None),
        ("2025-03-10", "Mensalidade dos sócios - Março", 920.00, None),
        ("2025-03-25", "Patrocínio trimestral", 1800.00, 0),
        ("2025-04-10", "Mensalidade dos sócios - Abril", 900.00, None),
        ("2025-04-20", "Venda de camisetas oficiais", 1200.00, None),
        ("2025-05-10", "Mensalidade dos sócios - Maio", 870.00, None),
        ("2025-06-10", "Mensalidade dos sócios - Junho", 810.00, None),
        ("2025-06-28", "Patrocínio trimestral", 1800.00, 1),
        ("2025-07-10", "Mensalidade dos sócios - Julho", 750.00, None),
        ("2025-08-10", "Mensalidade dos sócios - Agosto", 930.00, None),
        ("2025-08-15", "Renda de jogo beneficente", 2800.00, None),
        ("2025-09-10", "Mensalidade dos sócios - Setembro", 950.00, None),
        ("2025-09-30", "Patrocínio trimestral", 1800.00, 2),
        ("2025-10-10", "Mensalidade dos sócios - Outubro", 900.00, None),
        ("2025-11-10", "Mensalidade dos sócios - Novembro", 860.00, None),
        ("2025-12-10", "Mensalidade dos sócios - Dezembro", 980.00, None),
        ("2025-12-22", "Patrocínio trimestral", 1800.00, 3),
        ("2025-12-30", "Renda torneio de fim de ano", 4000.00, None),
        # 2026
        ("2026-01-10", "Mensalidade dos sócios - Janeiro", 1000.00, None),
        ("2026-02-10", "Mensalidade dos sócios - Fevereiro", 950.00, None),
        ("2026-03-10", "Mensalidade dos sócios - Março", 980.00, None),
        ("2026-03-28", "Patrocínio trimestral", 2000.00, 4),
        ("2026-04-10", "Mensalidade dos sócios - Abril", 1020.00, None),
    ]

    for data, desc, valor, patr_idx in receitas_data:
        exists = await db.recebimentos.find_one({"data": data, "descricao": desc})
        if not exists:
            patr_id = patr_ids[patr_idx] if patr_idx is not None and patr_idx < len(patr_ids) else None
            rec = {
                "id": make_id(),
                "descricao": desc,
                "valor": valor,
                "data": data,
                "patrocinador_id": patr_id,
                "criado_em": now,
            }
            await db.recebimentos.insert_one(rec)
            print(f"  + Receita: {data} - {desc} R${valor}")

    # ========== DESPESAS (2024-2026) ==========
    despesas_data = [
        # 2024
        ("2024-01-05", "Aluguel do campo - Janeiro", "Infraestrutura", 400.00),
        ("2024-01-20", "Compra de uniformes treino", "Material Esportivo", 1200.00),
        ("2024-02-05", "Aluguel do campo - Fevereiro", "Infraestrutura", 400.00),
        ("2024-02-15", "Compra de bolas (10 unid.)", "Material Esportivo", 800.00),
        ("2024-03-05", "Aluguel do campo - Março", "Infraestrutura", 400.00),
        ("2024-03-25", "Transporte para jogo fora", "Transporte", 350.00),
        ("2024-04-05", "Aluguel do campo - Abril", "Infraestrutura", 400.00),
        ("2024-04-18", "Água e isotônico (mês)", "Alimentação", 180.00),
        ("2024-05-05", "Aluguel do campo - Maio", "Infraestrutura", 400.00),
        ("2024-05-20", "Transporte para jogo fora", "Transporte", 380.00),
        ("2024-06-05", "Aluguel do campo - Junho", "Infraestrutura", 400.00),
        ("2024-06-15", "Manutenção de coletes e cones", "Material Esportivo", 250.00),
        ("2024-07-05", "Aluguel do campo - Julho", "Infraestrutura", 400.00),
        ("2024-07-18", "Taxa de inscrição campeonato", "Campeonato", 600.00),
        ("2024-08-05", "Aluguel do campo - Agosto", "Infraestrutura", 400.00),
        ("2024-08-22", "Transporte para jogo fora", "Transporte", 400.00),
        ("2024-09-05", "Aluguel do campo - Setembro", "Infraestrutura", 400.00),
        ("2024-09-10", "Água e isotônico (mês)", "Alimentação", 200.00),
        ("2024-10-05", "Aluguel do campo - Outubro", "Infraestrutura", 400.00),
        ("2024-10-15", "Transporte para jogo fora", "Transporte", 350.00),
        ("2024-11-05", "Aluguel do campo - Novembro", "Infraestrutura", 400.00),
        ("2024-11-20", "Compra de uniformes jogo", "Material Esportivo", 2500.00),
        ("2024-12-05", "Aluguel do campo - Dezembro", "Infraestrutura", 400.00),
        ("2024-12-22", "Confraternização fim de ano", "Eventos", 1500.00),
        # 2025
        ("2025-01-05", "Aluguel do campo - Janeiro", "Infraestrutura", 450.00),
        ("2025-01-18", "Compra de coletes novos", "Material Esportivo", 350.00),
        ("2025-02-05", "Aluguel do campo - Fevereiro", "Infraestrutura", 450.00),
        ("2025-02-20", "Compra de bolas (8 unid.)", "Material Esportivo", 720.00),
        ("2025-03-05", "Aluguel do campo - Março", "Infraestrutura", 450.00),
        ("2025-03-22", "Transporte para jogo fora", "Transporte", 400.00),
        ("2025-04-05", "Aluguel do campo - Abril", "Infraestrutura", 450.00),
        ("2025-04-15", "Água e isotônico (mês)", "Alimentação", 220.00),
        ("2025-05-05", "Aluguel do campo - Maio", "Infraestrutura", 450.00),
        ("2025-05-18", "Transporte para jogo fora", "Transporte", 420.00),
        ("2025-06-05", "Aluguel do campo - Junho", "Infraestrutura", 450.00),
        ("2025-06-20", "Manutenção de equipamentos", "Material Esportivo", 300.00),
        ("2025-07-05", "Aluguel do campo - Julho", "Infraestrutura", 450.00),
        ("2025-07-15", "Taxa inscrição campeonato 2º sem.", "Campeonato", 700.00),
        ("2025-08-05", "Aluguel do campo - Agosto", "Infraestrutura", 450.00),
        ("2025-08-20", "Transporte para jogo fora", "Transporte", 380.00),
        ("2025-09-05", "Aluguel do campo - Setembro", "Infraestrutura", 450.00),
        ("2025-09-12", "Água e isotônico (mês)", "Alimentação", 230.00),
        ("2025-10-05", "Aluguel do campo - Outubro", "Infraestrutura", 450.00),
        ("2025-10-18", "Transporte para jogo fora", "Transporte", 400.00),
        ("2025-11-05", "Aluguel do campo - Novembro", "Infraestrutura", 450.00),
        ("2025-11-25", "Compra de uniformes jogo (novos)", "Material Esportivo", 2800.00),
        ("2025-12-05", "Aluguel do campo - Dezembro", "Infraestrutura", 450.00),
        ("2025-12-20", "Confraternização fim de ano", "Eventos", 1800.00),
        # 2026
        ("2026-01-05", "Aluguel do campo - Janeiro", "Infraestrutura", 500.00),
        ("2026-01-15", "Compra de meias e caneleiras", "Material Esportivo", 600.00),
        ("2026-02-05", "Aluguel do campo - Fevereiro", "Infraestrutura", 500.00),
        ("2026-02-20", "Compra de bolas (12 unid.)", "Material Esportivo", 1080.00),
        ("2026-03-05", "Aluguel do campo - Março", "Infraestrutura", 500.00),
        ("2026-03-18", "Transporte para jogo fora", "Transporte", 450.00),
        ("2026-04-05", "Aluguel do campo - Abril", "Infraestrutura", 500.00),
        ("2026-04-15", "Água e isotônico (mês)", "Alimentação", 250.00),
    ]

    for data, desc, cat, valor in despesas_data:
        exists = await db.despesas.find_one({"data": data, "descricao": desc})
        if not exists:
            desp = {
                "id": make_id(),
                "descricao": desc,
                "categoria": cat,
                "valor": valor,
                "data": data,
                "criado_em": now,
            }
            await db.despesas.insert_one(desp)
            print(f"  + Despesa: {data} - {desc} R${valor}")

    # ========== RESUMO ==========
    total_atletas = await db.atletas.count_documents({})
    total_treinos = await db.treinos.count_documents({})
    total_partidas = await db.partidas.count_documents({})
    total_rec = await db.recebimentos.count_documents({})
    total_desp = await db.despesas.count_documents({})
    total_patr = await db.patrocinadores.count_documents({})

    print("\n========== RESUMO ==========")
    print(f"Atletas: {total_atletas}")
    print(f"Patrocinadores: {total_patr}")
    print(f"Treinos: {total_treinos}")
    print(f"Partidas: {total_partidas}")
    print(f"Receitas: {total_rec}")
    print(f"Despesas: {total_desp}")
    print("Seed concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed())
