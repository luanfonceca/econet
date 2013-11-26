from django.views.generic import TemplateView

from app.forms import CollectSpotForm

class HomeView(TemplateView):
    template_name = 'site/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = CollectSpotForm()
        return context
