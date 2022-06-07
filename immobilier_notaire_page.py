from termios import VT1
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import re
import logging
import os.path
from enum import Enum
        
class ImmobilierNotairesPageXpathFinderV1():
    ITEM_CONTAINER = '//inotr-bloc-annonce'
    ITEM_IMAGE = './/div[@class="container_photo"]//img'
    ITEM_URL = './/div[@class="container_photo"]//a'
    ITEM_LOCALISATION = './/span[@class="localisation"]'
    ITEM_DESCRIPTION ='.//div[@class="inotr-description"]/p'
    ITEM_IS_LOCATION = '//div[@data-prix-prioritaire]/span[@class="mois"]'
    ITEM_DETAIL_PARENT_TAG = './div[@class="container_detail"]'
    ITEM_DETAIL_TYPE = './/span[@class="type_bien"]'
    ITEM_DETAIL_NBPIECES = './/span[@class="pieces"]'
    ITEM_DETAIL_LOCALISATION = './/span[@class="localisation"]'
    ITEM_DETAIL_PRIX = './/div[@data-prix-prioritaire and @class="valeur"]'
    ITEM_DETAIL_SURFACE = './/div[@id="data-description-surface"]'
    
class ImmobilierNotairesPage:
    REGEXP_SUPERFICIE = r'\s*(?P<superficie>[0-9]+)\s+m\u00b2.*'
    REGEXP_NBPIECES= r'.+\s+(?P<nb_pieces>[0-9]+)\s+pièce.\s+.*'
    REGEXP_COMMUNE_CP= r'\s*(?P<commune>[^0-9]+)\s+\((?P<cp>[0-9]{2})\)\s*'
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
        results = []
        raw_results = self.dom.xpath(ImmobilierNotairesPageXpathFinderV1.ITEM_CONTAINER)
        self.finder = ImmobilierNotairesPageXpathFinderV1
        
        if raw_results is None or len(raw_results) == 0:
            raise Exception('cannot find compatible finder')    
        
        for item in raw_results:
            # on n'ajoute que les annonces qui ne sont pas des locations
            if item.xpath(self.finder.ITEM_IS_LOCATION) is None:
                results.append(item)

        return results

    def _find_detail_element(self, parent_item):
        element = parent_item.find(self.finder.ITEM_DETAIL_PARENT_TAG)
        return element

    def _find_search_item_url(self, parent_item):
        element = parent_item.find(self.finder.ITEM_URL)
        return element.attrib['href'] if element is not None else None

    def _find_search_item_superficie(self, parent_item):
        element = parent_item.find(self.finder.ITEM_DETAIL_SURFACE)
        if element is None:
            return None
        m = re.search(self.REGEXP_SUPERFICIE, element.text)
        return int(m.group('superficie')) if m is not None else None

    
    def _find_search_ITEM_INTITULE(self, parent_item):
        element = parent_item.find(self.finder.ITEM_DETAIL)
        return element.text if element is not None else None

    def _find_search_item_prix(self, parent_item):
        element = parent_item.find(self.finder.ITEM_DETAIL_PRIX)
        return int(element.text.replace(' ', '').replace('€','')) if element is not None else None

    def _find_search_item_commune_cp(self, parent_item):
        element = parent_item.xpath(self.finder.ITEM_DETAIL_LOCALISATION)
        return element.text if element is not None else None

    def _find_search_item_commune(self, parent_item):
        com_cp = self._find_search_item_commune_cp(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_CP, com_cp)
        return m.group('commune') if m is not None else None

    def _find_search_item_codepostal(self, parent_item):
        com_cp = self._find_search_item_commune_cp(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_CP, com_cp)
        return m.group('cp') if m is not None else None

    def _find_search_item_image_url(self, parent_item):
        element =  parent_item.find(self.finder.ITEM_IMAGE)
        return element.attrib['src']
        
    def _find_search_item_nb_pieces(self, parent_item):
        element =  parent_item.find(self.finder.ITEM_DETAIL_NBPIECES)
        if element is None:
            return None
        m = re.search(self.REGEXP_NBPIECES, element.text)
        return int(m.group('nb_pieces')) if m is not None else None



    def _extract_dict_from_parent_item(self, parent_item):
        return {
        'date_mail' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'created_at' : datetime.now().strftime('%Y-%m-%d'),
        'url' : self._find_search_item_url(parent_item),
        'prix' : self._find_search_item_prix(parent_item),
        'intitule' : self._find_search_ITEM_INTITULE(parent_item),
        'commune' : self._find_search_item_commune(parent_item),
        'code_postal' : self._find_search_item_codepostal(parent_item),
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
    