from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile
from base.functions import get_theme


@receiver(post_save, sender=User)
def Profile_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def Profile_save(sender, instance, **kwargs):
    instance.profile.save()
    
    theme = get_theme(context={"user":instance})

    instance.profile.theme=theme

    instance.profile.save()

    
