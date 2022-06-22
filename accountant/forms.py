from django import forms
from user_admin.models import Accountant

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

