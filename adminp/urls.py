from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('users/',views.users,name='users'),
    path('deleteuser/<int:id>/',views.deleteuser,name='deleteuser' ),
    path('blockuser/<int:id>/<str:action>/',views.blockuser,name='blockuser'),
]
