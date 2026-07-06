# ==============================================================================
# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE NATIVAS (DOMÍNIO: GESTÃO BOVINA)
# ==============================================================================

# SELEÇÃO DE CHAVE + MODELO 

GEMINI_API_KEY = "Sua_Chave" # Substitua "SUA_CHAVE_AQUI" pela sua chave real do Google Gemini 
GEMINI_MODEL = "gemini-3.1-flash-lite"

# ==============================================================================
# PROMPTS OPERACIONAIS - RELATÓRIOS ESTRUTURADOS DO TRABALHO
# ==============================================================================
PROMPT_CONSULTA_1 = (
    "Gere uma consulta para obter o total de animais distintos atendidos clinicamente "
    "por cada médico veterinário cadastrado no sistema, exibindo o nome do profissional "
    "e o volume total de atendimentos (COUNT). Ordene pelo total de forma decrescente."
)

PROMPT_CONSULTA_2 = (
    "Calcule a média de peso exata e atual do rebanho em idade adulta (bovinos com mais de 18 meses "
    "com base na data atual), utilizando apenas a última pesagem registrada de cada animal "
    "(DISTINCT ON id_bovino ordenado por data decrescente). Agrupe os resultados por raça (linhagem) e sexo do animal."
)

PROMPT_CONSULTA_3 = (
    "Gere uma consulta SQL para PostgreSQL para obter o histórico cronológico de movimentação dos piquetes no último trimestre. "
    "Regras para o SQL: "
    "1) Use uma CTE com UNION ALL para consolidar entradas (+1) e saídas (-1) EXCLUSIVAMENTE usando a tabela 'piquete_bovino'. "
    "2) Faça o JOIN com a tabela 'piquete' para pegar o nome. "
    "3) Calcule a lotação acumulada usando a função analítica SUM() OVER (PARTITION BY piquete.nome ORDER BY data). "
    "4) Retorne os dados puros, sem funções de formatação (como LPAD). "
    "Regras para a Apresentação Final: Transforme os dados em uma tabela de dupla entrada (Pivot Table) em texto simples (sem Markdown). "
    "Linhas = Nomes dos Piquetes; Colunas = Datas (DD/MM). "
    "REGRA CRÍTICA PARA A TABELA: O centro da tabela deve exibir EXCLUSIVAMENTE o Saldo Diário (a variação exata daquele dia, ex: +3, -1) "
    "e NÃO a lotação acumulada. Se não houver movimento no dia, use um traço '-'. "
)