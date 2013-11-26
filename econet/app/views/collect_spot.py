from django.template import RequestContext
from django.template.defaultfilters import linebreaks
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.utils import simplejson as json
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from accounts.models import User
from app.models import CollectSpot, CheckIn, Item
from app.forms import CollectSpotForm, CheckInDescartItemFormSet

def create(request):
    collect_spot_form = CollectSpotForm(request.POST or None)
    if collect_spot_form.is_valid():
        collect_spot = collect_spot_form.save()
        
        if request.user.pk:
            user = auth.get_user(request)
            collect_spot.collectors.add(user)
            collect_spot.save()
        messages.success(request, u'Salvou o novo Ponto.')
    else:
        messages.error(request, u'Deu Error visse')

    data = {
        'form': collect_spot_form,
    }
    return redirect('home')


def get_json(request):
    data = []
    for cs in CollectSpot.objects.values():
        description = linebreaks(cs.get('description', ''))
        description += '''
        <div class="descart_item_block">
            <a class="btn btn-block btn-success" href="/ioaspkaspaos/saoipokslas">
                Descartar
            </a>
        </div>
        '''
        data.append({ 
            'type': 'FeatureCollection',
            'features': [{ 
                'type': 'Feature',
                'geometry': {
                    'type': 'Point', 
                    'coordinates': [
                        cs.get('longitude'),
                        cs.get('latitude'),
                    ]
                },
                'properties': {
                    'marker-size': 'medium',
                    'marker-color': '#505050',
                    'marker-symbol': 'waste-basket',

                    'title': cs.get('name'),
                    'itens': ','.join(map(lambda x: str(x), Item.objects.filter(collect_spots=cs.get('id')).values_list('id', flat=True))),
                    'description': linebreaks(cs.get('description', '')),
                    'url': reverse('descart_item', args=[cs.get('id')])
                }
            }]
        })

    return HttpResponse(
        json.dumps(data),
        mimetype='application/json'
    )

def descart_item(request, pk):
    user = auth.get_user(request)
    collect_spot = CollectSpot.objects.get(pk=pk)
    check_in = CheckIn.objects.create(
        user=user,
        collect_spot=collect_spot
    )
    checking_itens_formset = CheckInDescartItemFormSet(
        data=request.POST, 
        instance=check_in
    )
    if checking_itens_formset.is_valid():
        checking_itens_formset.save()
        messages.success(request, u'Salvou as coisa.')
    else:
        messages.error(request, u'Deu Error visse')
    return redirect('home')