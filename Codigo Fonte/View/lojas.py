import sqlite3

conn = sqlite3.connect('Model/onsell.db')
cursor = conn.cursor()


def listar_ids_e_nomes():
    
    # Consultar os IDs e nomes dos usuários
    cursor.execute("SELECT idloja, nomeloja FROM Lojas")
    resultados = cursor.fetchall()

    return resultados



def obter_id_por_nome(nome_loja):

    # Consultar o ID do usuário pelo nome
    cursor.execute("SELECT idloja FROM Lojas WHERE nomeloja = ?", (nome_loja,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0] 
    else:
        return None 
    


def escolher_loja():
   
   while True:
        print("\n\nLista de Lojas:\n")
        lojas = listar_ids_e_nomes()
        for i, loja in enumerate(lojas, start=1):
            print(f"{i}. {loja[1]}")

    
        num_loja = input("\nDigite o número da loja: ")
        if num_loja.isdigit():
            num_loja = int(num_loja)
            if num_loja < 1 or num_loja > len(lojas):
                print("Número de loja inválido. Tente novamente.")
            else:
                return lojas[num_loja - 1]
        else:
            print("Digite um numero.")