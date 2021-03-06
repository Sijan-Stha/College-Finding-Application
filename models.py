# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


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


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.TextField()
    blog_content = models.TextField()
    blog_post_date = models.DateTimeField()
    blog_image = models.TextField(blank=True, null=True)
    college = models.ForeignKey('OrgDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'blog'


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_title = models.CharField(max_length=200)
    course_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'courses'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_headline = models.TextField()
    news_content = models.TextField()
    news_post_date = models.DateTimeField()
    news_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


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

    class Meta:
        managed = False
        db_table = 'org_details'
        unique_together = (('org_email', 'cs_username'),)


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roommember'


class StdDetails(models.Model):
    std_fullname = models.CharField(db_column='std_fullName', max_length=200)  # Field name made lowercase.
    std_username = models.CharField(db_column='std_userName', max_length=200)  # Field name made lowercase.
    std_password = models.CharField(max_length=250)
    std_phone = models.CharField(max_length=200)
    std_email = models.CharField(max_length=200)
    std_gender = models.CharField(max_length=50)
    std_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'std_details'
