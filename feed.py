import requests
import random
import string
import xml.etree.ElementTree as ET

# URL do feed XML
url = 'https://storage.cloud.google.com/psel-feedmanager/feed_psel.xml'

# Faz o download do arquivo XML
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Salva o conteúdo da resposta em um arquivo local
    with open('feed_.xml', 'wb') as f:
        f.write(response.content)
        print('Arquivo XML baixado com sucesso!')

    try:
        # Abre o arquivo XML
        tree = ET.parse('feed_psel.xml')
        root = tree.getroot()

        # Excluir produtos fora de estoque e salvar em um novo arquivo
        new_tree = ET.ElementTree(root)
        for product in root.findall('product'):
            stock = int(product.find('stock').text)
            if stock <= 0:
                root.remove(product)

        # IDs dos produtos para adicionar a cor
        product_ids = ['261557', '235840']

        # Iterar sobre os produtos no XML
        for product in root.findall('product'):
            product_id = product.find('id').text
            if product_id in product_ids:
                name = product.find('tittle').text  # Corrigido para 'tittle' em vez de 'title'
                last_word = name.split()[-1]  # Obtém a última palavra do título
                product.find('color').text = last_word

        # IDs dos produtos para corrigir os links de imagem
        product_ids_images = ['246804', '217865']

        # Corrigir os links das imagens para os IDs especificados
        for product in root.findall('product'):
            product_id = product.find('id').text
            if product_id in product_ids_images:
                # Gerar um link de imagem aleatório para cada ID
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=2))
                new_link = f'https://example.com/new_image_{random_suffix}.jpg'
                product.find('image_link').text = new_link
                print(f'Link de imagem corrigido para o produto ID {product_id}: {new_link}')

        tree.write('feed_updated.xml')
        print('Certo')

    except ET.ParseError as e:
        print(f'Erro ao abrir o arquivo XML: {e}')

else:
    print('Falha ao baixar o arquivo XML.')


