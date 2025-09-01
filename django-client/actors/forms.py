from django import forms

class ActorForm(forms.Form):
    # Id vient de l’utilisateur
    id = forms.IntegerField(min_value=1, label="ID")
    name = forms.CharField(max_length=100, label="Nom")
    bio = forms.CharField(widget=forms.Textarea, label="Biographie")
    picture = forms.URLField(label="Photo (URL)")
