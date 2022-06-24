from django.db import models
from django.contrib.auth.models import User


class StdDetails(models.Model):
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    std_fullname = models.CharField(db_column='std_fullName', max_length=200)  # Field name made lowercase.
    std_username = models.CharField(db_column='std_userName', max_length=200)  # Field name made lowercase.
    std_password = models.CharField(max_length=250)
    std_phone = models.CharField(max_length=200)
    std_email = models.CharField(max_length=200)
    std_gender = models.CharField(max_length=50)
    std_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.std_fullName
    
    class Meta:
        managed = False
        db_table = 'std_details'
# Create your models here.


class OrgDetails(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=200)
    org_email = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    org_website = models.CharField(max_length=255)
    org_district = models.CharField(max_length=50)
    org_address = models.CharField(max_length=255)
    org_type = models.CharField(max_length=50)
    cs_username = models.CharField(max_length=150)
    cs_password = models.CharField(max_length=255)
    students_no = models.IntegerField(blank=True, null=True)
    admission_fee = models.IntegerField(blank=True, null=True)
    tution_fee = models.IntegerField(blank=True, null=True)
    acceptance_rate = models.CharField(max_length=10, blank=True, null=True)
    avg_gpa = models.FloatField(blank=True, null=True)
    org_affiliation = models.CharField(max_length=100, blank=True, null=True)
    org_location = models.TextField(blank=True, null=True)
    org_overview = models.TextField(blank=True, null=True)
    org_image = models.TextField(blank=True, null=True)
    is_registered = models.IntegerField()
    contact_email = models.CharField(max_length=200, blank=True, null=True)
    org_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.org_name)

    class Meta:
        managed = False
        db_table = 'org_details'

class News(models.Model):
    news_id = models.IntegerField(primary_key=True)
    news_headline = models.TextField()
    news_content = models.TextField()
    news_post_date = models.DateTimeField(auto_now_add=True, null=True)
    news_image = models.ImageField(upload_to="media", blank=True, null=True)
    def __str__(self):
        return str(self.news_headline)

    class Meta:
        managed = False
        db_table = 'news'


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=255)
    blog_content = models.TextField()
    blog_post_date = models.DateTimeField(auto_now_add=True, null=True)
    blog_image = models.ImageField(upload_to="media", null=True)
    college = models.ForeignKey('OrgDetails', models.DO_NOTHING)
    def __str__(self):
        return str(self.blog_id)

    class Meta:
        managed = False
        db_table = 'blog'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'



class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.IntegerField(default=True)

    class Meta:
        managed = False
        db_table = 'roommember'


    def __str__(self):
        return self.name



class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    appointment_date = models.DateField()
    reason = models.CharField(max_length=255)
    roomname = models.CharField(max_length=255)
    org = models.ForeignKey('OrgDetails', models.DO_NOTHING)
    std = models.ForeignKey('StdDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointment'