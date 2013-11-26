from django import forms

from app.models import Bounty, CollectSpot

class BountyForm(forms.ModelForm):
    class Meta:
        model = Bounty
        exclude = ['users']

class CollectSpotForm(forms.ModelForm):
    class Meta:
        model = CollectSpot
        exclude = ['collectors']
        widgets = {
        	'latitude': forms.HiddenInput(),
        	'longitude': forms.HiddenInput(),
        }