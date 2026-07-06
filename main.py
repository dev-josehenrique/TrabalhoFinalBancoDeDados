from database import conectar, fechar_conexao
from crud import criar_tabelas, eliminar_tabelas, popular_banco
from crud import inserir_registro_generico, atualizar_registro_generico, deletar_registro_generico
from relatorios import consulta_1_veterinario, consulta_2_peso_adultos, consulta_3_historico_piquete
from llm import analise_llm

class Cor:
    CABECALHO = '\033[96m'
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    NEGRITO = '\033[1m'
    FIM = '\033[0m'

def menu():
    con = conectar()
    if not con:
        return

    while True:
        print(f"\n{Cor.CABECALHO}{Cor.NEGRITO}" + "="*50)
        print(f"🌾 SISTEMA DE GESTÃO DE DADOS E SAÚDE BOVINA 🌾".center(50))
        print("="*50 + f"{Cor.FIM}")
        
        print(f"\n{Cor.AMARELO}[ SETUP DE BANCO DE DADOS ]{Cor.FIM}")
        print("  1. Setup: Criar tabelas do zero")
        print("  2. Setup: Excluir todas as tabelas")
        print("  3. Setup: Carregar CSV/Inserts iniciais")
        
        print(f"\n{Cor.VERDE}[ OPERAÇÕES INTERATIVAS (CRUD) ]{Cor.FIM}")
        print("  4. Inserir Registro")
        print("  5. Atualizar Registro")
        print("  6. Deletar Registro")
        
        print(f"\n{Cor.CABECALHO}[ RELATÓRIOS GERENCIAIS ]{Cor.FIM}")
        print("  7. Relatório 1: Carga de Atendimentos por Veterinário")
        print("  8. Relatório 2: Média Atual de Peso (Raça x Sexo)")
        print("  9. Relatório 3: Histórico de Lotação de Piquetes")
        
        print(f"\n{Cor.AMARELO}[ INTEGRAÇÃO DE LLM ]{Cor.FIM}")
        print("  10. IA: Módulo de Inteligência Artificial Generativa")
        
        print(f"\n{Cor.VERMELHO}  0. Sair do Sistema{Cor.FIM}")
        print("-" * 50)
        
        opcao = input(f"{Cor.NEGRITO}Escolha uma opção: {Cor.FIM}")

        if opcao == '1':
            print(f"\n{Cor.AMARELO}Executando: Criação de Tabelas...{Cor.FIM}")
            criar_tabelas(con, 'ddl.sql')
        elif opcao == '2':
            print(f"\n{Cor.AMARELO}Executando: Exclusão de Tabelas...{Cor.FIM}")
            eliminar_tabelas(con)
        elif opcao == '3':
            popular_banco(con)
            
        elif opcao == '4':
            inserir_registro_generico(con)
        elif opcao == '5':
            atualizar_registro_generico(con)
        elif opcao == '6':
            deletar_registro_generico(con)
            
        elif opcao == '7':
            consulta_1_veterinario(con)
        elif opcao == '8':
            consulta_2_peso_adultos(con)
        elif opcao == '9':
            consulta_3_historico_piquete(con)
            
        elif opcao == '10':
            analise_llm(con)
            
        elif opcao == '0':
            fechar_conexao(con)
            print(f"{Cor.AMARELO}\nSaindo do sistema.{Cor.FIM}")
            break
        else:
            print(f"{Cor.VERMELHO}Opção inválida. Escolha um número de 0 a 10.{Cor.FIM}")

if __name__ == "__main__":
    menu()