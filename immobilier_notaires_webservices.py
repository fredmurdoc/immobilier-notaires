import requests
import json
url_service = 'https://www.immobilier.notaires.fr/pub-services/inotr-www-annonces/v1/annonces?offset=0&page=1&parPage=120&perimetre=0&departements=44&typeBiens=MAI&surfaceMin=80&prixMax=120000&typeTransactions=VENTE,VNI,VAE' 
headers = {'Accept': 'application/json, text/plain, */*',
    'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer' : 'https://www.immobilier.notaires.fr/fr/annonces-immobilieres-liste?page=1&parPage=120&surfaceMin=80&prixMax=120000&departement=44&typeTransaction=VENTE&typeBien=MAI'
}

response = requests.get(url=url_service, headers=headers)
# clé annonceResumeDto
if response.status_code == 200:
    json_resp = response.json()
    with open('tests/test_script.json', 'w') as fp:
        json.dump(json_resp, fp)
else:
    print('error %s ' % response.status_code)