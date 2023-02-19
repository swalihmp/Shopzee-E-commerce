from django.contrib import admin
from . import views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.shop,name='shop'),
    path('singleproduct/<int:id>/',views.singleproduct,name='singleproduct'),
    path('<slug:category_slug>/',views.shop,name='products_by_category'),
    path('search_data',views.search_data,name='search_data'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('blog',views.blog,name='blog'),
    path('submit_review/<int:id>/',views.submit_review,name='submit_review'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)