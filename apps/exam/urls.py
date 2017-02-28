from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^main$',views.home),
    url(r'^register',views.register),
    url(r'^login$',views.login),
    url(r'^quotes$',views.quotes),
    url(r'^logout$',views.logout),
    url(r'^add/quote$',views.add_quote),
    url(r'^add/favorite/(?P<quote_id>\d+)$',views.add_favorite),
    url(r'^remove/favorite/(?P<quote_id>\d+)$',views.remove_favorite),
    url(r'^users/(?P<user_id>\d+)$',views.show_user)
]
