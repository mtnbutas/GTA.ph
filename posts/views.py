# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from accounts.models import User
from accounts.models import Profile
from .models import BlogPost
from .models import Comment
from .models import Like
from .models import Dislike

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.core.urlresolvers import reverse
from django.views import generic

from . import forms

from django.db.models import F

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

####################################

class CkEditorFormView(generic.FormView):
	form_class = forms.CkEditorForm
	template_name = 'form.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(CkEditorFormView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		blogpost = form.save(commit=False)
		print self.request.user.id
		blogpost.owner = self.request.user
		print blogpost.owner
		blogpost.save()
		form.save_m2m()

		return redirect(reverse('post-detail', kwargs={'post_id': blogpost.pk, 'slug':blogpost.slug}))

	def get_success_url(self):
		print "why if here?"
		return reverse('ckeditor-form')

ckeditor_form_view = CkEditorFormView.as_view()

###############

def post_edit(request, post_id):
	blogpost = get_object_or_404(BlogPost, pk=post_id)

	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = forms.CkEditorEditForm(request.POST, request.FILES, instance=blogpost)
		if form.is_valid():
			blogpost = form.save(commit=False)
			blogpost.save()
			form.save_m2m()
			return redirect(
				reverse('post-detail', kwargs={'post_id': blogpost.pk, 'slug': blogpost.slug}))
	else:
		tags = ""

		if blogpost.tags.all().count() > 0:
			tags = blogpost.tags.all()

		data = { 
			'tag' : tags,
		}

		form = forms.CkEditorEditForm(instance=blogpost, initial=data)

	context = {
		'form': form,
		'blogpost': blogpost,
	}
	return render(request, 'form-edit.html', context)


def post_detail(request, post_id, slug):
	blogpost = get_object_or_404(BlogPost, pk=post_id)
	comments = Comment.objects.filter(bpId = blogpost).order_by('-create_date')
	blogpost.allLikes = Like.objects.filter(bpost=blogpost)
	blogpost.allDislikes = Dislike.objects.filter(bpost=blogpost)
	tags = blogpost.tags.all()
	liked = False
	disliked = False

	if blogpost.allLikes.filter(liker=request.user).count() == 1:
		liked = True

	if blogpost.allDislikes.filter(disliker=request.user).count() == 1:
		disliked = True

	if request.method == "POST":
		if request.user.is_authenticated():
			if 'like-btn' in request.POST:
				if Like.objects.filter(liker=request.user, bpost=blogpost).count() == 0:
					Like.objects.create(bpost=blogpost, liker=request.user)
					BlogPost.objects.filter(pk=post_id).update(likes=F('likes')+1)

					if Dislike.objects.filter(bpost=blogpost, disliker=request.user).count() > 0:
						Dislike.objects.filter(bpost=blogpost, disliker=request.user).delete()
						BlogPost.objects.filter(pk=post_id).update(dislikes=F('dislikes')-1)
					# blogpost.update(likes=F('likes')+1)
				else:
					Like.objects.filter(liker=request.user, bpost=blogpost).first().delete()
					BlogPost.objects.filter(pk=post_id).update(likes=F('likes')-1)
					# blogpost.update(likes=F('likes')-1)

				blogpost.save()
				return redirect(reverse('post-detail', kwargs={'post_id':post_id, 'slug': slug}))

			elif 'dislike-btn' in request.POST:
				if Dislike.objects.filter(disliker=request.user, bpost=blogpost).count() == 0:
					Dislike.objects.create(bpost=blogpost, disliker=request.user)
					BlogPost.objects.filter(pk=post_id).update(dislikes=F('dislikes')+1)

					if Like.objects.filter(bpost=blogpost, liker=request.user).count() > 0:
						Like.objects.filter(bpost=blogpost, liker=request.user).delete()
						BlogPost.objects.filter(pk=post_id).update(likes=F('likes')-1)
					# blogpost.update(Dislike=F('dislikes')+1)
				else:
					Dislike.objects.filter(disliker=request.user, bpost=blogpost).first().delete()
					BlogPost.objects.filter(pk=post_id).update(dislikes=F('dislikes')-1)
					# blogpost.update(Dislike=F('dislikes')-1)

				blogpost.save()
				return redirect(reverse('post-detail', kwargs={'post_id':post_id, 'slug': slug}))

			elif 'comment-btn' in request.POST:
				comment = request.POST['comment'].strip()
				new_comment = Comment.objects.create(content=comment, bpId=blogpost, ownerId=request.user)
				new_comment.save()

				print comment
				return redirect(reverse('post-detail', kwargs={'post_id':post_id, 'slug': slug}))

			elif 'delete-btn' in request.POST:
				postDelete = BlogPost.objects.get(id=post_id)
				postDelete.delete()

				return redirect(reverse('index'))

	return render(request, 'post.html', {"blogpost" : blogpost, "comments" : comments, "tags": tags, "liked" : liked, "disliked" : disliked})