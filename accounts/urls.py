from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('forgot_password/', views.forgot_password,name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword,name='resetpassword'),
    path('change_password/', views.change_password,name='change_password'),
    path('add_address/', views.add_address,name='add_address'),
    path('invoice/<int:id>/',views.invoice,name='invoice')
    
]
