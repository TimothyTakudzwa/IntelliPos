from django.db.models.signals import post_save
from django.dispatch import receiver

from merchant.models import MerchantProfile, OperatorProfile, POSTerminal


@receiver(post_save, sender=MerchantProfile)
def initialize_merchant(sender, instance, created, **kwargs): 
    """
    Creates an initial Operator Profile and POS Terminal for
    the newly created merchant
    """
    if created:
        op = OperatorProfile.objects.create(
            merchant=instance,
            user=instance.user
        )
        POSTerminal.objects.create(
            merchant=instance,
            operator_profile=op
        )

