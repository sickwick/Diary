from django.conf.urls import url
from django.urls import path
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
    url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]

# urlpatterns = [
#     path('', views.home_page, name='home'),
#     path('lists/new', views.new_list, name='new_list'),
#     path('lists/(.+)/', views.view_list, name='view_list'),
# ]

