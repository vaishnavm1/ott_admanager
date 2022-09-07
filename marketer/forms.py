from django import forms
from django.forms import formset_factory
from django.forms import Textarea, TextInput, FileField, Select
from user_admin.models import Marketer, Client, Advt, Order, Agency

from django.utils.translation import gettext_lazy as _


class DateInput(forms.DateInput):
    input_type = "date"

class AddClientForm(forms.ModelForm):
    CHOICES = (("0", "-- Select Client Type --"), ("Agency", "Agency"), ("Direct Client", "Direct Client"))
    # client_type = forms.ChoiceField(widget=forms.Select(attrs={"onchange":"clientTypeChanged(this)", "class":"form-select"}), choices=CHOICES)
    client_type = forms.ChoiceField(widget=forms.Select(attrs={"onchange":"clientTypeChanged(this)", "class":"form-select"}), choices=CHOICES)

    class Meta:
        model   =   Client
        # fields  =   ["client_type", "name", "company_name", "whatsapp_mbno", "gst_number", "district", "taluka", "address", "mbno", "email",]
        fields  =   "__all__"
        exclude = ["marketer_id", "is_active"]
        widgets =   {
                    "agency_address": Textarea(attrs={"cols":20, "rows":5}),
                    "client_address": Textarea(attrs={"cols":20, "rows":5}),
                    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = True
        for field in self.fields.values():
            if field.label == None:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class AddAgencyForm(forms.ModelForm):

    class Meta:
        model   =   Agency
        fields  =   "__all__"
        widgets =   {
                    "agency_address": Textarea(attrs={"cols":20, "rows":5}),
                    "agency_mobile_no": TextInput(attrs={"type":"number"}),
                    "agency_whatsapp_mobile_no": TextInput(attrs={"type":"number"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        


class AddAdForm(forms.ModelForm):
    # ad_pub_date     =   forms.DateField(widget = DateInput)
    ad_image        =   forms.FileField(required = False, widget= forms.FileInput(attrs={"accept":"image/*"}) )
    # ad_image    =   forms.FileField()
    class Meta:
        model   =   Advt
        # fields  =   [ "desc", "ad_image", "type"]
        fields  =   [ "desc", "ad_image"]
        widgets =   {
                    "desc": Textarea(attrs={"cols":40, "rows":10,"required":"true"}),
                    }
class UpdateAdForm(forms.ModelForm):
    # ad_pub_date     =   forms.DateField(widget = DateInput)
    # ad_image        =   forms.FileField(required = False, widget= forms.FileInput(attrs={"accept":"image/*"}) )
    # ad_image    =   forms.FileField()
    class Meta:
        model   =   Advt
        fields  =   [ "desc", "ad_image"]
        widgets =   {
                    "desc": Textarea(attrs={"cols":40, "rows":10,"required":"true"}),
                    # "type": Select(attrs={"disabled": "true", "required":"false"})
                    }

class SaveOrderUpdateForm(forms.ModelForm):
    class Meta:
        model   =   Order
        fields  =   ["mode_of_pay", "trans_id"]
        widgets =   {
            "mode_of_pay": Select(attrs={"class":"form-select",  "id":"modeOfPayment", "disabled":"true",}),
            "trans_id": TextInput(attrs={"class":"form-control", "id":"transaction_id", "disabled":"true"})
        }

class UpdateRoForm(forms.ModelForm):
    signed_release_order    =   forms.FileField(required = True, widget= forms.FileInput(attrs={"accept":"image/*"}) )
    class Meta:
        model   =   Order
        fields  =   ["signed_release_order",]
        
        
# AddAdFormset = formset_factory(AddAdForm, extra=2)