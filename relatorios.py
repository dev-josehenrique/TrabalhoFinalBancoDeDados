import pandas as pd
import matplotlib.pyplot as plt
import warnings
from datetime import datetime

# Silencia TODOS os avisos para deixar o terminal limpo
warnings.filterwarnings('ignore')

# Classe para colorir o terminal (Códigos ANSI)
class Cor:
    CABECALHO = '\033[96m' # Ciano
    VERDE = '\033[92m'     # Sucesso / Entradas
    VERMELHO = '\033[91m'  # Alertas / Saídas
    AMARELO = '\033[93m'   # Destaques
    NEGRITO = '\033[1m'
    FIM = '\033[0m'        # Reseta a cor

def consulta_1_veterinario(conexao):
    print(f"\n{Cor.NEGRITO}=== RELATÓRIO 1: Animais Tratados por Veterinário ==={Cor.FIM}")
    print("Descrição: Obter o total de animais distintos que foram atendidos por cada médico veterinário cadastrado no sistema.")
    
    query = """
        SELECT 
            v.nome AS veterinario, 
            COUNT(t.id_bovino) AS total_animais_tratados
        FROM veterinario v
        LEFT JOIN tratamento t ON v.id_veterinario = t.id_veterinario
        LEFT JOIN bovino b ON t.id_bovino = b.id_bovino
        GROUP BY v.nome
        ORDER BY total_animais_tratados DESC;
    """
    df = pd.read_sql_query(query, conexao)
    
    print("\nResultado da Consulta:")
    print(f"{Cor.CABECALHO}{Cor.NEGRITO}{'MÉDICO VETERINÁRIO':<25} | {'TOTAL DE ANIMAIS TRATADOS'}{Cor.FIM}")
    print("-" * 55)
    for _, row in df.iterrows():
        print(f"{row['veterinario']:<25} | {Cor.VERDE}{row['total_animais_tratados']:>25}{Cor.FIM}")
    
    ax = df.plot(kind='bar', x='veterinario', y='total_animais_tratados', 
                 legend=False, color=['#4C72B0', '#55A868'], width=0.3, figsize=(8, 5))
    
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=11)
        
    plt.title('Total de Animais Tratados por Veterinário')
    plt.xlabel('Médico Veterinário')
    plt.ylabel('Quantidade de Animais')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks(range(0, int(df['total_animais_tratados'].max()) + 2))
    plt.tight_layout()
    plt.show()

def consulta_2_peso_adultos(conexao):
    print(f"\n{Cor.NEGRITO}=== RELATÓRIO 2: Média do Peso Atual de Adultos por Raça e Sexo ==={Cor.FIM}")
    print("Descrição: Calcular a média de peso (baseada na última pesagem registrada) exclusivamente dos bovinos em idade adulta (idade superior a 18 meses na data de hoje).")
    
    # O INTERVAL '18 months' calcula dinamicamente a idade do bovino no PostgreSQL
    query = """
        WITH UltimaPesagem AS (
            SELECT DISTINCT ON (id_bovino) id_bovino, peso, data
            FROM pesagem
            ORDER BY id_bovino, data DESC
        )
        SELECT 
            r.linhagem AS raca,
            b.sexo,
            ROUND(AVG(up.peso), 2) AS media_peso
        FROM raca r
        JOIN bovino b ON r.id_raca = b.id_raca
        JOIN UltimaPesagem up ON b.id_bovino = up.id_bovino
        WHERE b.data_nascimento <= CURRENT_DATE - INTERVAL '18 months'
        GROUP BY r.linhagem, b.sexo
        ORDER BY r.linhagem, b.sexo;
    """
    df = pd.read_sql_query(query, conexao)
    
    df_pivot = df.pivot(index='raca', columns='sexo', values='media_peso').fillna(0)
    
    print("\nResultado da Consulta:")
    print(f"{Cor.CABECALHO}{Cor.NEGRITO}{'RAÇA (LINHAGEM)':<20} | {'SEXO':<15} | {'PESO MÉDIO ATUAL'}{Cor.FIM}")
    print("-" * 55)
    for raca in df_pivot.index:
        for sexo in df_pivot.columns:
            peso = df_pivot.loc[raca, sexo]
            print(f"{raca:<20} | {sexo:<15} | {Cor.AMARELO}{peso:>7.2f} kg{Cor.FIM}")
    
    ax = df_pivot.plot(kind='bar', figsize=(10, 6), color=['#C44E52', '#4C72B0'], width=0.5)
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f kg', padding=3, fontsize=10)
        
    plt.title('Média do Peso Atual de Animais Adultos (> 18 meses) por Raça e Sexo')
    plt.xlabel('Raça (Linhagem)')
    plt.ylabel('Peso Médio (kg)')
    plt.xticks(rotation=0)
    plt.legend(title='Sexo', loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    max_y = df_pivot.max().max()
    plt.ylim(0, max_y * 1.15)
    
    plt.tight_layout()
    plt.show()

def consulta_3_historico_piquete(conexao):
    hoje_dt = pd.Timestamp.now().normalize()
    data_corte_dt = hoje_dt - pd.DateOffset(months=3)
    data_corte_str = data_corte_dt.strftime('%Y-%m-%d')
    
    print(f"\n{Cor.NEGRITO}=== RELATÓRIO 3: Movimentação Diária de Piquetes ==={Cor.FIM}")
    print(f"Descrição: Histórico de lotação e movimentação de animais no último trimestre (Cruzando 3 tabelas).")
    
    query = """
        WITH Movimentacoes AS (
            SELECT id_piquete, data_entrada AS data_mov, 1 AS qtd FROM piquete_bovino WHERE data_entrada IS NOT NULL
            UNION ALL
            SELECT id_piquete, data_saida AS data_mov, -1 AS qtd FROM piquete_bovino WHERE data_saida IS NOT NULL
        ),
        SaldosDiarios AS (
            SELECT 
                pr.nome AS propriedade,
                p.nome AS piquete,
                pr.nome || ' - ' || p.nome AS piquete_completo,
                m.data_mov,
                SUM(CASE WHEN m.qtd = 1 THEN 1 ELSE 0 END) AS entradas,
                SUM(CASE WHEN m.qtd = -1 THEN 1 ELSE 0 END) AS saidas,
                SUM(m.qtd) AS saldo_dia
            FROM Movimentacoes m
            JOIN piquete p ON m.id_piquete = p.id_piquete
            JOIN propriedade pr ON p.id_propriedade = pr.id_propriedade
            GROUP BY pr.nome, p.nome, m.data_mov
        ),
        Acumulado AS (
            SELECT propriedade, piquete, piquete_completo, data_mov, entradas, saidas, saldo_dia,
                SUM(saldo_dia) OVER (PARTITION BY piquete_completo ORDER BY data_mov) AS lotacao_final
            FROM SaldosDiarios
        )
        SELECT * FROM Acumulado ORDER BY data_mov, propriedade, piquete;
    """
    df = pd.read_sql_query(query, conexao)
    
    if df.empty:
        print("\nResultado da Consulta: Nenhum dado encontrado.")
        return

    df['data_mov'] = pd.to_datetime(df['data_mov'])
    df_print = df[df['data_mov'] >= data_corte_dt].copy()
    
    print(f"\nResultado da Consulta (Saldo Diário a partir de {data_corte_str}):")
    
    pivot_term = df_print.pivot(index=['propriedade', 'piquete'], columns='data_mov', values='saldo_dia')
    datas_cols = sorted(pivot_term.columns)
    
    cabecalho = f"{Cor.CABECALHO}{Cor.NEGRITO}{'PROPRIEDADE':<20} | {'PIQUETE':<25} | "
    for d in datas_cols:
        cabecalho += f"{d.strftime('%d/%m'):^5} | "
    cabecalho += Cor.FIM
    
    print(cabecalho)
    print("-" * (51 + len(datas_cols) * 8)) 
    
    for prop, piq in pivot_term.index:
        linha = f"{str(prop):<20} | {str(piq):<25} | "
        for d in datas_cols:
            val = pivot_term.loc[(prop, piq), d]
            if pd.isna(val) or val == 0:
                linha += f"{'-':^5} | "
            elif val > 0:
                texto_val = f"+{int(val)}"
                linha += f"{Cor.VERDE}{texto_val:^5}{Cor.FIM} | "
            else:
                texto_val = f"{int(val)}"
                linha += f"{Cor.VERMELHO}{texto_val:^5}{Cor.FIM} | "
        print(linha)

    df_pivot = df.pivot(index='data_mov', columns='piquete_completo', values='lotacao_final')
    
    if data_corte_dt not in df_pivot.index:
        df_pivot.loc[data_corte_dt] = [pd.NA] * len(df_pivot.columns)
    if hoje_dt not in df_pivot.index:
        df_pivot.loc[hoje_dt] = [pd.NA] * len(df_pivot.columns)
        
    df_pivot = df_pivot.sort_index().ffill().fillna(0)
    df_pivot = df_pivot[df_pivot.index >= data_corte_dt]
    
    # 1. Aplicando o formato Padrão Brasil (DD/MM/AAAA)
    df_pivot.index = df_pivot.index.strftime('%d/%m/%Y')
    
    ax = df_pivot.plot(kind='line', marker='o', figsize=(13, 6), linewidth=2.5, markersize=8)
    
    for line in ax.lines:
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            if pd.notna(y):
                ax.annotate(f'{int(y)}', xy=(x, y), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=10)

    plt.title('Movimentação Diária e Lotação de Animais do Último Trimestre')
    plt.xlabel('Data da Movimentação')
    plt.ylabel('Quantidade Total de Animais no Piquete')
    
    max_y = df_pivot.max().max()
    plt.ylim(-0.5, max_y + 2) 
    plt.yticks(range(0, int(max_y) + 3, 2))
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.legend(title='Piquetes', bbox_to_anchor=(1.02, 1), loc='upper left')
    
    # 2. Forçando a renderização de TODAS as datas, inclinadas e bem alinhadas
    plt.xticks(ticks=range(len(df_pivot.index)), labels=df_pivot.index, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()