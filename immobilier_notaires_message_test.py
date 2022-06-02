from dis import pretty_flags
from itertools import count
import unittest
from immobilier_notaire_message import ImmobilierNotairesMessageXpathFinderV1, ImmobilierNotairesMessage
from lxml import etree
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
class TestImmobilierNotairesMessage(unittest.TestCase):

    def test_init_v1_ok(self):
        msg = ImmobilierNotairesMessage()
        msg.loadFromFile('tests/v1.html')
        self.assertIsNotNone(msg.dom)

    
    def test_find_search_items_v1(self):
        msg = ImmobilierNotairesMessage()
        msg.loadFromFile('tests/v1.html')
        items = msg._find_search_items()
        self.assertIsNotNone(items)
        self.assertEquals(len(items), 1)


    def test_find_search_items_and_guess_finder_v1(self):
        msg = ImmobilierNotairesMessage()
        msg.loadFromFile('tests/v1.html')
        msg._find_search_items()
        self.assertEqual(ImmobilierNotairesMessageXpathFinderV1, msg.finder)


    

    def get_first_item(self, fileTested):
        self.msg = ImmobilierNotairesMessage()
        self.msg.loadFromFile(fileTested)
        items = self.msg._find_search_items()
        """
        logging.debug('##############')
        logging.debug(items[0].tag)
        logging.debug(etree.tostring(items[0]))
        """
        return items[0]

    def debug_element(self, elem):
        logging.debug("### CHILD of %s" % elem.tag)
        counter = 0
        for child in elem.iter():
            logging.debug('----- counter child %s -----' % counter)
            logging.debug(child.tag)
            logging.debug(etree.tostring(child, pretty_print=True, method='html'))
            counter += 1
    def assert_url(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_url(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
        

    def assert_image(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_image_url(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
   
    def assert_superficie(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_superficie(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def assert_nbpieces(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_nb_pieces(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
        
    
    def assert_commune(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_commune(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)

    def assert_commune_codepostal(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_commune_codepostal(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)

    def assert_prix(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_item_prix(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def assert_description(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.msg._find_search_ITEM_INTITULE(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def test_find_search_item_url_v1(self):
        self.assert_url('tests/v1.html', 'https://www.immobilier.notaires.fr/fr/annonce-immo-detail/?idAnnonce=1478994&utm_source=alert&utm_medium=email&utm_campaign=annonces')

    def test_find_search_item_image_url_v1(self):
        self.assert_image('tests/v1.html', 'https://media.immobilier.notaires.fr/inotr/media/29/44051/1478994/137da42e_QQVGA.jpg')

    def test_find_detail_element(self):    
        item = self.get_first_item('tests/v1.html')
        detail_element = self.msg._find_detail_element(item)
        #self.debug_element(detail_element)
        self.assertIsNotNone(detail_element)

    def test_find_search_item_commune_departement(self):
        item = self.get_first_item('tests/v1.html')
        item_commune_departement = self.msg._find_search_item_commune_departement(item)
        logging.debug(item_commune_departement)
        self.assertIsNotNone(item_commune_departement)

    def test_find_search_item_description_v1(self):
        item = self.get_first_item('tests/v1.html')
        self.assert_description('tests/v1.html', 'Maison / villa')
    
    
    
    def test_find_search_item_prix_v1(self):
        self.assert_prix('tests/v1.html', 58750)

        
    def test_find_search_item_commune_v1(self):
        self.assert_commune('tests/v1.html', 'RIAILLE')
    
    def test_find_search_item_superficie_v1(self):
        self.assert_superficie('tests/v1.html', 80)
    

if __name__ == '__main__':
    unittest.main()

