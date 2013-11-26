from django.template import RequestContext
from django.template.defaultfilters import linebreaks
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import simplejson as json
from django.http import HttpResponse

from app.models import CollectSpot
from app.forms import CollectSpotForm

def create(request):
    collect_spot_form = CollectSpotForm(request.POST or None)
    if collect_spot_form.is_valid():
        collect_spot = collect_spot_form.save()
        
        if request.user:
            collect_spot.collectors.add(request.user)
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
        data.append({ 
            "type": "FeatureCollection",
            "features": [{ 
                "type": "Feature",
                "geometry": {
                    "type": "Point", 
                    "coordinates": [
                        cs.get('longitude'),
                        cs.get('latitude'),
                    ]
                },
                "properties": {
                    "title": cs.get('name'),
                    "description": linebreaks(cs.get('description', '')),
                    'marker-size': 'medium',
                    'marker-color': '#505050',
                    'marker-symbol': 'waste-basket'
                }
            }]
        })

    return HttpResponse(
        json.dumps(data),
        mimetype="application/json"
    )
