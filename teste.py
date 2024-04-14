import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET
import feed

class TestFeedFunctions(unittest.TestCase):
    @patch('feed.requests.get')
    def test_download_xml_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'<products><product><id>1</id><stock>5</stock></product></products>'
        result = feed.download_xml('https://example.com/feed.xml', 'feed.xml')
        self.assertTrue(result)

    @patch('feed.requests.get')
    def test_download_xml_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        result = feed.download_xml('https://example.com/invalid_feed.xml', 'invalid_feed.xml')
        self.assertFalse(result)

    def test_remover_produtos_sem_estoque(self):
        xml_string = '<products><product><id>1</id><stock>0</stock></product><product><id>2</id><stock>5</stock></product></products>'
        root = ET.fromstring(xml_string)
        feed.remover_produtos_sem_estoque(root)
        self.assertEqual(len(root.findall('product')), 1)
    
    def test_adicionar_cor_a_produtos(self):
        produto = ET.Element('product')
        id_produto = ET.SubElement(produto, 'id')
        id_produto.text = '261557'
        nome = ET.SubElement(produto, 'tittle')
        nome.text = 'Camisa Azul'
        cor = ET.SubElement(produto, 'color')
        feed.adicionar_cor_a_produtos('261557', ['261557'], produto)
        self.assertEqual(cor.text, 'Azul')

    def test_corrigir_links_de_imagem(self):
        produto = ET.Element('product')
        id_produto = ET.SubElement(produto, 'id')
        id_produto.text = '246804'
        link_imagem = ET.SubElement(produto, 'image_link')
        feed.corrigir_links_de_imagem('246804', ['246804'], produto)
        self.assertTrue(link_imagem.text.startswith('https://example.com/new_image_'))

    def test_processar_xml(self):
        xml_string = '<products><product><id>1</id><stock>0</stock></product><product><id>2</id><stock>5</stock></product></products>'
        root = ET.fromstring(xml_string)
        feed.processar_xml(root)
        self.assertEqual(len(root.findall('product')), 1)
    
    def test_salvar_xml(self):
        root = ET.Element('feed')
        feed.salvar_xml(root, 'teste.xml')
        with open('teste.xml', 'r') as f:
            content = f.read()
            self.assertIn('<feed />', content)
            
if __name__ == '__main__':
    unittest.main()
