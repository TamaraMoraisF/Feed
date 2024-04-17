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

# URL do feed XML e nome do arquivo local
url = 'https://ff06c38d0d5fb6cd1061f0be32d425c9ca90486fbad802ef2d697b4-apidata.googleusercontent.com/download/storage/v1/b/psel-feedmanager/o/feed_psel.xml?jk=AWNiL9J7fcU0wifZa6Na8sdOUNMbaecDwuq4vYazphRAX9o2dTynrGFvwBsP1lCGobUUSqPeJdeyKsKSP021mMocGSXhpDsY6uzaMEHqkdm6jxhMW49oqKXrZB9K6kRm3muu-o3EqEWW9sR3zKHqGoZvsZGU_YG_1Vs4p-6FlRPF8wkHQ6L457CUBJRxtAlo-CRnUIDkUijrQvQKFQC7byz8cWybB-qYWpKr8F8P3Vtb151trjv35eMGeR1Jr-kr0PtQ59IQ_Rbwpznh0TYT2yX6o_c6sw1MkGTwJLyF5AaAokuJiaAv2i5BPKW6kA8EBrhqlaTDis7Tav-e67uaCjxLKgNA1wMlUPf7cDXY-aM8DfnyRPrteW3NQv3lxWtkSHToe6ny3D4BxqjC8ZrvCcDi7dnteFJquHmx9EWVHNNFcOrElmUz6RXHwof9FwltGQyuiS2rl_vIhQX_Zqqrm8nxGX2HLt_UhkD8TpqXu4VY6CzK9aC-zL0aLI_fMBgbK8L0rxbEMN5XGjEf4ick4y2Ichp1fsejc2rejO0-m2_AUP40K19civSKMKENImcwzcGMmMMqe1VypO932Fsoc6mBvOjqBIOcaeD_5Y0cjRJyByvBIHUg9dWRLhgH3koHIiPdyn814x6hRXl300MrUbMWSShPS91tc85aF0x4VXrgwSRkCYB1Omv4KyckNCfGSCvIVbqQOe_xvBS9t5ogKg1bpYhZY_IyRSUNmtXIo8ewd_ZUxPM2nUtHqydA0hHv8UvnVax3597_D5Nqw__6x8wsZ2MSbNVrPfnPjiQPEhJ2R98YoIbdqLdJAryCkxgFvSu8qZOx54QA8lqWFkI5St6x3j3bRMUNUbkTL8YIM84C9VtSvmemvnP5lMRWp_9XCpS_V4qkok6uU70DVS7Z6KwSfh-WgOfCSU5bJqSpFsToi0zxWN8XpHtNCmCeBIp9XQnOLV0yUPR1lgBNkxTnrPALB1M2D7E-wn4E_roS5bFkZmwyjJJpahlypc48z_1mGc-W83LgAURYFE6Ddm1Esi5qQV5CyTZVCUXMoLotKDxzOSBG-LPU4r36dOcJKFLSbva6GFf9p1nQSAAkuXodf4uJwd90mjattA&isca=1'
xml_feed = 'feed_psel.xml'

# Download do arquivo XML
if download_xml(url, xml_feed):
    arvore = ET.parse(xml_feed)
    raiz = arvore.getroot()

    processar_xml(raiz)

    nome_arquivo_corrigido = 'feed_corrigido.xml'
    salvar_xml(raiz, nome_arquivo_corrigido)
