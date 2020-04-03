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

def main(request):

    if request.POST:
        hospitals_inputs = Hospitals(
                hospital_name = request.POST['hospital_name'],
                n95_weekly_volume = request.POST['n95_weekly_volume']
                )
        #writes the data to the db.sqlite
        hospitals_inputs.save()


    hosp_all_entries = Hospitals.objects.all()
    print (hosp_all_entries)
    print (hosp_all_entries[0].hospital_name)

    content = {
        'title': 'Insert Tagline Here',
        'hosp_all' : Hospitals.objects.all()
    }

    return render(request, 'main/index.html', content)
# Create your views here.
