# wikipemi

Un crawler simple pour télécharger des pages Wikipédia aléatoires, leurs liens internes et la feuille de style CSS associée.

## Installation

1. Clone ce dépôt.
2. Installe les dépendances Python :

   ```sh
   pip install -r requirements.txt
   ```

3. Assure-toi d’avoir Google Chrome installé.

## Utilisation

Lance le script principal :

```sh
python main.py
```

Les pages seront sauvegardées dans le dossier `wikipedia_fr` (modifiable dans [`config.py`](c:/Users/antoi/Documents/github/wikipemi/config.py)).

## Configuration

Modifie les paramètres dans [`config.py`](c:/Users/antoi/Documents/github/wikipemi/config.py) :

- `language` : langue de Wikipédia (ex : `"fr"`, `"en"`, etc.)
- `MAX_PAGES` : nombre maximum de pages à crawler (`0` = illimité)
- `PAUSE_PER_PAGE` : pause (en secondes) entre chaque page

## Dépendances

- requests
- beautifulsoup4
- selenium
- webdriver-manager

## Auteurs

- afon30

---
Projet éducatif, le but est simplement de télécharger en local un wikipedia