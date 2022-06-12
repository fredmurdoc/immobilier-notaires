import requests

def get_url_ws(departement_code, page, nb_items_per_page):
    return 'https://www.immobilier.notaires.fr/pub-services/inotr-www-annonces/v1/annonces?offset=0&page=%s&parPage=%s&perimetre=0&departements=%s&typeBiens=MAI&surfaceMin=80&prixMax=120000&typeTransactions=VENTE,VNI,VAE' % (page, nb_items_per_page, departement_code)

def download_annonces_du_jour_departement(departement_code):
    page = 1
    nb_per_page = 100
    current_page = page
    has_to_download = True
    items = []
    while has_to_download:
        print("download for dept %s, page %s" % (departement_code, page))
        headers = {'Accept': 'application/json, text/plain, */*',
            'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer' : 'https://www.immobilier.notaires.fr/fr/annonces-immobilieres-liste?page=1&parPage=120&surfaceMin=80&prixMax=120000&departement=%s&typeTransaction=VENTE&typeBien=MAI' % (departement_code)
        }
        url_service = get_url_ws(departement_code, page, nb_per_page)
        response = requests.get(url=url_service, headers=headers)
        # clé annonceResumeDto
        if response.status_code == 200:
            json_resp = response.json()
            items.extend(json_resp['annonceResumeDto'])
            if json_resp["page"] < json_resp["nbPages"]:
                has_to_download = True
                page += 1 
            else:
                has_to_download = False
        else:
            print('error %s ' % response.status_code)
            has_to_download = False
        
    return items    
