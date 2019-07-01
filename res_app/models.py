from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=256)
    role = models.CharField(max_length=256)
    daily_rate = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Name: {self.name}, Role: {self.role}"

class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete='CASCADE')

    # Add any additional attributes you want
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfileInfo.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.
