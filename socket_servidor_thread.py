import socket
import threading
import os
from dotenv import load_dotenv
import sqlite3

# Carrega as variáveis do arquivo .env
load_dotenv()

from Model.consultar_usuario import verificar_usuario
from Model.adicionar_venda import cadastrar_venda
from Model.consultar_venda import consultar_total_vendedor
from Model.consultar_loja import consultar_melhor_loja
from Model.consultar_usuario import consultar_melhor_vendedor
from Model.consultar_rede import consultar_vendas_rede

host = os.getenv('HOST')
port = 3333  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

connections = []

def handle_client(client_socket):
    # Cria uma nova conexão com o banco de dados
    db_connection = sqlite3.connect('nome_do_banco_de_dados.db')
    cursor = db_connection.cursor()

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        dados_recebidos = data.decode()
        data_array = dados_recebidos.split(",")

        if data_array[0] == '01.1':
            get = verificar_usuario(data_array[1])
            if get[0] == True:
                response = get
            elif get[0] == False:
                response = get[0]
            else:
                response = 'ERROR: Usuario desconhecido'

        elif data_array[0] == '02.0':
            if cadastrar_venda(data_array):
                response = True, 'Venda cadastrada com sucesso'
            else: 
                response = False, 'ERROR: Venda não cadastrada'

        elif data_array[0] == '03.1':
            response = consultar_total_vendedor(data_array[1])
        elif data_array[0] == '03.2':
            response = consultar_melhor_loja()
        elif data_array[0] == '03.3':
            response = consultar_melhor_vendedor(cursor)
        elif data_array[0] == '03.4':
            response = consultar_vendas_rede(cursor, data_array[1], data_array[2], data_array[3])
        else:
            print('ERROR: Unknown message type' + data_array[0])
            response = ''

        if not isinstance(response, bool):
            message_str = ','.join([str(item) for item in response])
        else:
            # Converte apenas o primeiro elemento em uma string
            message_str = [str(response[0])]
            # Concatena os demais elementos à lista de strings
            message_str.extend(response[1:])
            # Junta todos os elementos da lista em uma única string
            message_str = ','.join(message_str)

        client_socket.send(message_str.encode())
        print("messagem enviada: ", message_str)
   
    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    db_connection.close()

    client_socket.close()

def main():
    server_socket.listen(10)  
    try:
        while True:
            print('Aguardando conexões...')
            client_socket, client_address = server_socket.accept()
            print('Conexão estabelecida com:', client_address)
            connections.append(client_socket)
            
            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
            
    except ConnectionResetError:
         # Tratamento da exceção de conexão resetada pelo cliente
        print('Conexão resetada pelo cliente: ', client_address)
        connections.remove(client_socket)
        server_socket.close()

main()