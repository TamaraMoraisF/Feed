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

        # Excluir produtos fora de estoque
        for product in root.findall('product'):
            stock = product.find('stock').text
            if int(stock) <= 0:
                root.remove(product)

        # Salva as alterações em um novo arquivo XML
        tree.write('feed_updated.xml')
        print('Produtos fora de estoque removidos com sucesso!')

    except ET.ParseError as e:
        print(f'Erro ao abrir o arquivo XML: {e}')

else:
    print('Falha ao baixar o arquivo XML.')

# Excluir produtos fora de estoque

# Adicionar cor aos produtos especificados

# Corrigir links das imagens dos produtos com IDs específicos

