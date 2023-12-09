import os
import requests
from requests_oauthlib import OAuth1
from config import MEDIAWIKI_CONFIG
import time
from datetime import datetime
import logging

# Configuração do log
log_filename = os.path.join(os.getcwd(), 'logs', 'uploader.log')
os.makedirs(os.path.join(os.getcwd(), 'logs'), exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def obter_entrada_usuario(mensagem):
    return input(mensagem)

def obter_token_edicao(oauth):
    # URL para obter o token de edição
    api_token_url = MEDIAWIKI_CONFIG['api_edit_url'] + '?action=query&meta=tokens&type=csrf&format=json'
    response_token = requests.get(url=api_token_url, auth=oauth)

    if response_token.status_code == 200:
        return response_token.json()['query']['tokens']['csrftoken']
    else:
        raise Exception(f'Erro ao obter o token de edição. Status: {response_token.status_code}, Resposta: {response_token.text}')

def verificar_pagina_existe(page_title, oauth):
    # URL para verificar se a página existe
    api_page_url = MEDIAWIKI_CONFIG['api_page_url'] + f'?action=query&titles={page_title}&format=json'
    response_page = requests.get(url=api_page_url, auth=oauth)

    if response_page.status_code == 200:
        pages = response_page.json()['query']['pages']
        return list(pages.keys())[0] != "-1"  # Retorna True se a página existe, False caso contrário
    else:
        raise Exception(f'Erro ao verificar se a página existe. Status: {response_page.status_code}, Resposta: {response_page.text}')

def realizar_edicao(page_title, post_content, token, oauth, nome_arquivo):
    # Verificar se a página já existe
    if verificar_pagina_existe(page_title, oauth):
        data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mensagem = f'A página {page_title} já existe. A edição não foi realizada.'
        print(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')
        logging.info(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')
        return

    # URL para a API de edição do MediaWiki
    api_edit_url = MEDIAWIKI_CONFIG['api_edit_url']

    # Parâmetros para a edição da página, incluindo o token de edição
    params = {
        'action': 'edit',
        'title': page_title,
        'text': post_content,
        'contentformat': 'text/x-wiki',
        'contentmodel': 'wikitext',
        'minor': 'true',
        'recreate': 'true',
        'summary': '',
        'format': 'json',
        'token': token  # Incluir o token de edição
    }

    # Requisição para editar a página
    response = requests.post(url=api_edit_url, auth=oauth, data=params)

    # Verificar o status da resposta
    if response.status_code == 200:
        data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mensagem = f'Postagem realizada com sucesso para a página: {page_title}'
        print(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')
        logging.info(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')
    else:
        data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mensagem = f'Erro ao postar para a página {page_title}. Status: {response.status_code}, Resposta: {response.text}'
        print(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')
        logging.error(f'[{data_hora_atual}] ({nome_arquivo}) {mensagem}')

def main():
    # Obtém o caminho para a pasta "payload" do projeto
    diretorio_base = os.path.join(os.getcwd(), 'payload')

    # Solicitar ao usuário o nome do subdiretório onde os arquivos .txt estão localizados
    subdiretorio = obter_entrada_usuario('Informe o subdiretório onde os arquivos .txt estão localizados: ')

    # Monta o caminho completo para o diretório
    diretorio = os.path.join(diretorio_base, subdiretorio)

    # Utilizando as credenciais do arquivo de configuração
    consumer_key = MEDIAWIKI_CONFIG['consumer_key']
    consumer_secret = MEDIAWIKI_CONFIG['consumer_secret']
    access_token = MEDIAWIKI_CONFIG['access_token']
    access_token_secret = MEDIAWIKI_CONFIG['access_token_secret']

    # Configuração do cliente OAuth1
    oauth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    # Obter o token de edição
    token = obter_token_edicao(oauth)

    # Iterar sobre os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # Ler o conteúdo do arquivo
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                linhas = file.readlines()

            # Usar a primeira linha como título e o restante como corpo da postagem
            page_title = linhas[0].strip()
            post_content = ''.join(linhas[1:])

            # Realizar a verificação e edição na página, passando o nome do arquivo
            realizar_edicao(page_title, post_content, token, oauth, arquivo)

            # Aguardar 2 segundos antes da próxima postagem
            time.sleep(2)

if __name__ == "__main__":
    main()
