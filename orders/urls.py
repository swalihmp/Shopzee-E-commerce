from . import views
from django.urls import path

urlpatterns=[
    path('place_order/<STR', views.place_order, name='place_order'),
    path('payment', views.payment, name='payment'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('cod_order_complete',views.cod_order_complete,name='cod_order_complete'),
]