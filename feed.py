import requests
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

        tree.write('feed_updated.xml')
        print('Produtos sem estoque removidos e tags color atualizadas com sucesso!')

    except ET.ParseError as e:
        print(f'Erro ao abrir o arquivo XML: {e}')

else:
    print('Falha ao baixar o arquivo XML.')




# Excluir produtos fora de estoque

# Adicionar cor aos produtos especificados

# Corrigir links das imagens dos produtos com IDs específicos

