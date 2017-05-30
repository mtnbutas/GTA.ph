# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import User
from .models import Profile
from posts.models import BlogPost

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.core.urlresolvers import reverse
from django.views import generic

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from forms import UserInfoForm

# Create your views here.
def user_profile(request, user_id, user_username):
	# user = User.objects.filter(pk = user_id)
	user = get_object_or_404(User, pk=user_id)
	# print user
	# print user.password
	user_posts = BlogPost.objects.filter(owner=user).order_by('-create_date')

	return render(request, 'profile.html', {'user': user, 'user_posts': user_posts})

def edit_profile(request):
	if not request.user.is_authenticated:
		return redirect('login')

	context = {}
	data = { 
		'bio': request.user.profile.bio
	}
	form = UserInfoForm(instance=request.user, initial=data)

	if request.method == 'POST':
		if "edit-prof" in request.POST:
			print "IN EDIT PROFILE"
			form = UserInfoForm(request.POST, request.FILES, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect(
					reverse('user-profile', kwargs={'user_id': request.user.pk, 'user_username': request.user.username}))
		elif "change-password" in request.POST:
			print "IN CHANGE PASSWORD"
			currPassword = request.POST['currpassword']
			password1 = request.POST['password1']
			password2 = request.POST['password2']

			if request.user.check_password(currPassword):
				if password1 == password2:
					user = request.user
					user.set_password(password1)
					user.save()
					return redirect('login')
				else:
					print "error_message"
					context['error_message'] = "Passwords do no match"
			else:
				print "validation error"
				context['error_message'] = "Wrong Password"	

		elif "delete-acc" in request.POST:
			userDelete = User.objects.get(id=request.user.pk)
			userDelete.delete()
			return redirect(reverse('index'))

	context = {
		'form': form
	}
	return render(request, 'edit_profile.html', context)

def signup(request):
	return render(request, 'signup.html')

def signup_view(request):
	if request.user.is_authenticated():
		return redirect('index')

	context = {}

	if request.method == "POST":
		username = request.POST['username'].strip()
		password1 = request.POST['password1'].strip()
		password2 = request.POST['password2'].strip()
		first_name = request.POST['first_name'].strip()
		last_name = request.POST['last_name'].strip()
		email = request.POST['email'].strip()

		# print username, password1, password2, first_name, last_name, email
		check = re.match('^[\w|-]+$', username)

		username_valid = User.objects.filter(username=username)
		email_valid = User.objects.filter(email=email)
		context["first_name"] = first_name
		context["last_name"] = last_name

		if email_valid.exists():
			context["error_message"] = "Email is already registered."
		elif username_valid.exists():
			context["error_message"] = "Username is already taken."
		elif password1 != password2:
			context["error_message"] = "Passwords did not match."
		elif check is None:
			context["error_message"] = "Username is invalid."
		else:
			context = {}
			new_user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
			new_user.set_password(password1)
			new_user.is_staff = True
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			profile.save()
			auth_user = authenticate(username=username, password=password1)
			if auth_user is not None:
				login(request, auth_user)
				print "USER IS AUTHENTICATED"
				return redirect('index')
			# print "USER IS OKAY"

	return render(request, 'registration/signup.html', context=context)

def login_view(request):
	if request.user.is_authenticated():
		return redirect('index')

	context = {}

	if request.method == "POST":
		username = request.POST['username'].strip()
		password = request.POST['password'].strip()

		user = authenticate(username=username, password=password)

		if user is not None:
			print "username and password are correct"
			login(request, user)
			return redirect('index')

		else:
			context["error_message"] = "Wrong username or password"
			context["username"] = username

	return render(request, 'registration/login.html', context=context)

def logout_view(request):
	logout(request)
	return redirect('index')

