import immobilier_notaires_webservices
import json
from datetime import datetime

if __name__ == '__main__':
    items = []
    for dept in ['44', '35', '49', '56', '53']:
        items.extend(immobilier_notaires_webservices.download_annonces_du_jour_departement(dept))

    with open('annonces/immobilier_notaires_%s.json' % (datetime.now().strftime('%Y%m%d')), 'w') as fp:
        json.dump(items, fp)
