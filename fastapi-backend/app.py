#Ajout de la base de données
import json
from dataclasses import  asdict
from pydantic.dataclasses import dataclass

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel




with open("acteurs.json", "r") as f:  #ouvrir le json file en mode lecture
    acteurs_list = json.load(f)  #lecture du fichier  f et conversion en objet python

    list_acteurs = {k + 1: v for k, v in enumerate(acteurs_list)}


@dataclass
class Acteur():
    id: int
    name: str  #classe model
    bio: str
    picture: str

class ActeurUpdate(BaseModel):
    name: str  # classe model
    bio: str
    picture: str


app = FastAPI()  #Faire appel a fast api

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Persistence des données = sauvegarde permanente
def save_to_file():
    with open("acteurs.json", "w") as f:
        json.dump(list(list_acteurs.values()),f, indent=4)

#Donner le nombre de documents
@app.get("/total_acteurs")
def get_total_acteurs() -> dict:
    return {"total": len(list_acteurs)}


#Endpoint GET

@app.get("/acteurs")
def get_all_acteurs() -> list[Acteur]:
    res = []
    for id in list_acteurs:
        res.append(Acteur(**list_acteurs[id]))  #convertir un dictionnaire en objet grace a l'operateur
    return res

#permet de recuperer un acteur  en fonction de son id
@app.get("/acteur/{id}")
def get_acteur_by_id(id: int = Path(ge=1)) -> Acteur:  #ge veut dire >=
    if id not in list_acteurs:
        raise HTTPException(status_code=404, detail="Cet acteur n'existe pas")
    return Acteur(**list_acteurs[id])

#Creation d'un acteur
@app.post("/acteurs")
def create_acteur (acteur:Acteur) -> Acteur:
    if acteur.id in list_acteurs:
        raise HTTPException(status_code=409, detail="Cet acteur {acteur.id} existe deja")
    list_acteurs[acteur.id] = asdict(acteur) #transforme un object en dictionaire
    save_to_file()
    return acteur

@app.put("/acteur/{id}")
def update_acteur(acteur:ActeurUpdate, id: int=Path(ge=1)) -> Acteur: #ge >=
    if id not in list_acteurs:
        raise HTTPException(status_code=404,detail =f"Cet acteur avec {id} n'existe pas")
    update_data_acteur = Acteur(id = id, name=acteur.name, bio=acteur.bio, picture=acteur.picture)
    list_acteurs[id] = asdict(update_data_acteur)
    save_to_file()
    return update_data_acteur




@app.delete("/acteur/{id}")
def delete_acteur(id: int=Path(ge=1)) -> Acteur:
    if id in list_acteurs:
        acteur = Acteur(**list_acteurs[id])#l'operteur  **convertit un objet en dictionaire
        del list_acteurs[id]
        save_to_file()
        return acteur

    raise  HTTPException (status_code=404, detail="Cet acteur avec {id} n'existe pas")


