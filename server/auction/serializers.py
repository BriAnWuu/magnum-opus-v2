from rest_framework import serializers
from .models import Auction, Bid, Like, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AuctionSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    bid_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'seller', 'title', 'description', 'image_url', 'starting_price',
                  'current_bid', 'bid_count', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'seller', 'current_bid',
                            'bid_count', 'start_time', 'created_at', 'updated_at']


class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'bid_amount', 'created_at']
        read_only_fields = ['id', 'bidder', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True)

    class Meta:
        model = Like
        fields = ['id', 'auction', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['auction', 'user']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'auction', 'user', 'comment_text',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at',
                            'updated_at']
