import logging
import json
import sys
import os.path
import os
from datetime import datetime

"""
Concat toutes les annonces collectées dans un seul fichier json items.json
"""


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
def concat_all_annonces():
    items = []
    items_file = 'items.json'
    url_annonces = {}
    json_content = []
    is_updated_at = datetime.now().strftime('%Y-%m-%d')
    directory = 'annonces'
    for annonce_file in os.listdir(directory):
        
        
        json_file_annonce_path = os.path.join(directory, annonce_file)
        with open(json_file_annonce_path, 'r') as fp:
            items.extend(json.load(fp))

    with open(items_file, 'w') as fp:
        json.dump(items, fp)
            
if __name__ == '__main__':
    concat_all_annonces()