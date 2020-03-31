from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Hospitals

from airtable import Airtable

def main(request):

    if request.POST:
        hospitals_inputs = Hospitals(
                hospital_name = request.POST['hospital_name'],
                supplies_n95_mask = request.POST['n95_weekly_volume'],
                )
        #writes the data to the db.sqlite
        hospitals_inputs.save()

    return render(request, 'main/index.html', {'title': 'Insert Tagline Here'})
# Create your views here.

def refresh(request):
    atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals', api_key='keynI59Mcs9ZgXcXm')
    
    skip = (
        'hospital_id_of_submitting_person',
    )
    
    hospitals = atable.get_all(view='Raw Hospital Data')
    
    for hosp in hospitals:
        hospitals_inputs = Hospitals()   
        hospitals_inputs.id = hosp['id']
        for f in hosp['fields']:
            t = f.replace(' ', '_').replace('%', '').lower()
            if t in skip:
                continue
            setattr(hospitals_inputs, t, hosp['fields'][f])
        print(hospitals_inputs)
        hospitals_inputs.save()

    return render(request, 'main/index.html', {'title': 'Insert Tagline Here'})