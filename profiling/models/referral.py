from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiling.utils import generate_ref_code

User = get_user_model()


class ReferralSystem(models.Model):
    user = models.OneToOneField(
        User, related_name='refer_earn_customer',
        on_delete=models.CASCADE, null=True)

    code = models.CharField(max_length=6, blank=True)
    referred_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True,
        null=True, related_name="ref_by")

    my_referred_users = models.ManyToManyField(
        User, blank=True, related_name="my_referred_users")

    invites = models.IntegerField(default=0)

    class Meta:
        app_label = 'profiling'

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = str(self.user)+str(code)
        super(ReferralSystem, self).save(*args, **kwargs)

    @property
    def get_referred_profiles(self):
        qs = ReferralSystem.objects.select_related('referred_by')
        my_recoms = []
        for r_s in qs:
            if r_s.referred_by == self.user:
                my_recoms.append(r_s.user)
        return my_recoms


@receiver(post_save, sender=User)
def create_referral_system(sender, instance, created, **kwargs):
    if created:
        ReferralSystem.objects.create(user=instance)
