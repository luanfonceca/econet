#!/usr/bin/env python
# encoding: utf-8

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
    for cs in CollectSpot.objects.all():
        description = '''
        <blockquote>%(description)s</blockquote>
        <strong>Local</strong>: %(local)s

        <br><br>
        <strong>Itens aceitos</strong>: %(itens)s
        ''' % {
            'description': linebreaks(cs.description or u'Sem descrição definida.'),
            'local': cs.local or u'Sem local definido',
            'itens': ', '.join(map(
                lambda x: x.name,
                cs.accepted_itens.all()
            )) or u'Nenhum Item.'
        }

        itens = Item.objects.filter(
            collect_spots=cs.id
        ).values('id', 'name')

        def join_and_map(map_key, objects, join_key=','):
            def map_func(x):
                data = x.get(map_key)
                if not isinstance(data, basestring):
                    data = str(data)
                return data
            return str(join_key).join(
                map(map_func, objects)
            )
        data.append({ 
            'type': 'FeatureCollection',
            'features': [{ 
                'type': 'Feature',
                'geometry': {
                    'type': 'Point', 
                    'coordinates': [
                        cs.longitude,
                        cs.latitude,
                    ]
                },
                'properties': {
                    'marker-size': 'medium',
                    'marker-color': '#505050',
                    'marker-symbol': 'waste-basket',

                    'title': cs.name,
                    'local': cs.local,
                    'itens': join_and_map('id', itens),
                    'itens_name': join_and_map('name', itens),
                    'description': description,
                    'url': reverse('descart_item', args=[cs.id])
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