from django import forms

from django.contrib.auth.models import User
from .models import Profile


class UserInfoForm(forms.ModelForm):
	avatar = forms.FileField(required=False)
	bio = forms.CharField(required=False, widget=forms.Textarea, max_length=300)
	# password1 = forms.CharField()
	# password2 = forms.CharField()

	def save(self, commit=True):
		instance = super(UserInfoForm, self).save(commit=commit)
		print self.cleaned_data
		if self.cleaned_data['avatar']:
			instance.profile.avatar = self.cleaned_data['avatar']
			instance.profile.save()

		if self.cleaned_data['bio']:
			instance.profile.bio = self.cleaned_data['bio']
			instance.profile.save()

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'avatar', 'bio']
