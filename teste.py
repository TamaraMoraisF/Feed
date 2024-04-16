import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
import feed

class TestFeedFunctions(unittest.TestCase):
    @patch('feed.requests.get')
    def test_download_xml_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'<produtos><item><id>1</id><availability>"Em estoque"</availability></item></produtos>'
        result = feed.download_xml('https://example.com/feed.xml', 'feed.xml')
        self.assertTrue(result)

    @patch('feed.requests.get')
    def test_download_xml_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        result = feed.download_xml('https://example.com/invalid_feed.xml', 'invalid_feed.xml')
        self.assertFalse(result)

    def test_remover_produtos_sem_estoque(self):
        xml_string = '<produtos><item><id>1</id><availability>"Em estoque"</availability></item><item><id>2</id><availability>"Fora de estoque"</availability></item></produtos>'
        root = ET.fromstring(xml_string)
        item_a_remover = root.find("item[availability='\"Fora de estoque\"']")
        feed.remover_produtos_sem_estoque(root, item_a_remover)
        items_em_estoque = root.findall("item[availability='\"Fora de estoque\"']")
        self.assertEqual(len(items_em_estoque), 0)

    
    def test_adicionar_cor_a_produtos(self):
        item = ET.Element('item')
        id_produto = ET.SubElement(item, 'id')
        id_produto.text = '261557'
        nome = ET.SubElement(item, 'title')
        nome.text = 'Camisa Azul'
        cor = ET.SubElement(item, 'color')
        feed.adicionar_cor_a_produtos('261557', ['261557'], item)
        self.assertEqual(cor.text, 'Azul')

    def test_corrigir_links_de_imagem(self):
        item = ET.Element('item')
        id_produto = ET.SubElement(item, 'id')
        id_produto.text = '246804'
        link_imagem = ET.SubElement(item, 'image_link')
        feed.corrigir_links_de_imagem('246804', ['246804'], item)
        self.assertTrue(link_imagem.text.startswith('https://example.com/new_image_'))

    def test_processar_xml(self):
        xml_string = '<produtos><item><id>1</id><availability>"Em estoque"</availability></item><item><id>2</id><availability>"Fora de estoque"</availability></item></produtos>'
        root = ET.fromstring(xml_string)
        feed.processar_xml(root)
        self.assertEqual(root.find('item/id').text, '1')


    def test_salvar_xml(self):
        root = ET.Element('feed')
        feed.salvar_xml(root, 'teste.xml')
        with open('teste.xml', 'r') as f:
            content = f.read()
            self.assertIn('<feed />', content)

if __name__ == '__main__':
    unittest.main()
