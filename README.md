# Processador de Feeds XML

Este é um projeto de processamento de feeds XML de produtos no Feed Manager.

## Descrição

O script em Python `feed.py` permite realizar diversas operações em feeds XML de produtos, incluindo download do XML, remoção de produtos sem estoque, adição de cor aos produtos e correção de links de imagem.

## Dependências

- `requests`
- `xml.etree.ElementTree

## Uso
1. #### Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/feed-xml-processor.git

2. #### Instale as dependências:
   ```bash
   python feed.py

3. #### Execute o script:
   ```bash
   python feed.py

## Funcionalidades:

   • Download de XML de feed
   
   • Remoção de produtos sem estoque
   
   • Adição de cor aos produtos
   
   • Correção de links de imagem
   
   
## Exemplo de Uso:

   import feed
   
   #### URL do feed XML e nome do arquivo local
      url = 'https://example.com/feed.xml'
      
      xml_feed = 'feed.xml'
   
   #### Download do arquivo XML
   
      feed.download_xml(url, xml_feed)
   
   #### Processar o XML
   
      root = feed.process_xml(xml_feed)
   
   #### Salvar o XML processado
      
      feed.save_xml(root, 'processed_feed.xml')

   
## Testes:
   Os testes estão localizados no arquivo test_feed.py. Execute os testes com o seguinte comando:
     
      python -m unittest test_feed.py
