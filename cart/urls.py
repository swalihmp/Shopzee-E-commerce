from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('cart',views.cart,name='cart'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('addtowish/<int:id>',views.addtowish,name='addtowish'),
    path('cartinc/<int:id>',views.cartinc,name='cartinc'),
    path('cartdic/<int:id>',views.cartdic,name='cartdic'),
     path('remove/<int:id>',views.remove,name='remove'),
       
]