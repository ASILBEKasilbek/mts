# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

@receiver(post_save, sender=Order)
def notify_order(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Yangi buyurtma',
            f'Buyurtma #{instance.id} holati: {instance.status}',
            'admin@uzmat.uz',
            [instance.customer.email],
        )
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'Yangi buyurtma #{instance.id}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=instance.business.phones
        )