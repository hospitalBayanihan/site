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
from .models import Hospitals, Updates, Requests, Fulfillments

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
    tables = (
        'Hospitals',
        'Update Data',
        'Weekly Supply Tracker',
        'Fulfillment',
    )
    
    table_key = 'appLsmHfyJGeiXffC' # DEV table
    
    atable = Airtable(table_key, 'Hospitals')
    # Fields to skip
  
    #-- Update Hospitals Table --#
    skip = (
        'hospital_id_of_submitting_person',
    )
    hospitals = atable.get_all(view='Raw Hospital Data')  
    for hosp in hospitals:
        hospitals_inputs = Hospitals()   
        hospitals_inputs.id = hosp['id']
        for f in hosp['fields']:
            t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
            
            if t in skip:
                continue
                
            # setattr() modifies object variables identified by t
            setattr(hospitals_inputs, t, hosp['fields'][f])
            
        # Save each hosp data stored in hospitals_inputs to db
        hospitals_inputs.save()
    #-- End Update Hospitals Table --#
    
    #-- Update Updates Table --#
    atable = Airtable(table_key, 'Update Data')
    
    updates = atable.get_all(view='Grid view')  
    for update in updates:
        updates_inputs = Updates()   
        updates_inputs.id = update['id']
        updates_inputs.hospital = Hospitals.objects.get(id=update['fields']['Hospital'][0])
        
        for f in update['fields']:
            t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
            try:
                if t in Updates.to_skip:
                    continue
                setattr(updates_inputs, t, update['fields'][f])
            except:
                continue
        updates_inputs.save()
    #-- End Update Updates Table --#
    
    #-- Update Requests Table --#
    atable = Airtable(table_key, 'Weekly Supply Tracker')
    
    requests = atable.get_all(view='Grid 3')  
    for req in requests:
        requests_inputs = Requests()   
        requests_inputs.id = req['id']
        
        requests_inputs.hospital = Hospitals.objects.get(id=req['fields']['Hospital'][0])
        
        for f in req['fields']:
            t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
            
            if t in Requests.to_include:
                setattr(requests_inputs, t, req['fields'][f])
        
        requests_inputs.save()
    #-- End Update Requests Table --#
    
    
    #-- Update Fulfillments Table --#
    atable = Airtable(table_key, 'Fulfillment')
    
    fulfillments = atable.get_all(view='Grid view')  
    for ful in fulfillments:
        fulfillments_inputs = Fulfillments()   
        fulfillments_inputs.id = ful['id']
        fulfillments_inputs.request = Requests.objects.get(id=ful['fields']['Request Fulfilled'][0])
        
        for f in ful['fields']:
            t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
            try:
                if t in Fulfillments.to_skip:
                    continue
                setattr(fulfillments_inputs, t, ful['fields'][f])
            except:
                continue
        fulfillments_inputs.save()
    #-- End Update Fulfillments Table --#
    
    return render(request, 'main/index.html', {'title': 'Insert Tagline Here'})