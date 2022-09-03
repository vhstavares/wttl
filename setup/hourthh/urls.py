from django.urls import path

from . import views

urlpatterns = [
    path('struct_data/', views.struct_data, name='struct_data'),
]