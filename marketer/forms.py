from django import forms
from django.forms import formset_factory
from django.forms import Textarea, TextInput, FileField
from user_admin.models import Marketer, Client, Advt

from django.utils.translation import gettext_lazy as _


class DateInput(forms.DateInput):
    input_type = "date"

class AddClientForm(forms.ModelForm):
    class Meta:
        model   =   Client
        fields  =   ["name", "district", "taluka", "address", "mbno", "email",]

class AddAdForm(forms.ModelForm):
    # ad_pub_date     =   forms.DateField(widget = DateInput)
    ad_image        =   forms.FileField(required = False, widget= forms.FileInput(attrs={"accept":"image/*"}) )
    # ad_image    =   forms.FileField()
    class Meta:
        model   =   Advt
        fields  =   [ "desc", "ad_image", "type"]
        widgets =   {
                    "desc": Textarea(attrs={"cols":40, "rows":10,"required":"true"}),
                    }

# AddAdFormset = formset_factory(AddAdForm, extra=2)