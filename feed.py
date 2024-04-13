import requests

# URL do feed XML
url = 'https://storage.cloud.google.com/psel-feedmanager/feed_psel.xml'

# Faz o download do arquivo XML
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Salva o conteúdo da resposta em um arquivo local
    with open('feed_fake.xml', 'wb') as f:
        f.write(response.content)
        print('Arquivo XML baixado com sucesso!')
else:
    print('Falha ao baixar o arquivo XML.')

# Excluir produtos fora de estoque

# Adicionar cor aos produtos especificados

# Corrigir links das imagens dos produtos com IDs específicos

