from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('users/',views.users,name='users'),
    path('blockuser/<int:id>/<str:action>/',views.blockuser,name='blockuser'),
    path('change/<int:id>/<str:action>/',views.change,name='change'),
    path('adminaddproduct/',views.adminaddproduct,name='adminaddproduct'),
    path('adminproducts/',views.adminproducts,name='adminproducts'),
    path('category',views.category,name='category'),
    path('unlist/<int:id>/<str:action>/',views.unlist,name='unlist'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('productsingle/<int:id>',views.productsingle,name='productsingle'),
    path('editcategory/<int:id>/',views.editcategory,name='editcategory'),
    path('editprod/<int:id>/',views.editprod,name='editprod'),
    path('slideshow',views.slideshow,name='slideshow'),
    path('deleteslider/<int:id>',views.deleteslider,name='deleteslider'),
    path('addcoupon',views.addcoupon,name='addcoupon'),
    path('deletecoupon/<int:id>',views.deletecoupon,name='deletecoupon'),
    path('orders',views.orders,name='orders'),
    path('order_details/<int:id>/',views.order_details,name='order_details'),
    path('productvar',views.productvar,name='productvar'),
    path('blockvari/<int:id>/<str:action>/',views.blockvari,name='blockvari'),
    path('delcategory/<int:id>/',views.delcategory,name='delcategory'),
    path('multipleimages',views.multipleimages,name='multipleimages'),
    path('deleteimg/<int:id>/',views.deleteimg,name='deleteimg'),
    
    
]
