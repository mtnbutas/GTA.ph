from django.conf.urls import url
from django.views.generic.edit import CreateView

from views import signup_view
from views import login_view
from views import logout_view
from views import user_profile
from views import edit_profile


urlpatterns = [
	url(r'^signup/', signup_view, name='signup'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^edit-profile/$', edit_profile, name='edit-profile'),
    url(r'^user-profile/(?P<user_id>\d+)/(?P<user_username>[\w\-]+)/$', user_profile, name='user-profile'),
]