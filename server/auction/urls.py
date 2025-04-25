from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('<int:pk>/', views.auction_detail, name='auction_detail'),
    path('create/', views.create_auction, name='create_auction'),
]
