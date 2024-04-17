import requests
import xml.etree.ElementTree as ET

def download_xml(url, filename):
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("Falha ao obter o XML:", response.status_code)
        return False
    
def remover_produtos_sem_estoque(root, item):
    estoque = item.find('availability').text
    if estoque != '"Em estoque"':
        root.remove(item)

def adicionar_cor_a_produtos(id_item, ids_produtos_cor, item):
    if id_item in ids_produtos_cor:
        nome = item.find('title').text
        ultima_palavra = nome.split()[-1]
        item.find('color').text = ultima_palavra

def corrigir_links_de_imagem(id_item, ids_produtos_imagens, item):
    estoque = item.find('availability').text
    if estoque == '"Em estoque"' and id_item in ids_produtos_imagens:
        novo_link = item.find('image_link').text.replace('.mp3', '.jpg')
        item.find('image_link').text = novo_link
        print(f'Link de imagem corrigido para o item ID {id_item}: {novo_link}')


def processar_xml(root):
    for item in root.findall('item'):
        remover_produtos_sem_estoque(root, item)

        id_item = item.find('id').text

        ids_produtos_cor = ['261557', '235840']
        adicionar_cor_a_produtos(id_item, ids_produtos_cor, item)

        ids_produtos_imagens = ['246804', '217865']
        corrigir_links_de_imagem(id_item, ids_produtos_imagens, item)

def salvar_xml(root, nome_arquivo):
    with open(nome_arquivo, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        nova_arvore = ET.ElementTree(root)
        nova_arvore.write(f, encoding='utf-8', xml_declaration=False, default_namespace=None, short_empty_elements=True)

    print('Arquivo XML corrigido com sucesso.')

# URL direta de download do XML no Google Cloud Storage
url_xml = 'https://storage.googleapis.com/psel-feedmanager/feed_psel.xml'

# Download do arquivo XML
if download_xml(url_xml, 'feed_psel.xml'):
    arvore = ET.parse('feed_psel.xml')
    raiz = arvore.getroot()

    processar_xml(raiz)

    nome_arquivo_corrigido = 'feed_corrigido.xml'
    salvar_xml(raiz, nome_arquivo_corrigido)
else:
    print("Não foi possível baixar o XML.")
