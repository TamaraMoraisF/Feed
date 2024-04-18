import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
import feed

class TestFuncoesFeed(unittest.TestCase):
    @patch('feed.requests.get')
    def teste_download_xml_sucesso(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'<produtos><item><id>1</id><availability>"Em estoque"</availability></item></produtos>'
        resultado = feed.download_xml('https://exemplo.com/feed.xml', 'feed.xml')
        self.assertTrue(resultado)

    @patch('feed.requests.get')
    def teste_download_xml_falha(self, mock_get):
        mock_get.return_value.status_code = 404
        resultado = feed.download_xml('https://exemplo.com/invalid_feed.xml', 'invalid_feed.xml')
        self.assertFalse(resultado)

    def teste_remover_item_sem_estoque(self):
        xml_string = '<produtos><item><id>1</id><availability>"Em estoque"</availability></item><item><id>2</id><availability>"Fora de estoque"</availability></item></produtos>'
        root = ET.fromstring(xml_string)
        item_a_remover = root.find("item[availability='\"Fora de estoque\"']")
        feed.remover_item_sem_estoque(root, item_a_remover)
        items_em_estoque = root.findall("item[availability='\"Fora de estoque\"']")
        self.assertEqual(len(items_em_estoque), 0)

    def teste_adicionar_cor_ao_item(self):
        item = ET.Element('item')
        id_produto = ET.SubElement(item, 'id')
        id_produto.text = '261557'
        nome = ET.SubElement(item, 'title')
        nome.text = 'Camisa Azul'
        cor = ET.SubElement(item, 'color')
        feed.adicionar_cor_ao_item('261557', ['261557'], item)
        self.assertEqual(cor.text, 'Azul')

    def teste_corrigir_links_de_imagem(self):
        xml_string = '<produtos>' \
                    '<item><id>246804</id><availability>"Em estoque"</availability><image_link>https://exemplo.com/old_image.mp3</image_link></item>' \
                    '<item><id>217865</id><availability>"Fora de estoque"</availability><image_link>https://exemplo.com/old_image.mp3</image_link></item>' \
                    '</produtos>'
        root = ET.fromstring(xml_string)
        item_a_corrigir = root.find("item[id='246804']")
        feed.corrigir_links_de_imagem('246804', ['246804'], item_a_corrigir)
        link_corrigido = item_a_corrigir.find('image_link').text
        self.assertTrue(link_corrigido.startswith('https://exemplo.com/old_image.jpg'))


    def teste_processar_xml(self):
        xml_string = '<produtos>' \
                    '<item><id>1</id><title>Produto 1</title><availability>"Em estoque"</availability></item>' \
                    '<item><id>261557</id><title>Camisa Azul</title><availability>"Em estoque"</availability><color>Azul</color></item>' \
                    '<item><id>246804</id><title>Produto 3</title><availability>"Em estoque"</availability><image_link>https://exemplo.com/old_image.mp3</image_link></item>' \
                    '<item><id>999999</id><title>Produto 4</title><availability>"Fora de estoque"</availability></item>' \
                    '</produtos>'
        root = ET.fromstring(xml_string)
        feed.processar_xml(root)
        items_em_estoque = root.findall("item[availability='\"Fora de estoque\"']")
        self.assertEqual(len(items_em_estoque), 0)

        item_cor_azul = root.find("item[id='261557']")
        cor_azul = item_cor_azul.find('color').text
        self.assertEqual(cor_azul, 'Azul')

        item_link_corrigido = root.find("item[id='246804']")
        link_corrigido = item_link_corrigido.find('image_link').text
        self.assertTrue(link_corrigido.startswith('https://exemplo.com/old_image.jpg'))

        item_com_estoque = root.find("item[id='999999']")
        self.assertIsNone(item_com_estoque)

    def teste_salvar_xml(self):
        root = ET.Element('feed')
        feed.salvar_xml(root, 'teste.xml')
        with open('teste.xml', 'r') as f:
            conteudo = f.read()
            self.assertIn('<feed />', conteudo)

    def teste_pode_corrigir(self):
        id_item = '246804'
        ids_produtos_imagens = ['246804', '217865']
        estoque_em = '"Em estoque"'
        estoque_fora = '"Fora de estoque"'
        
        resultado_em_estoque = feed.pode_corrigir(id_item, ids_produtos_imagens, estoque_em)
        self.assertTrue(resultado_em_estoque)

        resultado_fora_estoque = feed.pode_corrigir(id_item, ids_produtos_imagens, estoque_fora)
        self.assertFalse(resultado_fora_estoque)

        id_item_nao_corrigir = '999999'
        resultado_id_invalido = feed.pode_corrigir(id_item_nao_corrigir, ids_produtos_imagens, estoque_em)
        self.assertFalse(resultado_id_invalido)

if __name__ == '__main__':
    unittest.main()
