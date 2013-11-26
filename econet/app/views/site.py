from django.views.generic import TemplateView

from app.forms import (
	CollectSpotForm, CheckInDescartItemFormSet
)

class HomeView(TemplateView):
    template_name = 'site/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['collect_spot_form'] = CollectSpotForm()
        context['descart_item_form'] = CheckInDescartItemFormSet()
        return context
