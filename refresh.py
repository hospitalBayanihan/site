from django.db import models 
from airtable import Airtable


atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals', api_key='keys8DEQxXELZX13q')

def getFields():
    # Function to get fields from airtable
    
    # Template entry exists where all columns are filled
    tmp = atable.match('Hospital Name', 'Template') 
    return (t for t in tmp['fields'])

class Hospitals(models.Model):
        
    fields = getFields()
    
    id = models.TextField(primary_key=True)  # AutoField?
    
    # List of fields that will be integer fields
    to_int = (
        'number_of_active_cases',
        'personnel_count_for_food',
    )
    
    for f in fields:
        # Replace spaces with '_' and remove '%' symbols
        t = f.replace(' ', '_').replace('%', '').lower()
        
        # locals()[t] creates a variable with name contained in string t
        if t.find('weekly_volume') > -1 or t in to_int:
            locals()[t] = models.IntegerField(blank=True, null=True)
        else:
            locals()[t] = models.TextField(blank=True, null=True)
    
    def __str__(self):
        tmp = ""
        for f in fields:
            tmp += f + ' : ' + getattr(self, f) + '\n'
        return tmp
    
    class Meta:
        db_table = 'Hospitals'

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