#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Echo - Exemplo de Socket TCP
Devolve qualquer mensagem que recebe (echo).
Versão concorrente com suporte a múltiplas conexões (Threads).
"""

import socket
import threading
import time

def handle_client(conexao, endereco):
    """Trata conexão de um cliente em uma thread separada"""
    print(f'[{time.strftime("%H:%M:%S")}] Conectado com {endereco}')
    
    try:
        while True:
            # Receber dados
            dados = conexao.recv(1024)
            
            if not dados:
                print(f'[{time.strftime("%H:%M:%S")}] Cliente {endereco} desconectou')
                break
                
            mensagem = dados.decode('utf-8')
            print(f'[{time.strftime("%H:%M:%S")}] Recebido de {endereco}: {mensagem}')
            
            # Enviar dados de volta (echo)
            resposta = f'Echo: {mensagem}'
            conexao.send(resposta.encode('utf-8'))
            
    except Exception as e:
        print(f'[{time.strftime("%H:%M:%S")}] Erro ao processar {endereco}: {e}')
    finally:
        conexao.close()
        print(f'[{time.strftime("%H:%M:%S")}] Conexão com {endereco} fechada')

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 5000))
servidor.listen(5)
print(f'[{time.strftime("%H:%M:%S")}] Servidor Echo (Concorrente) escutando em localhost:5000')

try:
    while True:
        print(f'[{time.strftime("%H:%M:%S")}] Aguardando conexão...')
        conexao, endereco = servidor.accept()
        
        # Criar thread para cada cliente
        thread = threading.Thread(target=handle_client, args=(conexao, endereco))
        thread.daemon = True
        thread.start()
        
except KeyboardInterrupt:
    print(f'\n[{time.strftime("%H:%M:%S")}] Servidor encerrado')
finally:
    servidor.close()