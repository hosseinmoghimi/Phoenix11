from accounting.forms import forms,AddInvoiceForm
 
 
class AddVehicleForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
 

class AddMaintenanceInvoiceForm(AddInvoiceForm):
    kilometer=forms.IntegerField(  required=False)
    service_man_id=forms.IntegerField(required=True)
    vehicle_id=forms.IntegerField(required=True)
    maintenance_type=forms.CharField(max_length=100, required=True)
    