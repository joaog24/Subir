import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

os.makedirs('/app/docs/imagens', exist_ok=True)

# Cores do E.C.P
AZUL_ESCURO = '#0A1F51'
AZUL_ROYAL = '#002B8C'
AMARELO = '#FFC107'
VERDE = '#28A745'
VERMELHO = '#DC3545'
BRANCO = '#FFFFFF'
CINZA_CLARO = '#F8F9FA'
CINZA = '#6C757D'

# ============================================================
# 1. DIAGRAMA DE CASOS DE USO
# ============================================================
def gerar_casos_uso():
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor(BRANCO)
    
    # Titulo
    ax.text(11, 15.5, 'DIAGRAMA DE CASOS DE USO - E.C.P MANAGER', 
            ha='center', va='center', fontsize=18, fontweight='bold', color=AZUL_ESCURO)
    ax.text(11, 15.0, 'Esporte Clube Piedade - Sistema de Gerenciamento', 
            ha='center', va='center', fontsize=11, color=CINZA)

    # Ator
    ax.add_patch(plt.Circle((1.5, 8), 0.5, color=AZUL_ESCURO, zorder=5))
    ax.text(1.5, 8, '👤', ha='center', va='center', fontsize=20, zorder=6)
    ax.text(1.5, 7.0, 'Administrador\n(Diretoria)', ha='center', va='center', fontsize=9, fontweight='bold', color=AZUL_ESCURO)

    # Grupos de Casos de Uso
    grupos = [
        {'nome': 'Autenticação', 'x': 5, 'y': 14, 'cor': VERMELHO,
         'casos': ['Fazer Login', 'Fazer Logout', 'Registrar Usuário']},
        {'nome': 'Gestão de Atletas', 'x': 10, 'y': 14, 'cor': AZUL_ROYAL,
         'casos': ['Cadastrar Atleta', 'Editar Atleta', 'Excluir Atleta', 'Buscar Atleta', 'Upload Foto', 'Definir Pé Dominante']},
        {'nome': 'Gestão de Treinos', 'x': 16, 'y': 14, 'cor': VERDE,
         'casos': ['Cadastrar Treino', 'Editar Treino', 'Excluir Treino', 'Registrar Presença', 'Ver Presenças']},
        {'nome': 'Gestão de Partidas', 'x': 5, 'y': 7.5, 'cor': AMARELO,
         'casos': ['Cadastrar Partida', 'Editar Partida', 'Excluir Partida', 'Ver Resultado Auto.']},
        {'nome': 'Gestão Financeira', 'x': 10, 'y': 7.5, 'cor': '#E91E63',
         'casos': ['Registrar Receita', 'Registrar Despesa', 'Cadastrar Patrocinador', 'Visualizar Saldo']},
        {'nome': 'Dashboard e Relatórios', 'x': 16, 'y': 7.5, 'cor': '#9C27B0',
         'casos': ['Ver Dashboard', 'Filtrar Período', 'Ver Gráficos', 'Exportar Excel', 'Exportar PDF']},
    ]
    
    for grupo in grupos:
        x, y = grupo['x'], grupo['y']
        n = len(grupo['casos'])
        h = n * 0.6 + 1.2
        
        rect = FancyBboxPatch((x-2.2, y-h), 4.4, h, boxstyle="round,pad=0.15",
                               facecolor=BRANCO, edgecolor=grupo['cor'], linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y-0.3, grupo['nome'], ha='center', va='center', fontsize=10, 
                fontweight='bold', color=grupo['cor'])
        
        for i, caso in enumerate(grupo['casos']):
            cy = y - 1.0 - i * 0.6
            elipse = mpatches.Ellipse((x, cy), 3.8, 0.5, facecolor=grupo['cor']+'20',
                                       edgecolor=grupo['cor'], linewidth=1.2)
            ax.add_patch(elipse)
            ax.text(x, cy, caso, ha='center', va='center', fontsize=7.5, color=AZUL_ESCURO)
            
            ax.annotate('', xy=(x-2.2, cy), xytext=(2, 8),
                        arrowprops=dict(arrowstyle='->', color=CINZA, lw=0.5, alpha=0.3))

    # Legenda
    ax.text(11, 0.8, 'Todos os casos de uso requerem autenticação via JWT | Ator único: Diretoria do Clube',
            ha='center', va='center', fontsize=9, style='italic', color=CINZA)

    plt.tight_layout()
    plt.savefig('/app/docs/imagens/01-diagrama-casos-uso.png', dpi=150, bbox_inches='tight',
                facecolor=BRANCO, edgecolor='none')
    plt.close()
    print('✓ 1/5 - Diagrama de Casos de Uso gerado')

# ============================================================
# 2. DIAGRAMA DE ARQUITETURA
# ============================================================
def gerar_arquitetura():
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor(BRANCO)

    ax.text(10, 13.5, 'DIAGRAMA DE ARQUITETURA DO SISTEMA - E.C.P MANAGER',
            ha='center', va='center', fontsize=18, fontweight='bold', color=AZUL_ESCURO)
    ax.text(10, 13.0, 'React + FastAPI + MongoDB no Kubernetes',
            ha='center', va='center', fontsize=11, color=CINZA)

    # Navegador
    rect = FancyBboxPatch((7.5, 11.5), 5, 1, boxstyle="round,pad=0.2",
                           facecolor='#E3F2FD', edgecolor=AZUL_ROYAL, linewidth=2)
    ax.add_patch(rect)
    ax.text(10, 12, '🌐 Navegador Web (Usuário)', ha='center', va='center',
            fontsize=12, fontweight='bold', color=AZUL_ESCURO)

    # Seta
    ax.annotate('', xy=(10, 10.5), xytext=(10, 11.5),
                arrowprops=dict(arrowstyle='->', color=AZUL_ROYAL, lw=2))
    ax.text(10.5, 11, 'HTTPS', ha='left', va='center', fontsize=8, color=CINZA)

    # Kubernetes
    kube = FancyBboxPatch((1, 1), 18, 9.5), 
    rect_k = FancyBboxPatch((1, 1), 18, 9.5, boxstyle="round,pad=0.3",
                             facecolor='#F5F5F5', edgecolor='#326CE5', linewidth=2.5, linestyle='--')
    ax.add_patch(rect_k)
    ax.text(10, 10.2, '☸ Cluster Kubernetes', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#326CE5')

    # Ingress
    rect_i = FancyBboxPatch((7, 9), 6, 0.8, boxstyle="round,pad=0.15",
                             facecolor='#326CE5', edgecolor='#1A237E', linewidth=1.5)
    ax.add_patch(rect_i)
    ax.text(10, 9.4, 'Ingress Controller', ha='center', va='center',
            fontsize=10, fontweight='bold', color=BRANCO)

    # Setas do Ingress
    ax.annotate('', xy=(5, 8), xytext=(8.5, 9),
                arrowprops=dict(arrowstyle='->', color=AZUL_ROYAL, lw=1.5))
    ax.text(5.5, 8.8, '/ (páginas)', ha='left', va='center', fontsize=8, color=CINZA)
    
    ax.annotate('', xy=(15, 8), xytext=(11.5, 9),
                arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.5))
    ax.text(13.5, 8.8, '/api/* (dados)', ha='left', va='center', fontsize=8, color=CINZA)

    # Frontend
    rect_f = FancyBboxPatch((2, 4.5), 6, 3.5, boxstyle="round,pad=0.2",
                             facecolor='#E8F5E9', edgecolor='#61DAFB', linewidth=2)
    ax.add_patch(rect_f)
    ax.text(5, 7.7, '⚛️ Frontend - React', ha='center', va='center',
            fontsize=11, fontweight='bold', color=AZUL_ESCURO)
    
    front_items = ['React 18 + Router', 'Shadcn UI + Tailwind CSS', 'Recharts (Gráficos)',
                   'Axios (HTTP Client)', 'Sonner (Notificações)', 'Porta: 3000']
    for i, item in enumerate(front_items):
        ax.text(5, 7.1 - i*0.4, f'• {item}', ha='center', va='center',
                fontsize=8, color=AZUL_ESCURO)

    # Backend
    rect_b = FancyBboxPatch((12, 4.5), 6, 3.5, boxstyle="round,pad=0.2",
                             facecolor='#FFF3E0', edgecolor='#009688', linewidth=2)
    ax.add_patch(rect_b)
    ax.text(15, 7.7, '⚡ Backend - FastAPI', ha='center', va='center',
            fontsize=11, fontweight='bold', color=AZUL_ESCURO)
    
    back_items = ['FastAPI + Uvicorn', 'Autenticação JWT', 'Pydantic (Validação)',
                  'Motor (MongoDB Async)', 'OpenPyXL + ReportLab', 'Porta: 8001']
    for i, item in enumerate(back_items):
        ax.text(15, 7.1 - i*0.4, f'• {item}', ha='center', va='center',
                fontsize=8, color=AZUL_ESCURO)

    # Seta Frontend -> Backend
    ax.annotate('', xy=(12, 6.2), xytext=(8, 6.2),
                arrowprops=dict(arrowstyle='<->', color=AZUL_ROYAL, lw=1.5))
    ax.text(10, 6.5, 'API REST', ha='center', va='center', fontsize=8, fontweight='bold', color=AZUL_ROYAL)

    # MongoDB
    rect_m = FancyBboxPatch((10, 1.5), 6, 2.5, boxstyle="round,pad=0.2",
                             facecolor='#E8F5E9', edgecolor='#47A248', linewidth=2)
    ax.add_patch(rect_m)
    ax.text(13, 3.7, '🗄️ MongoDB', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#47A248')
    
    collections = 'Collections: usuarios, atletas, treinos,\npresenças, partidas, patrocinadores,\nrecebimentos, despesas'
    ax.text(13, 2.5, collections, ha='center', va='center', fontsize=8, color=AZUL_ESCURO)

    # Seta Backend -> MongoDB
    ax.annotate('', xy=(14, 4), xytext=(14, 4.5),
                arrowprops=dict(arrowstyle='<->', color='#47A248', lw=2))
    ax.text(14.5, 4.25, 'Motor AsyncIO', ha='left', va='center', fontsize=8, color='#47A248')

    # Env
    rect_e = FancyBboxPatch((2, 1.5), 6, 2.5, boxstyle="round,pad=0.2",
                             facecolor='#FCE4EC', edgecolor=VERMELHO, linewidth=1.5, linestyle='--')
    ax.add_patch(rect_e)
    ax.text(5, 3.7, '🔐 Configuração (.env)', ha='center', va='center',
            fontsize=10, fontweight='bold', color=VERMELHO)
    env_items = ['REACT_APP_BACKEND_URL', 'MONGO_URL', 'DB_NAME',
                 'JWT_SECRET', 'CORS_ORIGINS']
    for i, item in enumerate(env_items):
        ax.text(5, 3.1 - i*0.35, f'• {item}', ha='center', va='center',
                fontsize=8, color=AZUL_ESCURO)

    plt.tight_layout()
    plt.savefig('/app/docs/imagens/02-diagrama-arquitetura.png', dpi=150, bbox_inches='tight',
                facecolor=BRANCO, edgecolor='none')
    plt.close()
    print('✓ 2/5 - Diagrama de Arquitetura gerado')

# ============================================================
# 3. DIAGRAMA DE BANCO DE DADOS (ERD)
# ============================================================
def gerar_banco_dados():
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor(BRANCO)

    ax.text(11, 15.5, 'DIAGRAMA DE BANCO DE DADOS (ERD) - E.C.P MANAGER',
            ha='center', va='center', fontsize=18, fontweight='bold', color=AZUL_ESCURO)
    ax.text(11, 15.0, 'MongoDB - Modelo Entidade-Relacionamento',
            ha='center', va='center', fontsize=11, color=CINZA)

    def draw_table(ax, x, y, name, fields, color, pk_fields=None, fk_fields=None):
        if pk_fields is None: pk_fields = ['id']
        if fk_fields is None: fk_fields = []
        
        w, row_h = 4.2, 0.35
        h = (len(fields) + 1) * row_h + 0.2
        
        # Header
        rect_h = FancyBboxPatch((x, y), w, row_h + 0.1, boxstyle="round,pad=0.05",
                                 facecolor=color, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect_h)
        ax.text(x + w/2, y + row_h/2 + 0.05, name, ha='center', va='center',
                fontsize=10, fontweight='bold', color=BRANCO)
        
        # Body
        rect_b = FancyBboxPatch((x, y - len(fields)*row_h - 0.1), w, len(fields)*row_h + 0.1,
                                 boxstyle="round,pad=0.05", facecolor=BRANCO, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect_b)
        
        for i, (fname, ftype) in enumerate(fields):
            fy = y - (i+1)*row_h + 0.05
            prefix = ''
            fc = AZUL_ESCURO
            if fname in pk_fields:
                prefix = '🔑 '
                fc = color
            elif fname in fk_fields:
                prefix = '🔗 '
                fc = VERMELHO
            ax.text(x + 0.15, fy, f'{prefix}{fname}', ha='left', va='center',
                    fontsize=7.5, fontweight='bold' if fname in pk_fields else 'normal', color=fc)
            ax.text(x + w - 0.15, fy, ftype, ha='right', va='center',
                    fontsize=7, color=CINZA)
        
        return (x + w/2, y - len(fields)*row_h/2)

    # Tabelas
    draw_table(ax, 0.5, 14, 'USUARIOS', [
        ('id', 'string PK'), ('nome', 'string'), ('email', 'string UK'),
        ('senha', 'string'), ('ativo', 'boolean'), ('criado_em', 'datetime')
    ], AZUL_ROYAL)

    draw_table(ax, 5.5, 14, 'ATLETAS', [
        ('id', 'string PK'), ('nome', 'string'), ('posicao', 'string'),
        ('telefone', 'string'), ('foto', 'string?'), ('pe_dominante', 'string?'),
        ('ativo', 'boolean'), ('criado_em', 'datetime')
    ], VERDE)

    draw_table(ax, 11, 14, 'TREINOS', [
        ('id', 'string PK'), ('data', 'string'), ('local', 'string'),
        ('observacoes', 'string?'), ('criado_em', 'datetime')
    ], '#E91E63')

    draw_table(ax, 16.5, 14, 'PRESENCAS', [
        ('id', 'string PK'), ('treino_id', 'string FK'), ('atleta_id', 'string FK'),
        ('presente', 'boolean'), ('criado_em', 'datetime')
    ], '#9C27B0', fk_fields=['treino_id', 'atleta_id'])

    draw_table(ax, 0.5, 7, 'PARTIDAS', [
        ('id', 'string PK'), ('data', 'string'), ('adversario', 'string'),
        ('local', 'string'), ('gols_clube', 'integer'), ('gols_adversario', 'integer'),
        ('resultado', 'string'), ('criado_em', 'datetime')
    ], AMARELO)

    draw_table(ax, 5.5, 7, 'PATROCINADORES', [
        ('id', 'string PK'), ('nome', 'string'), ('tipo', 'string'),
        ('contato', 'string'), ('ativo', 'boolean'), ('criado_em', 'datetime')
    ], '#FF5722')

    draw_table(ax, 11, 7, 'RECEBIMENTOS', [
        ('id', 'string PK'), ('descricao', 'string'), ('valor', 'float'),
        ('data', 'string'), ('patrocinador_id', 'string FK?'), ('criado_em', 'datetime')
    ], '#00BCD4', fk_fields=['patrocinador_id'])

    draw_table(ax, 16.5, 7, 'DESPESAS', [
        ('id', 'string PK'), ('descricao', 'string'), ('categoria', 'string'),
        ('valor', 'float'), ('data', 'string'), ('criado_em', 'datetime')
    ], VERMELHO)

    # Relacionamentos
    # Atletas <-> Presencas (N:N via Presencas)
    ax.annotate('', xy=(16.5, 12.5), xytext=(9.7, 12),
                arrowprops=dict(arrowstyle='<->', color='#9C27B0', lw=2, connectionstyle='arc3,rad=0.1'))
    ax.text(13, 13, 'N:N', ha='center', va='center', fontsize=8, fontweight='bold',
            color='#9C27B0', bbox=dict(boxstyle='round,pad=0.2', facecolor=BRANCO, edgecolor='#9C27B0'))

    # Treinos <-> Presencas (1:N)
    ax.annotate('', xy=(16.5, 13), xytext=(15.2, 13),
                arrowprops=dict(arrowstyle='->', color='#9C27B0', lw=2))
    ax.text(15.8, 13.3, '1:N', ha='center', va='center', fontsize=8, fontweight='bold',
            color='#E91E63', bbox=dict(boxstyle='round,pad=0.2', facecolor=BRANCO, edgecolor='#E91E63'))

    # Patrocinadores -> Recebimentos (1:N)
    ax.annotate('', xy=(11, 5.5), xytext=(9.7, 5.5),
                arrowprops=dict(arrowstyle='->', color='#FF5722', lw=2))
    ax.text(10.3, 5.9, '1:N', ha='center', va='center', fontsize=8, fontweight='bold',
            color='#FF5722', bbox=dict(boxstyle='round,pad=0.2', facecolor=BRANCO, edgecolor='#FF5722'))

    # Legenda
    leg_y = 0.8
    ax.text(4, leg_y, '🔑 Chave Primária', fontsize=9, color=AZUL_ESCURO)
    ax.text(8, leg_y, '🔗 Chave Estrangeira', fontsize=9, color=VERMELHO)
    ax.text(12.5, leg_y, '? = Campo Opcional', fontsize=9, color=CINZA)
    ax.text(16, leg_y, 'UK = Único', fontsize=9, color=AZUL_ROYAL)

    plt.tight_layout()
    plt.savefig('/app/docs/imagens/03-diagrama-banco-dados.png', dpi=150, bbox_inches='tight',
                facecolor=BRANCO, edgecolor='none')
    plt.close()
    print('✓ 3/5 - Diagrama de Banco de Dados gerado')

# ============================================================
# 4. FLUXOGRAMA
# ============================================================
def gerar_fluxograma():
    fig, axes = plt.subplots(2, 3, figsize=(24, 16))
    fig.patch.set_facecolor(BRANCO)
    fig.suptitle('FLUXOGRAMAS DO SISTEMA - E.C.P MANAGER', fontsize=20, fontweight='bold',
                 color=AZUL_ESCURO, y=0.98)

    def draw_box(ax, x, y, text, color, text_color=BRANCO, shape='rect', w=2.5, h=0.6):
        if shape == 'rect':
            rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.1",
                                   facecolor=color, edgecolor=color, linewidth=1.5)
            ax.add_patch(rect)
        elif shape == 'diamond':
            diamond = plt.Polygon([(x, y+h/1.5), (x+w/2, y), (x, y-h/1.5), (x-w/2, y)],
                                   facecolor=color, edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
        elif shape == 'oval':
            ellipse = mpatches.Ellipse((x, y), w, h, facecolor=color, edgecolor=color, linewidth=1.5)
            ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=7, fontweight='bold',
                color=text_color, wrap=True)

    def draw_arrow(ax, x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=CINZA, lw=1.2))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.15, my, label, fontsize=6, color=CINZA)

    # --- Fluxo 1: Autenticação ---
    ax = axes[0][0]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('1. Fluxo de Autenticação', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Tela de Login', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'Inserir\nEmail e Senha', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 6.9, 2.5, 6.3)
    draw_box(ax, 2.5, 6, 'Validar\nCredenciais?', AMARELO, AZUL_ESCURO, 'diamond', 2.8, 0.5)
    draw_arrow(ax, 1.1, 6, 0.5, 6)
    ax.text(1.3, 6.2, 'Não', fontsize=6, color=VERMELHO)
    draw_box(ax, 0.5, 5, 'Exibir Erro', VERMELHO, w=1.5)
    draw_arrow(ax, 0.5, 4.7, 0.5, 4.2)
    ax.annotate('', xy=(2.5, 8.1), xytext=(0.5, 4.2),
                arrowprops=dict(arrowstyle='->', color=CINZA, lw=1, connectionstyle='arc3,rad=-0.5'))
    draw_arrow(ax, 2.5, 5.5, 2.5, 4.8)
    ax.text(2.7, 5.2, 'Sim', fontsize=6, color=VERDE)
    draw_box(ax, 2.5, 4.5, 'Verificar Hash\nBcrypt', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 4.2, 2.5, 3.6)
    draw_box(ax, 2.5, 3.3, 'Gerar Token JWT', AMARELO, AZUL_ESCURO)
    draw_arrow(ax, 2.5, 3, 2.5, 2.4)
    draw_box(ax, 2.5, 2.1, 'Salvar Token\nno localStorage', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 1.8, 2.5, 1.2)
    draw_box(ax, 2.5, 0.9, 'DASHBOARD', VERDE, shape='oval', w=2, h=0.5)

    # --- Fluxo 2: Cadastro de Atleta ---
    ax = axes[0][1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('2. Cadastro de Atleta', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Clicar\n"Novo Atleta"', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'Preencher:\nNome, Posição,\nTelefone, Pé', AZUL_ESCURO, h=0.8)
    draw_arrow(ax, 2.5, 6.8, 2.5, 6.2)
    draw_box(ax, 2.5, 5.9, 'Adicionar\nFoto?', AMARELO, AZUL_ESCURO, 'diamond', 2.5, 0.5)
    draw_arrow(ax, 3.75, 5.9, 4.3, 5.9)
    ax.text(4, 6.1, 'Sim', fontsize=6, color=VERDE)
    draw_box(ax, 4.3, 5.1, 'Upload\nFoto', VERDE, w=1.4, h=0.5)
    draw_arrow(ax, 4.3, 4.85, 4.3, 4.4)
    draw_arrow(ax, 2.5, 5.4, 2.5, 4.2)
    ax.text(2.7, 5.0, 'Não', fontsize=6, color=VERMELHO)
    draw_box(ax, 2.5, 3.9, 'Validar\nFormulário', AMARELO, AZUL_ESCURO, 'diamond', 2.5, 0.5)
    draw_arrow(ax, 2.5, 3.4, 2.5, 2.8)
    ax.text(2.7, 3.1, 'Válido', fontsize=6, color=VERDE)
    draw_box(ax, 2.5, 2.5, 'POST /api/atletas', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 2.2, 2.5, 1.6)
    draw_box(ax, 2.5, 1.3, 'Salvar MongoDB', '#47A248')
    draw_arrow(ax, 2.5, 1, 2.5, 0.5)
    draw_box(ax, 2.5, 0.3, 'SUCESSO', VERDE, shape='oval', w=2, h=0.4)

    # --- Fluxo 3: Registro de Presença ---
    ax = axes[0][2]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('3. Registro de Presença', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Selecionar Treino', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'Clicar\n"N presentes"', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 6.9, 2.5, 6.3)
    draw_box(ax, 2.5, 6, 'Carregar Lista\nde Atletas', '#E91E63')
    draw_arrow(ax, 2.5, 5.7, 2.5, 5.1)
    draw_box(ax, 2.5, 4.8, 'Exibir Lista\ncom Checkboxes', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 4.5, 2.5, 3.9)
    draw_box(ax, 2.5, 3.6, 'Marcar/Desmarcar\nPresenças', AMARELO, AZUL_ESCURO)
    draw_arrow(ax, 2.5, 3.3, 2.5, 2.7)
    draw_box(ax, 2.5, 2.4, 'Clicar "Salvar"', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 2.1, 2.5, 1.5)
    draw_box(ax, 2.5, 1.2, 'POST\n/api/presencas/bulk', '#9C27B0')
    draw_arrow(ax, 2.5, 0.9, 2.5, 0.4)
    draw_box(ax, 2.5, 0.2, 'SUCESSO', VERDE, shape='oval', w=2, h=0.4)

    # --- Fluxo 4: Dashboard ---
    ax = axes[1][0]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('4. Dashboard com Filtros', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Verificar Token', VERMELHO)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'GET\n/api/dashboard/stats', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 6.9, 2.5, 6.3)
    draw_box(ax, 2.5, 6, 'GET\n/api/dashboard/charts', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 5.7, 2.5, 5.1)
    draw_box(ax, 2.5, 4.8, 'Exibir:\n6 KPIs + 3 Gráficos', VERDE)
    draw_arrow(ax, 2.5, 4.5, 2.5, 3.9)
    draw_box(ax, 2.5, 3.6, 'Usuário\nFiltra?', AMARELO, AZUL_ESCURO, 'diamond', 2.5, 0.5)
    draw_arrow(ax, 2.5, 3.1, 2.5, 2.5)
    ax.text(2.7, 2.8, 'Sim', fontsize=6, color=VERDE)
    draw_box(ax, 2.5, 2.2, 'Selecionar\nMês/Ano', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 1.9, 2.5, 1.3)
    draw_box(ax, 2.5, 1, 'Aggregation\nMongoDB', '#47A248')
    draw_arrow(ax, 2.5, 0.7, 2.5, 0.3)
    draw_box(ax, 2.5, 0.1, 'ATUALIZAR UI', VERDE, shape='oval', w=2, h=0.3)

    # --- Fluxo 5: Exportação ---
    ax = axes[1][1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('5. Exportação de Relatórios', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Página Relatórios', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'Selecionar Tipo:\nAtletas, Treinos,\nPartidas, Financeiro', AZUL_ESCURO, h=0.8)
    draw_arrow(ax, 2.5, 6.8, 2.5, 6.2)
    draw_box(ax, 2.5, 5.9, 'Escolher\nFormato?', AMARELO, AZUL_ESCURO, 'diamond', 2.5, 0.5)
    draw_arrow(ax, 1.25, 5.9, 0.6, 5.9)
    ax.text(0.9, 6.1, 'Excel', fontsize=6, color=VERDE)
    draw_box(ax, 0.6, 5, 'OpenPyXL\nGerar .xlsx', VERDE, w=1.5, h=0.5)
    draw_arrow(ax, 3.75, 5.9, 4.4, 5.9)
    ax.text(4.1, 6.1, 'PDF', fontsize=6, color=VERMELHO)
    draw_box(ax, 4.4, 5, 'ReportLab\nGerar .pdf', VERMELHO, w=1.5, h=0.5)
    draw_arrow(ax, 0.6, 4.75, 0.6, 4.2)
    draw_arrow(ax, 4.4, 4.75, 4.4, 4.2)
    draw_box(ax, 2.5, 3.9, 'Query MongoDB', '#47A248')
    draw_arrow(ax, 2.5, 3.6, 2.5, 3)
    draw_box(ax, 2.5, 2.7, 'Stream Response', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 2.4, 2.5, 1.8)
    draw_box(ax, 2.5, 1.5, 'Download\nArquivo', AZUL_ESCURO)
    draw_arrow(ax, 2.5, 1.2, 2.5, 0.6)
    draw_box(ax, 2.5, 0.4, 'SUCESSO', VERDE, shape='oval', w=2, h=0.4)

    # --- Fluxo 6: Financeiro ---
    ax = axes[1][2]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('6. Gestão Financeira', fontsize=12, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_box(ax, 2.5, 9.5, 'INÍCIO', VERDE, shape='oval', w=2, h=0.5)
    draw_arrow(ax, 2.5, 9.25, 2.5, 8.7)
    draw_box(ax, 2.5, 8.4, 'Página Financeiro', AZUL_ROYAL)
    draw_arrow(ax, 2.5, 8.1, 2.5, 7.5)
    draw_box(ax, 2.5, 7.2, 'Exibir Cards:\nReceitas, Despesas,\nSaldo', AZUL_ESCURO, h=0.8)
    draw_arrow(ax, 2.5, 6.8, 2.5, 6.2)
    draw_box(ax, 2.5, 5.9, 'Selecionar\nAba?', AMARELO, AZUL_ESCURO, 'diamond', 2.5, 0.5)
    
    draw_arrow(ax, 1.25, 5.9, 0.5, 5.3)
    draw_box(ax, 0.6, 5, 'Despesas', VERMELHO, w=1.3, h=0.4)
    draw_arrow(ax, 2.5, 5.4, 2.5, 4.8)
    draw_box(ax, 2.5, 4.6, 'Patrocínio', '#FF5722', w=1.3, h=0.4)
    draw_arrow(ax, 3.75, 5.9, 4.4, 5.3)
    draw_box(ax, 4.4, 5, 'Receitas', VERDE, w=1.3, h=0.4)
    
    draw_arrow(ax, 2.5, 4.4, 2.5, 3.8)
    draw_box(ax, 2.5, 3.5, 'CRUD:\nCriar, Editar,\nExcluir', AZUL_ROYAL, h=0.7)
    draw_arrow(ax, 2.5, 3.15, 2.5, 2.6)
    draw_box(ax, 2.5, 2.3, 'Salvar no\nMongoDB', '#47A248')
    draw_arrow(ax, 2.5, 2, 2.5, 1.4)
    draw_box(ax, 2.5, 1.1, 'Recalcular\nSaldo', AMARELO, AZUL_ESCURO)
    draw_arrow(ax, 2.5, 0.8, 2.5, 0.3)
    draw_box(ax, 2.5, 0.1, 'ATUALIZADO', VERDE, shape='oval', w=2, h=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/app/docs/imagens/04-fluxogramas.png', dpi=150, bbox_inches='tight',
                facecolor=BRANCO, edgecolor='none')
    plt.close()
    print('✓ 4/5 - Fluxogramas gerados')

# ============================================================
# 5. DIAGRAMA DE CLASSES
# ============================================================
def gerar_classes():
    fig, axes = plt.subplots(1, 2, figsize=(24, 16))
    fig.patch.set_facecolor(BRANCO)
    fig.suptitle('DIAGRAMA DE CLASSES - E.C.P MANAGER', fontsize=20, fontweight='bold',
                 color=AZUL_ESCURO, y=0.98)

    def draw_class(ax, x, y, name, attrs, methods, color, w=4.5):
        attr_h = len(attrs) * 0.32
        meth_h = len(methods) * 0.32
        total_h = attr_h + meth_h + 0.8

        # Header
        rect_h = FancyBboxPatch((x, y), w, 0.5, boxstyle="round,pad=0.05",
                                 facecolor=color, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect_h)
        ax.text(x + w/2, y + 0.25, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color=BRANCO)

        # Attributes
        rect_a = FancyBboxPatch((x, y - attr_h - 0.1), w, attr_h + 0.1,
                                 facecolor='#F5F5F5', edgecolor=color, linewidth=1)
        ax.add_patch(rect_a)
        for i, attr in enumerate(attrs):
            ax.text(x + 0.15, y - 0.15 - i*0.32, attr, ha='left', va='center',
                    fontsize=7, color=AZUL_ESCURO, family='monospace')

        # Methods
        if methods:
            rect_m = FancyBboxPatch((x, y - attr_h - meth_h - 0.2), w, meth_h + 0.1,
                                     facecolor=BRANCO, edgecolor=color, linewidth=1)
            ax.add_patch(rect_m)
            for i, meth in enumerate(methods):
                ax.text(x + 0.15, y - attr_h - 0.25 - i*0.32, meth, ha='left', va='center',
                        fontsize=7, color=VERDE if '+' in meth else VERMELHO, family='monospace')

    # Backend
    ax = axes[0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')
    ax.set_title('Backend (Python/FastAPI)', fontsize=14, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_class(ax, 0.2, 15.5, 'Usuario', [
        '+ id: string', '+ nome: string', '+ email: string',
        '+ senha: string', '+ ativo: boolean', '+ criado_em: datetime'
    ], [], AZUL_ROYAL)

    draw_class(ax, 5.5, 15.5, 'Atleta', [
        '+ id: string', '+ nome: string', '+ posicao: string',
        '+ telefone: string', '+ foto: string?', '+ pe_dominante: string?',
        '+ ativo: boolean', '+ criado_em: datetime'
    ], [], VERDE)

    draw_class(ax, 0.2, 12.5, 'Treino', [
        '+ id: string', '+ data: string', '+ local: string',
        '+ observacoes: string?', '+ criado_em: datetime'
    ], [], '#E91E63')

    draw_class(ax, 5.5, 12.5, 'Presenca', [
        '+ id: string', '+ treino_id: string', '+ atleta_id: string',
        '+ presente: boolean', '+ criado_em: datetime'
    ], [], '#9C27B0')

    draw_class(ax, 0.2, 10, 'Partida', [
        '+ id: string', '+ data: string', '+ adversario: string',
        '+ local: string', '+ gols_clube: int', '+ gols_adversario: int',
        '+ resultado: string', '+ criado_em: datetime'
    ], [
        '+ calcular_resultado(): string'
    ], AMARELO)

    draw_class(ax, 5.5, 10, 'Patrocinador', [
        '+ id: string', '+ nome: string', '+ tipo: string',
        '+ contato: string', '+ ativo: boolean', '+ criado_em: datetime'
    ], [], '#FF5722')

    draw_class(ax, 0.2, 6.8, 'Recebimento', [
        '+ id: string', '+ descricao: string', '+ valor: float',
        '+ data: string', '+ patrocinador_id: string?', '+ criado_em: datetime'
    ], [], '#00BCD4')

    draw_class(ax, 5.5, 6.8, 'Despesa', [
        '+ id: string', '+ descricao: string', '+ categoria: string',
        '+ valor: float', '+ data: string', '+ criado_em: datetime'
    ], [], VERMELHO)

    draw_class(ax, 0.2, 4.2, 'ServicoAutenticacao', [
        '- JWT_SECRET: string', '- JWT_ALGORITHM: string'
    ], [
        '+ hash_senha(senha): string',
        '+ verificar_senha(texto, hash): bool',
        '+ criar_token(dados): string',
        '+ obter_usuario_atual(token): Usuario'
    ], AZUL_ESCURO, w=5)

    draw_class(ax, 5.7, 4.2, 'ServicoExportacao', [
        '- db: Database'
    ], [
        '+ exportar_excel(tipo): Response',
        '+ exportar_pdf(tipo): Response',
        '- gerar_excel(dados): BytesIO',
        '- gerar_pdf(dados): BytesIO'
    ], AZUL_ESCURO, w=5)

    draw_class(ax, 0.2, 1.5, 'DashboardStats', [
        '+ total_atletas_ativos: int', '+ total_treinos: int',
        '+ total_partidas: int', '+ total_receitas: float',
        '+ total_despesas: float', '+ saldo: float',
        '+ vitorias: int', '+ empates: int', '+ derrotas: int'
    ], [], '#673AB7')

    # Frontend
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')
    ax.set_title('Frontend (React)', fontsize=14, fontweight='bold', color=AZUL_ESCURO, pad=10)

    draw_class(ax, 0.2, 15.5, 'PaginaLogin', [
        '- formData: objeto', '- carregando: boolean'
    ], [
        '+ handleSubmit(): void',
        '+ handleLogin(): void',
        '+ handleRegistro(): void'
    ], AZUL_ROYAL)

    draw_class(ax, 5.5, 15.5, 'PaginaDashboard', [
        '- estatisticas: DashboardStats', '- graficos: objeto',
        '- mes: numero', '- ano: numero'
    ], [
        '+ carregarDados(): void',
        '+ handleFiltro(): void'
    ], VERDE)

    draw_class(ax, 0.2, 12.5, 'PaginaAtletas', [
        '- atletas: Atleta[]', '- filtrados: Atleta[]',
        '- termoBusca: string', '- formData: AtletaForm'
    ], [
        '+ carregarAtletas(): void',
        '+ handleSubmit(): void',
        '+ handleEditar(atleta): void',
        '+ handleExcluir(id): void',
        '+ handleImagem(arquivo): void'
    ], '#E91E63')

    draw_class(ax, 5.5, 12.5, 'PaginaTreinos', [
        '- treinos: Treino[]', '- presencas: Presenca[]',
        '- treinoSelecionado: Treino'
    ], [
        '+ carregarTreinos(): void',
        '+ abrirPresenca(treino): void',
        '+ salvarPresencas(): void'
    ], '#9C27B0')

    draw_class(ax, 0.2, 9.2, 'PaginaPartidas', [
        '- partidas: Partida[]', '- formData: PartidaForm'
    ], [
        '+ carregarPartidas(): void',
        '+ getBadgeResultado(r): JSX',
        '+ handleSubmit(): void'
    ], AMARELO)

    draw_class(ax, 5.5, 9.2, 'PaginaFinanceiro', [
        '- recebimentos: Recebimento[]', '- despesas: Despesa[]',
        '- patrocinadores: Patrocinador[]', '- abaAtiva: string'
    ], [
        '+ carregarDados(): void',
        '+ calcularTotais(): objeto'
    ], '#FF5722')

    draw_class(ax, 0.2, 6.3, 'PaginaRelatorios', [
        '- relatorios: objeto[]'
    ], [
        '+ handleExportar(tipo, formato): void'
    ], '#00BCD4')

    draw_class(ax, 5.5, 6.3, 'Layout', [
        '- menuMobileAberto: boolean', '- itensMenu: objeto[]'
    ], [
        '+ handleLogout(): void',
        '+ ConteudoSidebar(): JSX'
    ], AZUL_ESCURO)

    draw_class(ax, 0.2, 4, 'ServicoAPI', [
        '- baseURL: string', '- token: string'
    ], [
        '+ get(url): Promise',
        '+ post(url, dados): Promise',
        '+ put(url, dados): Promise',
        '+ delete(url): Promise',
        '+ interceptarRequisicao(): void',
        '+ interceptarResposta(): void'
    ], AZUL_ESCURO, w=5)

    draw_class(ax, 5.7, 4, 'Componentes Shadcn UI', [
        '• Card', '• Button', '• Dialog',
        '• Table', '• Input', '• Select',
        '• Badge', '• Tabs', '• Sheet'
    ], [], CINZA, w=5)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/app/docs/imagens/05-diagrama-classes.png', dpi=150, bbox_inches='tight',
                facecolor=BRANCO, edgecolor='none')
    plt.close()
    print('✓ 5/5 - Diagrama de Classes gerado')

# Gerar todos os diagramas
print('Gerando diagramas PNG...\n')
gerar_casos_uso()
gerar_arquitetura()
gerar_banco_dados()
gerar_fluxograma()
gerar_classes()
print('\n✅ Todos os 5 diagramas PNG gerados em /app/docs/imagens/')
