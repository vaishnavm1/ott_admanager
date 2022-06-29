from django.contrib import admin
# from .models import Post
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    #removed email from fields
    class Meta:
        model = Account
        fields = ('mobile_no', 'email', "first_name", "middle_name", "last_name", "district", "taluka", "address" )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    #Added email from fields 
    class Meta:
        model = Account
        fields = ('password', 'mobile_no', 'is_active', 'is_admin', 'email', "first_name", "middle_name", "last_name", "district", "taluka", "address")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AccountAdmin(UserAdmin):
    # list_display = ("email", "username", "date_joined","last_login","is_admin","is_staff")
    # list_display = ( "username", "date_joined","last_login","is_admin","is_staff", "mobile_no")
    list_display = ( "email", "mobile_no", "username", "first_name", "middle_name", "last_name", "district", "taluka", "address", "date_joined","last_login","is_admin","is_staff")
    # search_fields = ("email", "username",)
    search_fields = ( "mobile_no", "email")
    readonly_fields = ("date_joined","last_login")
    filter_horizontal = ()
    # list_filter = ("first_name", "middle_name", "last_name", "district", "taluka", "address")
    ordering = ('mobile_no', "email")
    fieldsets = (
            (None, {'fields' : ('password', "mobile_no", "username" , "email")}),
                ('Personal Info', {"fields": ("first_name", "middle_name", "last_name", "district", "taluka", "address")}),
                ("Permissions", {"fields": ("is_admin", "is_staff","is_superuser", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )
    add_fieldsets =   (
                (None, {'fields' : ("email", "mobile_no",  'password1', 'password2', "first_name", "middle_name", "last_name", "district", "taluka", "address", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )
    #both fieldset and add_fieldsets had email field which is removed now... and below as well for fiedsets at 2nd pos and 1st pos at add_field



class L2AdminAccount(UserAdmin):
    list_display = ("date_joined","last_login","is_admin","is_staff", "mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address")
    search_fields = ("email", "mobile_no")
    readonly_fields = ("date_joined","last_login")
    filter_horizontal = ()
    list_filter = ()
    ordering = ('mobile_no', "email")
    fieldsets = (
            (None, {'fields' : ('password', "mobile_no", "email")}),
                ('Personal Info', {"fields": ("first_name", "middle_name", "last_name", "district", "taluka", "address")}),
                ("Permissions", {"fields": ("is_admin", "is_staff","is_superuser", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )
    add_fieldsets = UserAdmin.add_fieldsets +  (
                (None, {'fields' : ("mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )

class MarketerAccount(UserAdmin):
    list_display = ("date_joined","last_login","is_admin","is_staff", "mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address")
    search_fields = ("email", "mobile_no")
    readonly_fields = ("date_joined","last_login")
    filter_horizontal = ()
    list_filter = ()
    ordering = ('mobile_no', "email")
    fieldsets = (
            (None, {'fields' : ('password', "mobile_no", "email")}),
                ('Personal Info', {"fields": ("first_name", "middle_name", "last_name", "district", "taluka", "address")}),
                ("Permissions", {"fields": ("is_admin", "is_staff","is_superuser", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )
    add_fieldsets = UserAdmin.add_fieldsets +  (
                (None, {'fields' : ("mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )

class PublisherAccount(UserAdmin):
    list_display = ("date_joined","last_login","is_admin","is_staff", "mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address")
    search_fields = ("email", "mobile_no")
    readonly_fields = ("date_joined","last_login")
    filter_horizontal = ()
    list_filter = ()
    ordering = ('mobile_no', "email")
    fieldsets = (
            (None, {'fields' : ('password', "mobile_no", "email")}),
                ('Personal Info', {"fields": ("first_name", "middle_name", "last_name", "district", "taluka", "address")}),
                ("Permissions", {"fields": ("is_admin", "is_staff","is_superuser", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )
    add_fieldsets = UserAdmin.add_fieldsets +  (
                (None, {'fields' : ("mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )


class AccountantAccount(UserAdmin):
    list_display = ("date_joined","last_login","is_admin","is_staff", "mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address")
    search_fields = ("email", "mobile_no")
    readonly_fields = ("date_joined","last_login")
    filter_horizontal = ()
    list_filter = ()
    ordering = ('mobile_no', "email")
    fieldsets = (
            (None, {'fields' : ('password', "mobile_no", "email")}),
                ('Personal Info', {"fields": ("first_name", "middle_name", "last_name", "district", "taluka", "address")}),
                ("Permissions", {"fields": ("is_admin", "is_staff","is_superuser", "is_active", "is_user_admin", "is_marketer", "is_publisher", "is_accountant" )}),
            )
    add_fieldsets = UserAdmin.add_fieldsets +  (
                (None, {'fields' : ("mobile_no", "email", "first_name", "middle_name", "last_name", "district", "taluka", "address", "is_user_admin", "is_marketer", "is_publisher", "is_accountant")}),
            )



admin.site.register(Account, AccountAdmin)
admin.site.register(Post)
admin.site.register(Admin, L2AdminAccount)

admin.site.register(Marketer, MarketerAccount)
admin.site.register(Publisher, PublisherAccount)
admin.site.register(Accountant, AccountantAccount)

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "client_id", "bill_status", "total_bill_amt", "order_status", "signed_release_order"]
    list_filter = ("client_id", )

class AdvtAdmin(admin.ModelAdmin):
    list_display = ["id", "is_published", "order_id"]
    list_filter = ("is_published", )


admin.site.register(Order, OrderAdmin)
admin.site.register(Client)
admin.site.register(Advt, AdvtAdmin)
admin.site.register(AdType)
