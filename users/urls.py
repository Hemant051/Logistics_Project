from django.urls import path
from .views import home, profile,contact, RegisterView
from . import views
urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('index/',views.index,name='index'),
    path('result/',views.result,name='result'),
    path("contact/", views.contact, name='contact'),
    path('profile/', profile, name='users-profile'),
]
