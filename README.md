1. API 
L’API a été développée avec FASTAPI, elle fournit des endpoints CRUD pour gérer les données (création, lecture, mise à 
jour, suppression).

• Les codes de statut (200, 201, 404, etc.), 
• La validation des champs obligatoires.


2. Choix des technologies utilisées 
• FastAPI:  backend principal et gestion de la base de données 
• Django + Django REST Framework: service rapide pour tester et consommer 
l’API. 
• HTML, CSS, JavaScript : interface utilisateur simple et responsive. 
• Symfony : interface utilisateur simple et responsive.

3.  Architecture et interactions 
• FastAPI est le cœur du système, l’API consommée par les clients. 
• HTML, CSS, JavaScript , envoie des requêtes HTTP vers l’API. 
• Synfony consomme L’API  via HTTP 
• Django consomme également l’API via HTTP.
