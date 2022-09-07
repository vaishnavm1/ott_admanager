from django import forms
from user_admin.models import Accountant, Marketer

class AccountantLoginForm(forms.Form):
     email      =   forms.EmailField()
     password   =   forms.CharField()

     def clean(self, *args, **kwargs):
         email      =   self.cleaned_date.get("email")
         password   =   self.cleaned_date.get("password")
         pass


class AccountantAuth(forms.ModelForm):
    class Meta:
        model = Accountant
        fields = ["email", "password"]

class MarketerCreateForm(forms.ModelForm):
    class Meta:
        model   =   Marketer
        fields  =   ["first_name", "middle_name", "last_name", "district", "taluka", "address", "email", "mobile_no", "password"]

class EditMarketerForm(forms.ModelForm):
    class Meta:
        model   =   Marketer
        fields  =   ["first_name", "middle_name", "last_name", "district", "taluka", "address", "email", "mobile_no"]