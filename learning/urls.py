from django.conf.urls import url, include
from django.urls import path
from lists import views, urls

urlpatterns = [
    url(r'^$', views.home_page, name = 'home'),
    url(r'^lists/', include(urls)),
]

# urlpatterns = [
#     path('', views.home_page, name='home'),
#     path('lists/new', views.new_list, name='new_list'),
#     path('lists/(.+)/', views.view_list, name='view_list'),
# ]
