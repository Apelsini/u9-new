from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.contrib.auth.models import Group

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('auth:profile', args=(self.pk,))
    # def is_my_customer(self):
    #     group = Group.objects.filter(id=profile.user.id).all()
    #     for grp in group:
    #         if str(grp).find('customer') >= 0:
    #             groupstring = True
    #         else:
    #             groupstring = False
    #     return True

class Custcode(models.Model):  #data that gives access to customer functions
    codeword = models.CharField(max_length=16)