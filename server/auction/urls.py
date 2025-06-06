from django.urls import path

from auction.views.auction import (
    AuctionListView,
    AuctionCreateView,
    AuctionDetailView,
    auction_cancel,
)
from auction.views.like import manage_like
from auction.views.bid import place_bid
from auction.views.comment import ManageCommentView


urlpatterns = [
    path('', AuctionListView.as_view(), name='auction_list'),
    path('create/', AuctionCreateView.as_view(), name='auction_create'),
    path('<int:pk>/', AuctionDetailView.as_view(), name='auction_detail'),
    path('<int:pk>/cancel/', auction_cancel, name='auction_cancel'),

    path('<int:pk>/bid/', place_bid, name='place_bid'),

    path('<int:pk>/comment/', ManageCommentView.as_view(), name='manage_comment'),
    path(
        '<int:pk>/comment/<uuid:comment_id>/',
        ManageCommentView.as_view(),
        name='manage_comment_id'
    ),

    path('<int:pk>/like/', manage_like, name='manage_like'),
]
