import os
from django.core.files.storage import default_storage
from django.db.models import FileField

from allauth.account.models import EmailAddress


def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """

    try:
        instance = kwargs['instance']
        if os.path.exists(instance.photo.path) and instance.is_3d == False:
            try:
                default_storage.delete(instance.photo.path)
            except:
                pass
    except:
        pass


def create_user_email(sender, instance, **kwargs):
    if instance.is_manager:

        email_address_object = EmailAddress.objects.filter(user=instance).first()
        if email_address_object:
            email_address_object.email = instance.email
        else:
            email_address_object = EmailAddress(
                user=instance, email=instance.email, verified=True, primary=True)

        email_address_object.save()
