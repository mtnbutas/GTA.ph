# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from notifications.models import Notification as Notification

#########################################################
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from django.db.models import signals
from signals import notify

from taggit.managers import TaggableManager
###########################################################

class BlogPost(models.Model):
	# bpId = models.AutoField(primary_key = True)
	owner = models.ForeignKey(User, related_name="blog_post")
	title = models.CharField(max_length = 80)
	slug = models.CharField(max_length = 80)
	# content = RichTextUploadingField()
	content = models.TextField()
	coverphoto = models.ImageField(default="/no-img-coverphoto.jpg")
	create_date = models.DateTimeField(auto_now_add = True)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)
	tags = TaggableManager(blank=True)
	
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(BlogPost, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return '/posts/'+str(self.id)+'/'+str(self.slug)+'/'


class Like(models.Model):
	bpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

	def __str__(self):
		return self.liker.first_name + " " + self.liker.last_name + " likes " + self.bpost.title

	def save(self, *args, **kwargs):
		notify.send(self.liker, recipient=self.bpost.owner, target=self.bpost, verb="liked" )
		print self.bpost.owner
		print "this is called at Like"

		super(Like, self).save(*args, **kwargs)


class Dislike(models.Model):
	bpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	disliker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislikes")

	def __str__(self):
		return self.disliker.first_name + " " + self.disliker.last_name + " dislikes " + self.bpost.title

	def save(self, *args, **kwargs):
		notify.send(self.disliker, recipient=self.bpost.owner, target=self.bpost, verb="disliked" )
		print self.bpost.owner
		print "this is called"

		super(Dislike, self).save(*args, **kwargs)


class Comment(models.Model):
	# commentId = models.AutoField(primary_key = True)
	bpId = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
	ownerId = models.ForeignKey(User, related_name="comments")
	content = models.TextField(max_length = 150)
	create_date = models.DateTimeField(auto_now = True)

	def __str__(self):
		user = User.objects.filter(pk=self.ownerId.pk).first()

		return self.content + " by " + user.first_name + " " + user.last_name

	def save(self, *args, **kwargs):
		notify.send(self.ownerId, recipient=self.bpId.owner, target=self.bpId, verb="commented on" )
		print self.bpId.owner
		print "this is called"

		super(Comment, self).save(*args, **kwargs)
		


    # def save(self, *args, **kwargs):
    # 	notify.send(self.user, recipient=self.content_object.author, action_object=self.content_object, target=self, verb="commented on")