import requests
import random
import string
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

contador_sufixo = {}

def corrigir_links_de_imagem(id_item, ids_produtos_imagens, item):
    global contador_sufixo

    if id_item in ids_produtos_imagens:
        if id_item not in contador_sufixo:
            contador_sufixo[id_item] = 0
        
        sufixo_aleatorio = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        novo_link = f'https://example.com/new_image_{id_item}_{sufixo_aleatorio}.jpg'
        
        contador_sufixo[id_item] += 1
        
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

# URL do feed XML e nome do arquivo local
url = 'https://ff401d59c2a65eca56e0556319a230613acacb6808cee9dddf9201b-apidata.googleusercontent.com/download/storage/v1/b/psel-feedmanager/o/feed_psel.xml?jk=AWNiL9LLVdJGh0Co9PTJzhKJpMxLJk47hY1n8gkXUlca6j-h26XCqa1-76se6VLHqr5cdbS69vrWxyppjvDkj7kinPYBPQwnVuUZxbrJChaqwPO4yQSA5lrj1GG4DeDV8AdmLM-q4b9wxByQDW7ZlzGwcxv80mAqynyvvO62os4qV8JeMXl0q00LNr0iI5zMnAQfJqT00m_j6OcZlBN69d86B4hoti0WpN90t-ck-vtSWri5ge4EeJ_Wh6ITDaxvUKYgWAaCbCQ4Y44pChQZtogWTrA0WxHFVUp5cmr6boyPeS5asl4Cr9z-r8vw-GufEWruffuiw3j4UQamRU8RO_ive7yv6Xet-0Uq-mk-d5_W2KPkihaMdEczgGo5SY0p6AsygVD4XzcdgnNAiQQ8O9lcISNUkUC7CgmEyQENtXfsMSMrfoM_ntOMsBZ2ZBw-tTPZoF2mxe9xY2_gX7Xw0XcTWiiL-LjSd8-5Yt_qgsD_mRIN-cfUXbYs-M_re-okLse-dWY_b8Pcws_DhGyC6f0b_F-XwDGMC995kvaB_uAy6pGz_MDIa6HFhY4UwwXr8fYbqob4kdp6daHH6x5eZ2xa74Yk8C1nyJz4OEduTRl31Itu0ixu7DFpWcquf2wEemf-BXoCOANKrHps9tMDJXDQfsy8YWT4IDEyz5wAfLgUjAZ8owz1CWNfyVNvn9oJ5SFR5C1BuyDc7wbfXfywcyxzb7hgF6v7k7DYElOKnPj9yIQS3ychOojZGS0kDjoJ5A13MtQqa41culebF3adBkAq2JUfmhUb1mkHkH-E2yHz6MfF75nCBQ3f5dWS4fYruaz2dLnj_MltZz4qjQ4ZcYxx-L56TJsU8C3cc2QIkD4VyCPz4sU_O1mjATe4NUy1wcOl6DVROn1P7IBN7meF2jrEB1AhU4HpgyVSixqJOtZXUXHic28uHf4KWRF5Xtd-UrmBAL-1bGU24bzz-5kEO0whXQYPgJfi4LGBhD7FSPAs8EKSCuddSmNQFMnRLlYZK358vifG2TH-73bFThDFGP5RCjbOOiV-wjB8_sNbsSxLzBkKKr3sxqlvZZrpA3CtBqJc0ExHDwDHgxL44k399uGimQAkY94PDw&isca=1'
xml_feed = 'feed_psel.xml'

# Download do arquivo XML
if download_xml(url, xml_feed):
    arvore = ET.parse(xml_feed)
    raiz = arvore.getroot()

    processar_xml(raiz)

    nome_arquivo_corrigido = 'feed_corrigido.xml'
    salvar_xml(raiz, nome_arquivo_corrigido)
