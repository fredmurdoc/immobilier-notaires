import os
from posixpath import dirname
import json
from datetime import datetime
from immobilier_notaire_message import ImmobilierNotairesMessage

def extract_items():
    url_annonces = {}
    json_content = []
    
    directory = '%s/results' % dirname(__file__)
    for payload_file in os.listdir(directory):
        f = os.path.join(directory, payload_file)
        extension = os.path.splitext(payload_file)[1]
        # checking if it is a file
        if os.path.isfile(f) and extension == '.html':
            #get payload file
            print('analyze payload file %s' % payload_file)
            #analyse it
            msg = ImmobilierNotairesMessage()
            msg.loadFromFile(f)
            try:
                extracted = msg.extract_items()
                json_content.extend(extracted)
            except Exception as e:
                print(e)    
    #on recherche les annonces en doublons 
    for index, item in enumerate(json_content):
        print(index)
        if item['url'] not in url_annonces.keys():
            url_annonces[item['url']] = { 'date': item['date_mail'], 'index': index}
        else: #si la date croisée est plus recente on la conserve comme reference et 
            if url_annonces[item['url']]['date'] < item['date_mail']:
                url_annonces[item['url']] = { 'date': item['date_mail'], 'index': index}
    
    items = []
    # on ajoute que les items a conserver
    for url, item_to_keep in url_annonces.items():
        print(item_to_keep)
        items.append(json_content[item_to_keep['index']])

    with open('items.json', 'w') as fp:
        json.dump(items, fp)
        fp.close()

if __name__ == '__main__':
    extract_items()
    