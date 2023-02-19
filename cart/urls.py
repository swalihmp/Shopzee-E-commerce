from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('cart',views.cart,name='cart'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('addtowish/<int:id>',views.addtowish,name='addtowish'),
    path('cartinc',views.cartinc,name='cartinc'),
    path('cartdic',views.cartdic,name='cartdic'),
    path('addressload',views.addressload,name='addressload'),
    
    path('remove/<int:id>',views.remove,name='remove'),
    path('removewish/<int:id>',views.removewish,name='removewish'),
    path('checkout',views.checkout,name='checkout'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
       
]