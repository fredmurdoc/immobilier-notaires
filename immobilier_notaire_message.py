from termios import VT1
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import re
import logging
import os.path
from enum import Enum
        
class ImmobilierNotairesMessageXpathFinderV1():
    ITEMS_PARENT_TAG_TR = '//tr[./td/div/table/tr/td/a[contains(@href, "https://www.immobilier.notaires.fr/")]/img]'
    ITEM_IMAGE = './/img'
    ITEM_URL = './/a'
    ITEM_DETAIL_PARENT_TAG = './td/div/table/tr/td/table'
    ITEM_DETAIL = './/span'
    
class ImmobilierNotairesMessage:
    REGEXP_SUPERFICIE = r'\s*(?P<superficie>[0-9]+)\s+m\u00b2.*'
    REGEXP_NBPIECES= r'.+\s+(?P<nb_pieces>[0-9]+)\s+pièce.\s+.*'
    REGEXP_COMMUNE_DEPARTEMENT= r'\s*(?P<commune>[^0-9]+)\s+\((?P<cp>[0-9]{2})\)\s*'
    def __init__(self):
        self.finder = None
        self.date = None
    def loadFromFile(self, file):
        self.date = os.path.getmtime(file)
        with open(file, 'r') as fp:
            content = fp.read()
            self.loadFromString(content)
            fp.close()    
    
    def loadFromString(self, payload):
        soup = BeautifulSoup(payload, "html.parser")
        self.dom = etree.HTML(str(soup))
        #logging.debug(etree.tostring(self.dom))
    
    def _find_search_items(self):
        results = self.dom.xpath(ImmobilierNotairesMessageXpathFinderV1.ITEMS_PARENT_TAG_TR)
        self.finder = ImmobilierNotairesMessageXpathFinderV1
        """
        if results is None or len(results) == 0:
            results = self.dom.xpath(ImmobilierNotairesXpathFinderV2.ITEMS_PARENT_TAG_TR)
            self.finder = ImmobilierNotairesXpathFinderV2
        """
        if results is None or len(results) == 0:
            raise Exception('cannot find compatible finder')    
        if results is None or len(results) < 2:
            raise Exception('cannot find results')    
        
        return results[1:]

    def _find_detail_element(self, parent_item):
        element = parent_item.find(self.finder.ITEM_DETAIL_PARENT_TAG)
        return element

    def _find_search_item_url(self, parent_item):
        element = parent_item.find(self.finder.ITEM_URL)
        return element.attrib['href'] if element is not None else None

    def _find_search_item_superficie(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL)[3]
        if element is None:
            return None
        m = re.search(self.REGEXP_SUPERFICIE, element.text)
        return int(m.group('superficie')) if m is not None else None

    def _find_search_item_superficie_terrain(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL)[5]
        if element is None:
            return None
        m = re.search(self.REGEXP_SUPERFICIE, element.text)
        return int(m.group('superficie')) if m is not None else None

    
    def _find_search_ITEM_INTITULE(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL)[0]
        return element.text if element is not None else None

    def _find_search_item_prix(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL)[1]
        return int(element.text.replace(' ', '').replace('€','')) if element is not None else None

    def _find_search_item_commune_departement(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL)[2]
        return element.text if element is not None else None

    def _find_search_item_commune(self, parent_item):
        com_cp = self._find_search_item_commune_departement(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_DEPARTEMENT, com_cp)
        return m.group('commune') if m is not None else None

    def _find_search_item_commune_codepostal(self, parent_item):
        com_cp = self._find_search_item_commune_cp(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_CP, com_cp)
        return m.group('cp') if m is not None else None


    def _find_search_item_image_url(self, parent_item):
        element =  parent_item.find(self.finder.ITEM_IMAGE)
        return element.attrib['src']
        
        
    def _extract_dict_from_parent_item(self, parent_item):
        return {
        'date_mail' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'created_at' : datetime.now().strftime('%Y-%m-%d'),
        'url' : self._find_search_item_url(parent_item),
        'prix' : self._find_search_item_prix(parent_item),
        'intitule' : self._find_search_ITEM_INTITULE(parent_item),
        'commune' : self._find_search_item_commune(parent_item),
        'code_postal' : self._find_search_item_commune_codepostal(parent_item),
        'image_url' : self._find_search_item_image_url(parent_item),
        'superficie' : self._find_search_item_superficie(parent_item),
        'nb_pieces' : self._find_search_item_nb_pieces(parent_item)
        }
    
    def extract_items(self):
        extract = []
        items = self._find_search_items()
        for item in items:
            extract.append(self._extract_dict_from_parent_item(item))
        return extract
    