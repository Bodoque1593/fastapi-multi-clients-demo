import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ActorForm


FASTAPI_URL = "http://127.0.0.1:8000"


def actor_list(request):

    id_param = (request.GET.get("id") or "").strip()

    try:
        if id_param:
            # Filtrer par ID -> /acteur/{id}
            actor_id = int(id_param)
            r = requests.get(f"{FASTAPI_URL}/acteur/{actor_id}")
            if r.status_code == 200:
                acteurs = [r.json()]
            else:
                acteurs = []  # introuvable
        else:
            # Sin filtro -> todos
            r = requests.get(f"{FASTAPI_URL}/acteurs")
            r.raise_for_status()
            acteurs = r.json()

    except Exception as e:
        acteurs = []
        messages.error(request, f"Erreur lors de la récupération: {e}")

    return render(
        request,
        "actors/actor_list.html",
        {
            "acteurs": acteurs,
            "id": id_param,  # mantiene el valor en el input
        },
    )




# Detail

def actor_detail(request, id):
    """
    GET /acteur/{id}
    """
    try:
        r = requests.get(f"{FASTAPI_URL}/acteur/{id}")
        if r.status_code == 404:
            messages.warning(request, f"Acteur {id} introuvable.")
            return redirect("actors:list")
        r.raise_for_status()
        acteur = r.json()
    except Exception as e:
        messages.error(request, f"Erreur: {e}")
        return redirect("actors:list")

    return render(request, "actors/actor_detail.html", {"acteur": acteur})



# Création

def actor_create(request):
    """
    POST -> /acteurs  (corps JSON)
    """
    if request.method == "POST":
        form = ActorForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                r = requests.post(f"{FASTAPI_URL}/acteurs", json=payload)
                if r.status_code == 409:
                    messages.error(request, "Conflit: cet ID existe déjà.")
                else:
                    r.raise_for_status()
                    messages.success(request, "Acteur créé avec succès.")
                    return redirect("actors:list")
            except Exception as e:
                messages.error(request, f"Erreur: {e}")
    else:
        form = ActorForm()

    return render(request, "actors/actor_form.html", {"form": form, "mode": "create"})



# Mise a jour

def actor_update(request, id):

    # précharger l'acteur
    try:
        base = requests.get(f"{FASTAPI_URL}/acteur/{id}")
        if base.status_code == 404:
            messages.warning(request, f"Acteur {id} introuvable.")
            return redirect("actors:list")
        base.raise_for_status()
        data = base.json()
    except Exception as e:
        messages.error(request, f"Erreur: {e}")
        return redirect("actors:list")

    if request.method == "POST":
        form = ActorForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            payload = {
                "name": cleaned["name"],
                "bio": cleaned["bio"],
                "picture": cleaned["picture"],
            }
            try:
                r = requests.put(f"{FASTAPI_URL}/acteur/{id}", json=payload)
                r.raise_for_status()
                messages.success(request, "Acteur modifié avec succès.")
                return redirect("actors:detail", id=id)
            except Exception as e:
                messages.error(request, f"Erreur: {e}")
    else:
        # pré-remplir
        form = ActorForm(initial={
            "id": data.get("id"),
            "name": data.get("name"),
            "bio": data.get("bio"),
            "picture": data.get("picture"),
        })

    return render(request, "actors/actor_form.html", {"form": form, "mode": "update", "act_id": id})



# Suppression

def actor_delete(request, id):

    if request.method == "POST":
        try:
            r = requests.delete(f"{FASTAPI_URL}/acteur/{id}")
            if r.status_code == 404:
                messages.warning(request, "Cet acteur n'existe pas.")
            else:
                r.raise_for_status()
                messages.success(request, "Acteur supprimé.")
        except Exception as e:
            messages.error(request, f"Erreur: {e}")
        return redirect("actors:list")

    # page de confirmation
    try:
        one = requests.get(f"{FASTAPI_URL}/acteur/{id}").json()
    except Exception:
        one = None
    return render(request, "actors/actor_confirm_delete.html", {"acteur": one, "act_id": id})
