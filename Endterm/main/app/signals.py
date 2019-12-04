from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Article
from utils.upload import article_delete_path


@receiver(post_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    # instance.documents.count() > 0:
    if instance.document:
        article_delete_path(document=instance.document)