from django.db import models    

from airtable import Airtable

# Create your models here.

class Hospitals(models.Model):
    id = models.TextField(primary_key=True)  # AutoField?
    
    atable = Airtable('appLsmHfyJGeiXffC', 'Hospitals')
    tmp = atable.match('Name', 'Template - Template') 
    
    fields = (t for t in tmp['fields'])
    
    # List of fields that will be integer fields
    to_int = (
        'number_of_active_cases',
        'personnel_count_for_food',
    )
    
    for f in fields:
        # Replace spaces with '_' and remove '%' symbols
        t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
        
        # locals()[t] creates a variable with name contained in string t
        if t.find('weekly_volume') > -1 or t in to_int:
            locals()[t] = models.IntegerField(blank=True, null=True)
        else:
            locals()[t] = models.TextField(blank=True, null=True)
    
    def __str__(self):
        tmp = ""
        for f in self.fields:
            tmp += f + ' : ' + getattr(self, f) + '\n'
        return tmp
    
    class Meta:
        db_table = 'Hospitals'
        
class Updates(models.Model):
    id = models.TextField(primary_key=True)  # AutoField?
    hospital = models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    
    atable = Airtable('appLsmHfyJGeiXffC', 'Update Data')
    tmp = atable.match('Hospital', 'Template - Template') 
    
    fields = (t for t in tmp['fields'])
    
    # List of fields that will be integer fields
    to_int = (
        'number_of_active_cases',
        'average_personnel_count',
    )
    
    to_skip = (
        'hospital',
    )
    
    for f in fields:
        # Replace spaces with '_' and remove '%' symbols
        t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
        
        # locals()[t] creates a variable with name contained in string t
        if t in to_skip:
            continue
        elif t.find('weekly_volume') > -1 or t in to_int:
            locals()[t] = models.IntegerField(blank=True, null=True)
        else:
            locals()[t] = models.TextField(blank=True, null=True)
    
    def __str__(self):
        tmp = ""
        for f in self.fields:
            tmp += f + ' : ' + getattr(self, f) + '\n'
        return tmp
    
    class Meta:
        db_table = 'Updates'
        
class Requests(models.Model):
    id = models.TextField(primary_key=True)  # AutoField?
    hospital = models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    
    atable = Airtable('appLsmHfyJGeiXffC', 'Weekly Supply Tracker')
    tmp = atable.match('Hospital', 'Template - Template') 
    
    fields = (t for t in tmp['fields'])
    
    to_include = (
        'covered_week',
        'request_status',
        'deadline',
        'overdue',
    )
    
    for f in fields:
        # Replace spaces with '_' and remove '%' symbols
        t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
        
        # locals()[t] creates a variable with name contained in string t
        if t in to_include:
            locals()[t] = models.TextField(blank=True, null=True)
    
    def __str__(self):
        tmp = ""
        for f in self.fields:
            tmp += f + ' : ' + getattr(self, f) + '\n'
        return tmp
    
    class Meta:
        db_table = 'Requests'

class Fulfillments(models.Model):
    id = models.TextField(primary_key=True)  # AutoField?
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    
    atable = Airtable('appLsmHfyJGeiXffC', 'Fulfillment')
    tmp = atable.match('Donated by', 'Template') 
    
    fields = (t for t in tmp['fields'])
    
    # List of fields that will be integer fields
    to_int = (
        'number_of_active_cases',
        'personnel_count_for_food',
    )
    
    to_skip = (
        'hospital',
        'request_fulfilled',
    )
    
    for f in fields:
        # Replace spaces with '_' and remove '%' symbols
        t = f.replace(' ', '_').replace('%', '').replace('?', '').lower()
        
        # locals()[t] creates a variable with name contained in string t
        if t in to_skip:
            continue
        if t.find('provided') > -1 or t in to_int:
            locals()[t] = models.IntegerField(blank=True, null=True)
        else:
            locals()[t] = models.TextField(blank=True, null=True)
    
    def __str__(self):
        tmp = ""
        for f in self.fields:
            tmp += f + ' : ' + getattr(self, f) + '\n'
        return tmp
    
    class Meta:
        db_table = 'Fulfillments'
        