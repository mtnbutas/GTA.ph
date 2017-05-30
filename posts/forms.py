from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingFormField
# from ckeditor.fields import RichTextUploadingField 
import ckeditor
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import BlogPost

class CkEditorForm(forms.ModelForm):
	title = forms.CharField(widget=TextInput(attrs={'placeholder': 'Title', 'maxlength': '80'}))
	# content = RichTextUploadingField()
	# content = RichTextUploadingFormField()
	coverphoto = forms.ImageField(label='Add a cover photo')
	content = forms.CharField(widget=CKEditorUploadingWidget())
	class Meta:
		model = BlogPost
		fields = [
				'coverphoto',
				'title',
				'content',
				'tags',]

##########################################

class CkEditorEditForm(forms.ModelForm):
	title = forms.CharField(widget=TextInput(attrs={'placeholder': 'Title', 'maxlength': '80'}))
	# content = RichTextUploadingField()
	# content = RichTextUploadingFormField()
	coverphoto = forms.ImageField(label='Change cover photo')
	content = forms.CharField(widget=CKEditorUploadingWidget())
	class Meta:
		model = BlogPost
		fields = [
				'coverphoto',
				'title',
				'content',
				'tags',]

##########################################