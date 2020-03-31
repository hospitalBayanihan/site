from django.db import models    

from airtable import Airtable

# Create your models here.
def getFields():
    atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals', api_key='keynI59Mcs9ZgXcXm')
    tmp = atable.match('Hospital Name', 'Template')
    return (t for t in tmp['fields'])
    
fields = getFields()

class Hospitals(models.Model):
    id = models.TextField(primary_key=True)  # AutoField?
    
    to_int = (
        'number_of_active_cases',
        'personnel_count_for_food',
    )
    
    for f in fields:
        t = f.replace(' ', '_').replace('%', '').lower()
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
