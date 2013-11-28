from django.views.generic import TemplateView

from accounts.models import User
from app.models import Item, Timeline
from app.forms import (
	CollectSpotForm, CheckInDescartItemFormSet
)

class HomeView(TemplateView):
    template_name = 'site/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['collect_spot_form'] = CollectSpotForm()
        context['descart_item_form'] = CheckInDescartItemFormSet()
        context['avalible_itens'] = Item.objects.all()
        context['ranked_users'] = User.objects.order_by('-earned_points')[:10]
        context['timeline'] = Timeline.objects.all()[:5]
        return context