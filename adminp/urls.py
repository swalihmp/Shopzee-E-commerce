from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('users/',views.users,name='users'),
    path('blockuser/<int:id>/<str:action>/',views.blockuser,name='blockuser'),
    path('adminaddproduct/',views.adminaddproduct,name='adminaddproduct'),
    path('adminproducts/',views.adminproducts,name='adminproducts'),
    path('category',views.category,name='category'),
    path('unlist/<int:id>/<str:action>/',views.unlist,name='unlist'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('productsingle/<int:id>',views.productsingle,name='productsingle'),
    path('editcategory/<int:id>/',views.editcategory,name='editcategory'),
    path('slideshow',views.slideshow,name='slideshow')
    
]
