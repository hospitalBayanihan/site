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
    # View to update sqlite db with airtable data

    atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals', api_key='keys8DEQxXELZX13q')

    # Fields to skip
    skip = (
        'hospital_id_of_submitting_person',
    )
    
    # hospitals contains a list of each row in from airtable
    hospitals = atable.get_all(view='Raw Hospital Data')
    
    for hosp in hospitals:
        hospitals_inputs = Hospitals()   
        hospitals_inputs.id = hosp['id']
        for f in hosp['fields']:
            # hosp['fields'] is a dictionary where keys are fields of airtable and values have the corresponding value
            t = f.replace(' ', '_').replace('%', '').lower()
            
            if t in skip:
                continue
                
            # setattr() modifies object variables identified by t
            setattr(hospitals_inputs, t, hosp['fields'][f])
            
        # Save each hosp data stored in hospitals_inputs to db
        hospitals_inputs.save()

    return render(request, 'main/index.html', {'title': 'Insert Tagline Here'})