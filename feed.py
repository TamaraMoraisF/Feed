import requests
import random
import string
import xml.etree.ElementTree as ET

def download_xml(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print('Arquivo XML baixado com sucesso!')
        return True
    else:
        print('Falha ao baixar o arquivo XML.')
        return False

def remover_produtos_sem_estoque(root):
    for produto in root.findall('product'):
        estoque = int(produto.find('stock').text)
        if estoque <= 0:
            root.remove(produto)

def adicionar_cor_a_produtos(id_produto, ids_produtos_cor, produto):
    if id_produto in ids_produtos_cor:
        nome = produto.find('tittle').text
        ultima_palavra = nome.split()[-1]
        produto.find('color').text = ultima_palavra

def corrigir_links_de_imagem(id_produto, ids_produtos_imagens, produto):
    if id_produto in ids_produtos_imagens:
        sufixo_aleatorio = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        novo_link = f'https://example.com/new_image_{sufixo_aleatorio}.jpg'
        produto.find('image_link').text = novo_link
        print(f'Link de imagem corrigido para o produto ID {id_produto}: {novo_link}')

def processar_xml(root):
    for produto in root.findall('product'):
        remover_produtos_sem_estoque(root)

        id_produto = produto.find('id').text

        ids_produtos_cor = ['261557', '235840']
        adicionar_cor_a_produtos(id_produto, ids_produtos_cor, produto)

        ids_produtos_imagens = ['246804', '217865']
        corrigir_links_de_imagem(id_produto, ids_produtos_imagens, produto)

def salvar_xml(root, nome_arquivo):
    arvore = ET.ElementTree(root)
    arvore.write(nome_arquivo)
    print('Arquivo XML corrigido com sucesso.')

# URL do feed XML e nome do arquivo local
url = 'https://storage.cloud.google.com/psel-feedmanager/feed_psel.xml'
xml_feed = 'feed_psel.xml'
xml_exemplo = 'feed_psel_exemplo.xml'

# Download do arquivo XML
if download_xml(url, xml_feed):
    arvore = ET.parse(xml_exemplo)
    raiz = arvore.getroot()

    processar_xml(raiz)

    nome_arquivo_corrigido = 'feed_corrigido.xml'
    salvar_xml(raiz, nome_arquivo_corrigido)
