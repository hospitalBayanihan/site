from django.db import models    

from airtable import Airtable

# Create your models here.

def getFields():
    # Function to get fields from airtable
    atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals', api_key='keys8DEQxXELZX13q')
    
    # Template entry exists where all columns are filled
    # Unfilled airtable fields do not show as a field
    tmp = atable.match('Hospital Name', 'Template') 
    return (t for t in tmp['fields'])
    
fields = getFields()

class Hospitals(models.Model):
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
