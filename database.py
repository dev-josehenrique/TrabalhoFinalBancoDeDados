import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            user="postgres",       
            password="sua_senha",
            host="localhost",
            port="5432",
            database="BD_TrabalhoFinal" 
        )
        return conexao
    
    except psycopg2.OperationalError:
        print("\n[ERRO] O banco de dados está offline ou não foi encontrado.")
        return None
        
    except UnicodeDecodeError:
        # Captura o erro do 'ç' no Windows que o Postgres joga quando erramos a senha/usuário
        print("\n[ERRO DE AUTENTICAÇÃO] Usuário ou senha incorretos, ou o banco não existe.")
        return None
        
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        return None

def fechar_conexao(conexao):
    if conexao:
        try:
            conexao.close()
        except Exception:
            pass # Fecha silenciosamente sem incomodar o usuário