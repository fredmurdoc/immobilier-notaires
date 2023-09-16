python main.py
last_file=$(ls -1rt annonces/immobilier_notaires_*.json | tail -1)
cp $last_file ../django_projects/rechercheMaison/data/immo_notaires_annonces.json
