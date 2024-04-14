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

def remove_out_of_stock_products(root):
    for product in root.findall('product'):
        stock = int(product.find('stock').text)
        if stock <= 0:
            root.remove(product)

def add_color_to_products(root, product_ids_color):
    for product in root.findall('product'):
        product_id = product.find('id').text
        if product_id in product_ids_color:
            name = product.find('tittle').text
            last_word = name.split()[-1]
            product.find('color').text = last_word

def correct_image_links(root, product_ids_images):
    for product in root.findall('product'):
        product_id = product.find('id').text
        if product_id in product_ids_images:
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=2))
            new_link = f'https://example.com/new_image_{product_id}_{random_suffix}.jpg'
            product.find('image_link').text = new_link
            print(f'Link de imagem corrigido para o produto ID {product_id}: {new_link}')

def save_xml(root, filename):
    tree = ET.ElementTree(root)
    tree.write(filename)
    print('Arquivo XML atualizado com sucesso.')

# URL do feed XML e nome do arquivo local
url = 'https://storage.cloud.google.com/psel-feedmanager/feed_psel.xml'
xml_dowload = 'feed_.xml'
xml_edit = 'feed_psel.xml'

# Download do arquivo XML
if download_xml(url, xml_dowload):
    # Abre o arquivo XML
    tree = ET.parse(xml_edit)
    root = tree.getroot()

    # Excluir produtos fora de estoque
    remove_out_of_stock_products(root)

    # IDs dos produtos para adicionar cor
    product_ids_color = ['261557', '235840']
    add_color_to_products(root, product_ids_color)

    # IDs dos produtos para corrigir os links de imagem
    product_ids_images = ['246804', '217865']
    correct_image_links(root, product_ids_images)

    # Salvar as alterações em um novo arquivo XML
    updated_xml_filename = 'feed_updated.xml'
    save_xml(root, updated_xml_filename)



