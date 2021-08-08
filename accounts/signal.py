from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from buyerseller.models import Customer
from .models import Profile
from allauth.account.signals import user_signed_up


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_signed_up)
def retrieve_social_data(request, user, **kwargs):
    """Signal, that gets extra data from sociallogin and put it to profile."""
    # get the profile where i want to store the extra_data
    profile = Profile(user=user)
    # in this signal I can retrieve the obj from SocialAccount
    data = SocialAccount.objects.filter(user=user, provider='facebook')
    # check if the user has signed up via social media
    if data:
        picture = data[0].get_avatar_url()
        if picture:
            # custom def to save the pic in the profile
            save_image_from_url(model=profile, url=picture)
        profile.save()