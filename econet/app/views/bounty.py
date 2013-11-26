from django.views.generic import ListView, DetailView, CreateView, \
                                 DeleteView, UpdateView

from app.models import Bounty 
from app.forms import BountyForm

class BountyView(object):
    model = Bounty
    form_class = BountyForm

    def get_template_names(self):
        """Nest templates within bounty directory."""
        tpl = super(BountyView, self).get_template_names()[0]
        app = self.model._meta.app_label
        mdl = 'bounty'
        self.template_name = tpl.replace(app, '{0}'.format(mdl))
        return [self.template_name]


class BountyDateView(BountyView):
    date_field = 'created_at'
    

class BountyBaseListView(BountyView):
    paginate_by = 10

class BountyCreateView(BountyView, CreateView):
    pass

class BountyDeleteView(BountyView, DeleteView):

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('app_bounty_list')


class BountyDetailView(BountyView, DetailView):
    pass


class BountyListView(BountyBaseListView, ListView):
    pass


class BountyUpdateView(BountyView, UpdateView):
    pass

