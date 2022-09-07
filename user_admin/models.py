# from distutils.command.upload import upload
from django.db import models
import os
from django.core.exceptions import ValidationError

# Custom Account Model Imports
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import datetime

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', "JPG"]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Post(models.Model):
    name        =   models.CharField(max_length=100)
    post_image  =   models.ImageField(upload_to="post-images")

    
    def __str__(self):
        return self.name



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = "Published")

class PublishedManagerAll(models.Manager):
    def get_queryset(self):
        return super(PublishedManagerAll, self).get_queryset()


class AccountManager(BaseUserManager):
    def create_user(self, mobile_no, email, password=None):
        if not mobile_no:
            raise ValueError("User must have an mobile number")
        user    =   self.model(
                            mobile_no   =   mobile_no,
                            email       =   email
                        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, mobile_no, email):
        user    =   self.create_user(
                            password    =   password,
                            mobile_no   =   mobile_no,
                            email       =   email
                        )
        user.is_admin       =   True
        user.is_staff       =   True
        user.is_superuser   =   True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    username        =   models.CharField(max_length=30)
    email           =   models.EmailField(verbose_name="email", max_length=60,unique=True)
    date_joined     =   models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login      =   models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin        =   models.BooleanField(default=False)
    is_active       =   models.BooleanField(default=True)
    is_staff        =   models.BooleanField(default=False)
    is_superuser    =   models.BooleanField(default=False)

    # Custom Fields
    mobile_no       =   models.CharField(max_length=20, unique = True)

    # full_name       =   models.CharField(max_length=200)
    first_name      =   models.CharField(max_length=100)
    middle_name     =   models.CharField(max_length=100)
    last_name       =   models.CharField(max_length=100)

    district        =   models.CharField(max_length=100)
    taluka          =   models.CharField(max_length=100)
    address         =   models.TextField()


    is_user_admin   =   models.BooleanField(default = False)
    is_marketer     =   models.BooleanField(default = False)
    is_publisher    =   models.BooleanField(default = False)
    is_accountant   =   models.BooleanField(default = False)



    USERNAME_FIELD  =   "email"
    REQUIRED_FIELDS =   ["mobile_no"]

    objects     =   AccountManager()

    def __str__(self):
        return self.mobile_no

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Just created for the sake of it, allocate charts, search and filter functionalities
class Admin(Account):
    pass
    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

class Marketer(Account):
    pass
    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'
    

class Publisher(Account):
    pass

class Accountant(Account):
    pass



# Now custom models other than auth models will be defined...
class Agency(models.Model):
    agency_name                 =   models.CharField(max_length=252, blank=True, null=True)
    agency_mobile_no            =   models.CharField(max_length=30,  unique=True)
    agency_district             =   models.CharField(max_length=252, blank=True, null=True)
    agency_taluka               =   models.CharField(max_length=252, blank=True, null=True)
    agency_address              =   models.TextField(blank=True, null=True)
    agency_whatsapp_mobile_no   =   models.CharField(max_length=30, unique=True)
    agency_email                =   models.EmailField(max_length=60, unique=True)
    agency_gst_number           =   models.CharField(max_length=100, blank=True, null=True)

    marketer_id                 =   models.ForeignKey(Marketer, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.agency_name
    


class Client(models.Model):

    # class Type(models.TextChoices):
    #     AGENCY = "Agency" 
    #     DIRECT_CLIENT = "Direct Client"

    # is_agency               =   models.BooleanField(default=False)
    agency_id               =   models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    # client_type             =   models.CharField(max_length=252, default=Type.DIRECT_CLIENT)


    
    
    company_name         =   models.CharField(max_length=252)

    name                 =   models.CharField(max_length=252)
    district             =   models.CharField(max_length=252)
    taluka               =   models.CharField(max_length=252)
    address              =   models.TextField()
    mobile_no            =   models.CharField(max_length=30, unique = True)

    whatsapp_mobile_no   =   models.CharField(max_length=30, unique = True)
    gst_number           =   models.CharField(max_length=100, null=True, blank=True)

    email                =   models.EmailField(max_length=60, unique = True)

    created     =   models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    is_active       =   models.BooleanField(default = True)
    marketer_id     =   models.ForeignKey(Marketer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
import uuid    

class Order(models.Model):

    class Status(models.TextChoices):
        IN_REVIEW = "In Review"
        FRESH = "Fresh"
        ACCEPTED = "Accepted"
        REJECTED = "Rejected"
    
    class Mop(models.TextChoices):
        CASH = "Cash"
        UPI = "Upi"
        CHEQUE = "Cheque"
        NET_BANKING = "Net-Banking"
        Pdc_Cheque  = "Pdc_Cheque"
        NONE = "None"

    # ORDER_STATUS_CHOICES            =   (("In Review","In Review"), ("Fresh", "Fresh"), ("Accepted", "Accepted"), ("Rejected", "Rejected") )
    # ORDER_MOP_CHOICES               =   (("cash", "Cash"), ("upi", "UPI"), ("cheque", "Cheque"), ("none", "None")) 

    order_id                            =   models.UUIDField(default=uuid.uuid4, editable=False)
    client_id                           =   models.ForeignKey(Client, on_delete = models.CASCADE)
    marketer_id                         =   models.ForeignKey(Marketer, on_delete = models.CASCADE)

    bill_status                         =   models.BooleanField(default = False)

    bill_status_msg                     =   models.CharField(max_length=200, null=True, blank=True)
    
    order_status                        =   models.CharField(max_length=100, choices=Status.choices, default = Status.FRESH)

    discount_requested                  =   models.BooleanField(default=False)
    discount_req_amt                    =   models.IntegerField(default=0)
    
    discount_decision                   =   models.BooleanField(null=True, blank=True)
    discount_alloted_amt                =   models.IntegerField(default=0)

    # Will be null in all cases, expect when someone i.e admin allows discount

    discount_allowed_or_rejected_admin  =   models.ForeignKey(Admin, null=True, blank=True, on_delete = models.CASCADE)

    discounted_new_bill_amt             =   models.IntegerField(null=True, blank=True)

    # GST Section
    gst_relax_requested                 =   models.BooleanField(default=False)
    gst_relax_decision                  =   models.BooleanField(null=True, blank=True)
    gst_allowed_or_rejected_admin       =   models.ForeignKey(Admin, null=True, blank=True, on_delete = models.CASCADE, related_name="gst_allowed_or_rejected_admin")


    
    total_bill_amt                      =   models.IntegerField(default = 0)

    # After discount or not.... Final Bill Paid by the client
    
    final_bill_amt          =   models.IntegerField(default = 0)
    gst_final_bill_amt      =   models.IntegerField(default = 0)

    # Agency discout, only if client has come via an agency
    agency_discount_percent =   models.IntegerField(default=0, null=True, blank=True)
    agency_discount_amt     =   models.IntegerField(default=0, null=True, blank=True)
    agency_discount_given   =   models.BooleanField(default=False)

    b4_agency_discount_bill =   models.IntegerField(default=0, null=True, blank=True)

    mode_of_pay             =   models.CharField(max_length=100, choices=Mop.choices, default = Mop.NONE)
    trans_id                =   models.CharField(max_length=100, null = True, blank = True)
    payment_accepted_datetime=  models.DateTimeField(null=True, blank=True)
    # cheque_image            =   models.ImageField(upload_to="cheque-images", null=True, blank=True)
    # bill_receipt            =   models.ImageField(upload_to="bill-receipts", null=True, blank=True)
    # release_order           =   models.ImageField(upload_to="release-orders", null=True, blank=True)
    signed_release_order    =   models.FileField(upload_to="signed-release-orders", null=True, blank=True)
    created                 =   models.DateTimeField(verbose_name="created", auto_now_add=True)

    def get_discounted_new_bill(self):
        return self.total_bill_amt - self.discount_alloted_amt
    
    



class Advt(models.Model):
    desc                    =   models.TextField(verbose_name="Ad Description")
    ad_image                =   models.ImageField(upload_to="ad-images", null = True, blank = True)
    # type                    =   models.ForeignKey(AdType, on_delete=models.CASCADE)

    order_id                =   models.ForeignKey(Order, on_delete=models.CASCADE)
    ad_amt                  =   models.IntegerField(default=0)
    
    ad_pub_date             =   models.DateTimeField(unique = True, blank=True, null=True)
    ad_pub_actual_date      =   models.DateTimeField(null = True, blank = True)
    is_published            =   models.BooleanField(default = False)


class Type(models.Model):
    title       =   models.CharField(max_length=100)
    created =   models.DateTimeField(auto_now_add=True)
    is_active   =   models.BooleanField(default = True)
    def __str__(self):
        return f'{self.title}'


class Location(models.Model):
    name    =   models.CharField(max_length=100)
    rate    =   models.IntegerField()
    type    =   models.ForeignKey(Type, on_delete=models.CASCADE)
    # Is Location Full Maharashtra
    is_mah  =   models.BooleanField(default=False)

    is_active   =   models.BooleanField(default = True)
    def __str__(self):
        return f'{self.name} | {self.type} INR : {self.rate}'
    

class AdLoc(models.Model):
    location    =   models.ForeignKey(Location, on_delete=models.CASCADE)
    advt_id     =   models.ForeignKey(Advt, on_delete=models.CASCADE, related_name="ad_locs")
    def __str__(self):
        return f'{self.location} | Ad : {self.advt_id.id}'
    

    






#  Iteration 2 Reason : By client (tables modeified : Advt, AdType)
# class AdType(models.Model):
#     title       =   models.CharField(max_length=100)
#     rate        =   models.IntegerField()
#     is_active   =   models.BooleanField(default = True, blank = True, null = True)
#     created =   models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f'{self.title} | {self.rate}'


# class Advt(models.Model):
#     desc                    =   models.TextField(verbose_name="Ad Description")
#     ad_image                =   models.ImageField(upload_to="ad-images", null = True, blank = True)
#     type                    =   models.ForeignKey(AdType, on_delete=models.CASCADE)

#     order_id                =   models.ForeignKey(Order, on_delete=models.CASCADE)
    
#     ad_pub_date             =   models.DateTimeField()
#     ad_pub_actual_date      =   models.DateTimeField(null = True, blank = True)
#     is_published            =   models.BooleanField(default = False)

#  Iteration 1 Reason : By me
# class Advt(models.Model):
#     desc                    =   models.TextField()
#     ad_image                =   models.ImageField(upload_to="ad-images", null = True, blank = True)
#     type                    =   models.ForeignKey(AdType, on_delete=models.CASCADE)
#     marketer_id             =   models.ForeignKey(Marketer, on_delete=models.CASCADE, null=True, blank=True)
#     client_id               =   models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)

#     # order_id                =   models.ForeignKey(Order, on_delete=models.CASCADE, null = True, blank = True)
    
#     ad_pub_date             =   models.DateTimeField()
#     ad_pub_actual_date      =   models.DateTimeField(null = True, blank = True)

