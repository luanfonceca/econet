from django import forms
from django.forms.models import (
    inlineformset_factory, BaseInlineFormSet
)

from app.models import (
    Bounty, CollectSpot, Item, CheckIn, DescartedItem
)

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

    def clean_description(self):
        if 'accepted_itens' in self.changed_data:
            itens_description = map(
                lambda x: 'Item Aceito: %s' % x,
                Item.objects.filter(
                    pk__in=self.data.getlist('accepted_itens')
                ).values_list('name', flat=True)
            )
        return "%s\n\n%s" % (
            self.cleaned_data['description'], 
            '\n'.join(itens_description)
        )


class DescartItemForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        # fields = ['itens']
    

class DescartItemFormSet(BaseInlineFormSet):
    def save(self, user=None, commit=True):        
        if user:
            self.instance.updated_by = user
            if not self.instance.pk:
                self.instance.created_by = self.instance.updated_by
        return super(DescartItemFormSet, self).save(commit=commit)

CheckInDescartItemFormSet = inlineformset_factory(
    parent_model=CheckIn, 
    model=DescartedItem,
    form=DescartItemForm,
    formset=DescartItemFormSet,
    can_delete=False,
    extra=1, 
)