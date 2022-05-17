from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name="register"),
    url(r'^studio/$', views.studio, name="studio"),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^add_post/$', views.addPost, name="add_post"),
    url(r'^comment/(?P<post_slug>[-\w]+)/$', views.comment, name='comment'),
    url(r'^detail/(?P<post_slug>[-\w]+)/$', views.detail, name='detail'),
    url(r'^editDetail/delete/(?P<post_slug>[-\w]+)/$', views.deletePost, name='delete'),
    url(r'^editDetail/(?P<post_slug>[-\w]+)/$', views.editDetail, name='editDetail'),
    url(r'^(?P<genre>[-\w]+)/$', views.index, name="index_by_genre"),
]