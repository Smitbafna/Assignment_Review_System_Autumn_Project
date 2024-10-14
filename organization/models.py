
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# Create your models here.





class CustomUser(AbstractUser):
    enr_no = models.CharField(max_length=20, unique=True)  
    whatsapp_no = models.CharField(max_length=15, blank=True) 
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)  
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)  
    dob = models.DateField(blank=True, null=True)  
    branch = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return self.username  

class ConnectionDetails(models.Model):
    connection_id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(CustomUser, related_name='connections')
    login_start = models.DateTimeField(auto_now_add=True)
    login_end = models.DateTimeField(null=True, blank=True)
    user_agent = models.CharField(max_length=255)
    connection_ip = models.GenericIPAddressField()
    device_name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Connection {self.connection_id} for user {self.user_id}'



class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=255)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_organizations')

    def __str__(self):
        return self.org_name





class OrgMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    org_id_FK= models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    user = models.ManyToManyField(CustomUser,  related_name='org_members')
    is_admin = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_reviewee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.org.org_name}"






class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_members_FK = models.ManyToManyField(OrgMember, related_name='teams')
    team_leader_FK = models.ForeignKey(OrgMember, on_delete=models.CASCADE, related_name='led_teams')
    team_leader_submission_FK = models.ForeignKey('assignment.Submission', on_delete=models.CASCADE, related_name='led_teams')

    def __str__(self):
        return self.team_name

