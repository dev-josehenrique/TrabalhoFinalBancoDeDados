import os
import re
import pandas as pd
from google import genai
from google.genai import types

# Importação nativa do arquivo de variáveis de ambiente do projeto
try:
    import env
except ImportError:
    print("\n[ERRO CRÍTICO] O arquivo 'env.py' não foi localizado no diretório atual.")

class Cor:
    CABECALHO = '\033[96m'
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    NEGRITO = '\033[1m'
    FIM = '\033[0m'

def obter_client_ia():
    """Inicializa o cliente do Google GenAI utilizando a chave isolada no arquivo env.py."""
    api_key = getattr(env, "GEMINI_API_KEY", None)
    
    # Fallback para variáveis do sistema operacional caso a string padrão não seja alterada
    if not api_key or "SUA_CHAVE_AQUI" in api_key or api_key == "":
        api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        print(f"\n{Cor.VERMELHO}[AVISO DA IA] Chave da API do Gemini não configurada.{Cor.FIM}")
        print(f"Por favor, preencha a variável {Cor.NEGRITO}GEMINI_API_KEY{Cor.FIM} dentro do seu arquivo {Cor.AMARELO}env.py{Cor.FIM}.")
        return None
        
    return genai.Client(api_key=api_key)

def obter_esquema_banco_dinamico(conexao):
    """
    Inspeciona o catálogo oficial do PostgreSQL (information_schema) em tempo real.
    A IA descobre as tabelas, colunas e tipos diretamente do banco ativo, sem dados estáticos.
    """
    try:
        cursor = conexao.cursor()
        # Query que varre o dicionário de dados do PostgreSQL buscando tabelas criadas pelo usuário
        query = """
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """
        cursor.execute(query)
        linhas = cursor.fetchall()
        cursor.close()
        
        if not linhas:
            return "Aviso: O banco de dados conectado está vazio ou sem tabelas no esquema público."
            
        esquema = "Estrutura do Banco de Dados Detectada Dinamicamente no PostgreSQL:\n"
        tabela_atual = ""
        
        for tabela, coluna, tipo in linhas:
            if tabela != tabela_atual:
                if tabela_atual != "":
                    esquema += ")\n"
                tabela_atual = tabela
                esquema += f"- {tabela} ({coluna} {tipo.upper()}"
            else:
                esquema += f", {coluna} {tipo.upper()}"
                
        if tabela_atual != "":
            esquema += ")"
            
        return esquema
        
    except Exception as e:
        print(f"\n{Cor.VERMELHO}[ERRO] Falha crítica ao interrogar o catálogo do PostgreSQL: {e}{Cor.FIM}")
        return ""

def extrair_codigo_sql(texto_ia):
    """Remove marcações de markdown (```sql ... ```) da resposta gerada pela LLM."""
    padrao = r"```sql(.*?)```"
    match = re.search(padrao, texto_ia, re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto_ia.replace("```", "").strip()

def analise_llm(conexao):
    """Módulo Text-to-SQL acoplado às variáveis ambientais do env.py e ao catálogo dinâmico."""
    client = obter_client_ia()
    if not client:
        return

    # Busca a estrutura em tempo de execução diretamente do banco
    esquema_vivo = obter_esquema_banco_dinamico(conexao)
    modelo_selecionado = getattr(env, "GEMINI_MODEL")

    print("\n")
    print(f"{Cor.VERDE}LLM selecionada: {Cor.NEGRITO}{modelo_selecionado}{Cor.FIM}")
    
    while True:
        print(f"\n{Cor.AMARELO}[ INTERFACE OPERACIONAL DO MÓDULO LLM ]{Cor.FIM}")
        print("  1. Executar Consulta 1 (Carga de Atendimentos por Veterinário)")
        print("  2. Executar Consulta 2 (Média de Peso de Animais Adultos por Linhagem/Sexo)")
        print("  3. Executar Consulta 3 (Histórico de Lotação e Fluxo de Piquetes)")
        print("  4. Pergunta Livre (Interface Direta em Linguagem Natural)")
        print(f"{Cor.VERMELHO}  0. Voltar ao Menu Anterior{Cor.FIM}")
        print("-" * 75)
        
        opcao = input(f"{Cor.NEGRITO}Escolha uma opção: {Cor.FIM}")
        
        pergunta = ""
        if opcao == '1':
            pergunta = getattr(env, "PROMPT_CONSULTA_1", "")
        elif opcao == '2':
            pergunta = getattr(env, "PROMPT_CONSULTA_2", "")
        elif opcao == '3':
            pergunta = getattr(env, "PROMPT_CONSULTA_3", "")
        elif opcao == '4':
            pergunta = input(f"\n{Cor.NEGRITO}Digite o que você deseja consultar: {Cor.FIM}")
        elif opcao == '0':
            print(f"{Cor.AMARELO}Retornando ao painel principal...{Cor.FIM}")
            break
        else:
            print(f"{Cor.VERMELHO}Opção inválida.{Cor.FIM}")
            continue
            
        if not pergunta or pergunta.strip() == "":
            print(f"{Cor.VERMELHO}Falha ao extrair o escopo do prompt ou entrada vazia.{Cor.FIM}")
            continue

        instrucoes_sql = (
            "Você é um Engenheiro de Dados especialista em PostgreSQL. "
            f"Considere a estrutura de tabelas obtida dinamicamente do banco de dados:\n{esquema_vivo}\n"
            "Gere uma instrução SQL válida compatível com PostgreSQL que atenda ao pedido do usuário.\n\n"
            "Regras cruciais de desenvolvimento:\n"
            "1. Devolva APENAS a query SQL pura na resposta, sem blocos markdown (```), sem comentários e sem texto explicativo periférico.\n"
            "2. Ao realizar filtros de texto (cláusulas WHERE com strings/VARCHAR), utilize o operador ILIKE em vez de '=' ou aplique a função LOWER() "
            "para garantir que a busca funcione de forma insensível a maiúsculas e minúsculas (case-insensitive), evitando filtros vazios por incompatibilidade de caixa."
        )
        try:
            print(f"\n{Cor.AMARELO}1. IA lendo o prompt e gerando a query via {modelo_selecionado}...{Cor.FIM}")
            
            resposta_sql = client.models.generate_content(
                model=modelo_selecionado,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction=instrucoes_sql,
                    temperature=0.1
                )
            )
            
            sql_gerado = extrair_codigo_sql(resposta_sql.text)
            
            print(f"\n{Cor.CABECALHO}{Cor.NEGRITO}==== [ QUERY SQL DINÂMICA GERADA PELA IA ] ===={Cor.FIM}")
            print(f"{Cor.AMARELO}{sql_gerado}{Cor.FIM}")
            print(f"{Cor.CABECALHO}{Cor.NEGRITO}================================================{Cor.FIM}\n")

            print(f"{Cor.AMARELO}2. Submetendo comando ao servidor PostgreSQL...{Cor.FIM}")
            df_resultado = pd.read_sql_query(sql_gerado, conexao)
            
            if df_resultado.empty:
                print(f"{Cor.VERMELHO}A query executou corretamente, mas a tabela lógica retornou vazia.{Cor.FIM}")
                continue

            print(f"{Cor.AMARELO}3. Analisando registros tabulares para emissão de parecer...{Cor.FIM}\n")
            dados_string = df_resultado.to_string(index=False)
            
            instrucoes_analise = (
                "Você é um assistente técnico de banco de dados zootécnicos. "
                "Seu papel é olhar para o resultado da consulta SQL fornecida e responder à "
                "pergunta original do usuário de forma extremamente direta, curta e objetiva. "
                "Não gere relatórios longos, não traga recomendações de mercado e não dê sugestões estratégicas. "
                "Apenas exiba uma resposta clara e curta em formato textual ou markdown respondendo o que foi pedido."
            )
            
            prompt_analise = (
                f"Objetivo Analítico: {pergunta}\n\n"
                f"Dados Coletados no Banco:\n{dados_string}"
            )
            
            resposta_analise = client.models.generate_content(
                model=modelo_selecionado,
                contents=prompt_analise,
                config=types.GenerateContentConfig(
                    system_instruction=instrucoes_analise,
                    temperature=0.3
                )
            )
            
            print(f"{Cor.VERDE}{Cor.NEGRITO}=== RESULTADO PÓS ANÁLISE ==={Cor.FIM}")
            print(resposta_analise.text)
            print(f"{Cor.VERDE}{Cor.NEGRITO}" + "="*45 + f"{Cor.FIM}\n")
            
            input(f"{Cor.CABECALHO}Pressione ENTER para continuar...{Cor.FIM}")

        except Exception as e:
            print(f"{Cor.VERMELHO}Erro na interpretação ou execução da query SQL gerada: {e}{Cor.FIM}")