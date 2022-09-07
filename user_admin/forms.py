from pyexpat import model
from django import forms
from .models import *
  
class PostForm(forms.ModelForm):
  
    class Meta:
        model = Post
        fields = "__all__"

class EditAdinForm(forms.ModelForm):
    class Meta:
        model   =   Admin
        fields  =   ["first_name", "middle_name", "last_name", "district", "taluka", "address", "mobile_no"]