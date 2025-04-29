from django.urls import path
from .views import AuctionListView, AuctionCreateView, AuctionDetailView, cancel_auction, place_bid, manage_comment, manage_like

urlpatterns = [
    path('', AuctionListView.as_view(), name='auction_list'),
    path('create/', AuctionCreateView.as_view(), name='auction_create'),
    path('<int:pk>/', AuctionDetailView.as_view(), name='auction_detail'),
    path('<int:pk>/cancel/', cancel_auction, name='cancel_auction'),

    path('<int:pk>/bid/', place_bid, name='place_bid'),

    path('<int:pk>/comment/', manage_comment, name='manage_comment'),
    path('<int:pk>/comment/<int:comment_id>/',
         manage_comment, name='manage_comment'),

    path('<int:pk>/like/', manage_like, name='manage_like'),
]
