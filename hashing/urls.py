from django.urls import path
from .views import home, hash, quickhash
urlpatterns = [
    path('hash/<str:hash>', hash, name='hash'),
    path('quickhash/', quickhash, name="quickhash"),
    path('', home, name='home'),
]
