import csv
from dados import inserts_bovinos
import psycopg2

class Cor:
    CABECALHO = '\033[96m'
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    NEGRITO = '\033[1m'
    FIM = '\033[0m'

# ==========================================
# FUNÇÕES DE SETUP (MANTIDAS INTACTAS)
# ==========================================
def criar_tabelas(conexao, caminho_ddl):
    cursor = conexao.cursor()
    try:
        with open(caminho_ddl, 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        conexao.commit()
        print(f"{Cor.VERDE}Tabelas criadas com sucesso!{Cor.FIM}")
    except Exception as e:
        conexao.rollback()
        print(f"{Cor.VERMELHO}Erro ao criar tabelas: {e}{Cor.FIM}")
    finally:
        cursor.close()

def eliminar_tabelas(conexao):
    cursor = conexao.cursor()
    try:
        cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conexao.commit()
        print(f"{Cor.AMARELO}Banco limpo. Todas as tabelas foram apagadas.{Cor.FIM}")
    except Exception as e:
        conexao.rollback()
        print(f"{Cor.VERMELHO}Erro ao limpar banco: {e}{Cor.FIM}")
    finally:
        cursor.close()

def popular_banco(conexao):
    cursor = conexao.cursor()
    print(f"\n{Cor.CABECALHO}--- INSERINDO DADOS NO BANCO ---{Cor.FIM}")
    try:
        for nome_tabela, query in inserts_bovinos.items():
            print(f"Povoando tabela {nome_tabela}... ", end='')
            cursor.execute(query)
            print(f"{Cor.VERDE}OK{Cor.FIM}")
            
        conexao.commit()
        print(f"{Cor.VERDE}Carga de dados completa com sucesso!{Cor.FIM}")
    except Exception as e:
        conexao.rollback()
        print(f"\n{Cor.VERMELHO}Erro ao inserir na tabela {nome_tabela}: {e}{Cor.FIM}")
    finally:
        cursor.close()


# ==========================================
# NOVAS FUNÇÕES CRUD INTERATIVAS COMPLETAS
# ==========================================
# O 'pk' em branco indica tabelas associativas/compostas onde o usuário precisa digitar todas as FKs.
CONFIG_TABELAS = {
    '1': {'nome': 'propriedade', 'pk': 'id_propriedade'},
    '2': {'nome': 'raca', 'pk': 'id_raca'},
    '3': {'nome': 'medicamento', 'pk': 'id_medicamento'},
    '4': {'nome': 'doenca', 'pk': 'id_doenca'},
    '5': {'nome': 'tipo_tratamento', 'pk': 'id_tipo_tratamento'},
    '6': {'nome': 'vacina', 'pk': 'id_vacina'},
    '7': {'nome': 'veterinario', 'pk': 'id_veterinario'},
    '8': {'nome': 'piquete', 'pk': 'id_piquete'},
    '9': {'nome': 'bovino', 'pk': 'id_bovino'},
    '10': {'nome': 'pesagem', 'pk': 'id_pesagem'},
    '11': {'nome': 'tratamento', 'pk': 'id_tratamento'},
    '12': {'nome': 'receita', 'pk': ''},
    '13': {'nome': 'piquete_bovino', 'pk': ''},
    '14': {'nome': 'vacina_bovino', 'pk': ''},
    '15': {'nome': 'historico', 'pk': ''}
}

def menu_tabelas():
    print(f"\n{Cor.CABECALHO}--- SELECIONE A TABELA ALVO ---{Cor.FIM}")
    
    print(f"\n{Cor.AMARELO}[ Tabelas de Cadastros Básicos ]{Cor.FIM}")
    for k in range(1, 9):
        val = CONFIG_TABELAS[str(k)]
        print(f"  {k}. {val['nome'].capitalize()}")
        
    print(f"\n{Cor.AMARELO}[ Tabelas Operacionais e Movimentação ]{Cor.FIM}")
    for k in range(9, 16):
        val = CONFIG_TABELAS[str(k)]
        print(f" {k}. {val['nome'].capitalize()}")
        
    op = input(f"\n{Cor.NEGRITO}Opção: {Cor.FIM}")
    return CONFIG_TABELAS.get(op)

def inserir_registro_generico(conexao):
    print(f"\n{Cor.NEGRITO}{Cor.CABECALHO}--- INSERIR REGISTRO ---{Cor.FIM}")
    tab_info = menu_tabelas()
    if not tab_info:
        print(f"{Cor.VERMELHO}Tabela inválida.{Cor.FIM}")
        return
        
    tabela, pk = tab_info['nome'], tab_info['pk']
    cursor = conexao.cursor()
    
    try:
        cursor.execute(f"SELECT * FROM {tabela} LIMIT 0")
        colunas = [desc[0] for desc in cursor.description]
        
        # Remove a PK apenas se ela for um serial auto-incremento
        if pk and pk in colunas: 
            colunas.remove(pk)
            
        valores = {}
        print(f"\n{Cor.AMARELO}Preencha os dados (Deixe em branco para pular/Nulo):{Cor.FIM}")
        for col in colunas:
            val = input(f"  {col}: ")
            valores[col] = val if val.strip() != "" else None
            
        print(f"\n{Cor.CABECALHO}Resumo da Nova Tupla ({tabela}):{Cor.FIM}")
        for col, val in valores.items():
            print(f"  {col}: {Cor.VERDE}{val}{Cor.FIM}")
            
        confirma = input(f"\n{Cor.VERMELHO}Confirmar inserção? (S/N): {Cor.FIM}")
        if confirma.upper() == 'S':
            cols_str = ", ".join(valores.keys())
            placeholders = ", ".join(["%s"] * len(valores))
            cursor.execute(f"INSERT INTO {tabela} ({cols_str}) VALUES ({placeholders})", tuple(valores.values()))
            conexao.commit()
            print(f"{Cor.VERDE}Registro inserido com sucesso!{Cor.FIM}")
        else:
            print(f"{Cor.AMARELO}Operação cancelada pelo usuário.{Cor.FIM}")
    except Exception as e:
        conexao.rollback()
        print(f"{Cor.VERMELHO}Erro SQL: {e}{Cor.FIM}")
    finally:
        cursor.close()

def atualizar_registro_generico(conexao):
    print(f"\n{Cor.NEGRITO}{Cor.CABECALHO}--- ATUALIZAR REGISTRO ---{Cor.FIM}")
    tab_info = menu_tabelas()
    if not tab_info:
        print(f"{Cor.VERMELHO}Tabela inválida.{Cor.FIM}")
        return
        
    tabela, pk = tab_info['nome'], tab_info['pk']
    cursor = conexao.cursor()
    
    try:
        # Busca o registro
        if pk:
            id_valor = input(f"\nInforme o '{pk}' do registro a ser editado: ")
            cursor.execute(f"SELECT * FROM {tabela} WHERE {pk} = %s", (id_valor,))
            registro = cursor.fetchone()
            condicao_where = f"{pk} = %s"
            valores_where = (id_valor,)
        else:
            print(f"\n{Cor.AMARELO}Tabela associativa. Informe os dados para localizar o registro:{Cor.FIM}")
            cursor.execute(f"SELECT * FROM {tabela} LIMIT 0")
            colunas = [desc[0] for desc in cursor.description]
            clausulas = []
            valores_where = []
            for col in colunas:
                val = input(f"  {col} (filtro): ")
                if val.strip() != "":
                    clausulas.append(f"{col} = %s")
                    valores_where.append(val)
            
            if not clausulas:
                print(f"{Cor.VERMELHO}Nenhum filtro informado.{Cor.FIM}")
                return
            
            where_sql = " AND ".join(clausulas)
            cursor.execute(f"SELECT * FROM {tabela} WHERE {where_sql}", tuple(valores_where))
            registro = cursor.fetchone()
            condicao_where = where_sql
            
        if not registro:
            print(f"{Cor.VERMELHO}Registro não encontrado.{Cor.FIM}")
            return
            
        colunas = [desc[0] for desc in cursor.description]
        print(f"\n{Cor.CABECALHO}Tupla Atual:{Cor.FIM} (ENTER para manter o valor atual)")
        
        novos_valores = {}
        for col, val in zip(colunas, registro):
            entrada = input(f"  {col} [{val}]: ")
            novos_valores[col] = entrada if entrada.strip() != "" else val
        
        # --- BLOCO DE CONFIRMAÇÃO ADICIONADO ---
        print(f"\n{Cor.CABECALHO}Resumo da Atualização ({tabela}):{Cor.FIM}")
        for col, val in novos_valores.items():
            print(f"  {col}: {Cor.AMARELO}{val}{Cor.FIM}")
            
        confirma = input(f"\n{Cor.VERMELHO}Salvar alterações no banco? (S/N): {Cor.FIM}")
        if confirma.upper() == 'S':
            set_clause = ", ".join([f"{col} = %s" for col in novos_valores.keys()])
            params = list(novos_valores.values()) + list(valores_where)
            
            cursor.execute(f"UPDATE {tabela} SET {set_clause} WHERE {condicao_where}", tuple(params))
            conexao.commit()
            print(f"{Cor.VERDE}Registro atualizado com sucesso!{Cor.FIM}")
        else:
            print(f"{Cor.AMARELO}Atualização cancelada pelo usuário.{Cor.FIM}")
        # ----------------------------------------
        
    except Exception as e:
        conexao.rollback()
        print(f"{Cor.VERMELHO}Erro SQL: {e}{Cor.FIM}")
    finally:
        cursor.close()

def deletar_registro_generico(conexao):
    print(f"\n{Cor.NEGRITO}{Cor.CABECALHO}--- DELETAR REGISTRO ---{Cor.FIM}")
    tab_info = menu_tabelas()
    if not tab_info:
        print(f"{Cor.VERMELHO}Tabela inválida.{Cor.FIM}")
        return
        
    tabela, pk = tab_info['nome'], tab_info['pk']
    cursor = conexao.cursor()
    
    try:
        if pk:
            # LÓGICA PARA TABELAS NORMAIS (CHAVE SIMPLES)
            id_valor = input(f"\nInforme o '{pk}' do registro a ser deletado: ")
            cursor.execute(f"SELECT * FROM {tabela} WHERE {pk} = %s", (id_valor,))
            registro = cursor.fetchone()
            
            if not registro:
                print(f"{Cor.VERMELHO}Registro não encontrado no banco.{Cor.FIM}")
                return
                
            colunas = [desc[0] for desc in cursor.description]
            print(f"\n{Cor.CABECALHO}Tupla Encontrada ({tabela}):{Cor.FIM}")
            for col, val in zip(colunas, registro):
                print(f"  {col}: {Cor.AMARELO}{val}{Cor.FIM}")
                
            confirma = input(f"\n{Cor.VERMELHO}Atenção: A deleção é irreversível! Deletar registro? (S/N): {Cor.FIM}")
            if confirma.upper() == 'S':
                cursor.execute(f"DELETE FROM {tabela} WHERE {pk} = %s", (id_valor,))
                conexao.commit()
                print(f"{Cor.VERDE}Registro deletado com sucesso!{Cor.FIM}")
            else:
                print(f"{Cor.AMARELO}Deleção cancelada pelo usuário.{Cor.FIM}")
                
        else:
            # LÓGICA PARA TABELAS ASSOCIATIVAS (CHAVES COMPOSTAS)
            print(f"\n{Cor.AMARELO}Tabela associativa detectada. Informe os dados para localizar o registro exato:{Cor.FIM}")
            print("(Deixe o campo em branco se não quiser usá-lo como filtro de busca)")
            
            cursor.execute(f"SELECT * FROM {tabela} LIMIT 0")
            colunas = [desc[0] for desc in cursor.description]
            
            clausulas_where = []
            valores_where = []
            
            for col in colunas:
                val = input(f"  {col}: ")
                if val.strip() != "":
                    clausulas_where.append(f"{col} = %s")
                    valores_where.append(val)
            
            if not clausulas_where:
                print(f"{Cor.VERMELHO}Nenhum dado informado. Operação cancelada para evitar deleção em massa.{Cor.FIM}")
                return
                
            where_sql = " AND ".join(clausulas_where)
            
            cursor.execute(f"SELECT * FROM {tabela} WHERE {where_sql}", tuple(valores_where))
            registros = cursor.fetchall()
            
            if not registros:
                print(f"{Cor.VERMELHO}Nenhum registro encontrado correspondente a esses dados.{Cor.FIM}")
                return
            
            print(f"\n{Cor.CABECALHO}Registros Encontrados ({len(registros)}):{Cor.FIM}")
            for i, reg in enumerate(registros, 1):
                print(f"  [{i}] {reg}")
                
            confirma = input(f"\n{Cor.VERMELHO}Deletar TODOS os registros listados acima? (S/N): {Cor.FIM}")
            if confirma.upper() == 'S':
                cursor.execute(f"DELETE FROM {tabela} WHERE {where_sql}", tuple(valores_where))
                conexao.commit()
                print(f"{Cor.VERDE}Deleção concluída com sucesso!{Cor.FIM}")
            else:
                print(f"{Cor.AMARELO}Deleção cancelada pelo usuário.{Cor.FIM}")
                
    except Exception as e:
        conexao.rollback()
        print(f"{Cor.VERMELHO}Erro SQL: {e}{Cor.FIM}")
    finally:
        cursor.close()