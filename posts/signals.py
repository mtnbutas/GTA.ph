from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from models import User
from django.db import models

def my_handler(sender, instance, created, **kwargs):
	notify.send(instance, verb="was saved")
	print "went here"

# post_save.connect(my_handler, sender=User)
# models.signals.posts_save.connect(my_handler, sender=User)