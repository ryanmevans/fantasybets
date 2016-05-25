from django.conf.urls import url, include
from . import views

app_name= 'betting'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

	url(r'^register$', views.UserFormView.as_view(), name='register'),
	url(r'^login$', views.login_user, name='login_user'),
	url(r'^logout$', views.logout_user, name='logout_user'),


    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),     
    url(r'placebet$', views.BetCreate.as_view(), name='placebet'), 
    url(r'mybets$', views.BetsView.as_view(), name='mybets'),
]
