from rest_framework import serializers
from .models import Auction, Bid, Like, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True
    )

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'bid_amount', 'created_at']
        read_only_fields = ['id', 'bidder', 'created_at']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Bid.objects.all(),
                fields=['user', 'auction', 'bid_amount']
            )
        ]

    def validate_bid_amount(self, value):
        auction = self.initial_data.get('auction')  # Use self.initial_data
        if not auction:
            raise serializers.ValidationError("Auction id is required.")
        try:
            auction_instance = Auction.objects.get(pk=auction)
        except Auction.DoesNotExist:
            raise serializers.ValidationError("Invalid auction id.")
        if value <= auction_instance.current_bid:
            raise serializers.ValidationError(
                "Bid amount must be greater than the current highest bid.")
        if value <= auction_instance.starting_price:
            raise serializers.ValidationError(
                "Bid amount must be greater than the starting price.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True
    )

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
        queryset=Auction.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'auction', 'user', 'comment_text',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at',
                            'updated_at']


class AuctionSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    # Add method fields
    bid_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'seller', 'title', 'description', 'image_url', 'starting_price', 'current_bid',
                  'start_time', 'end_time', 'status', 'created_at', 'updated_at', 'bid_count', 'like_count', 'comment_count']
        read_only_fields = ['id', 'seller', 'current_bid', 'start_time',
                            'created_at', 'updated_at', 'bid_count', 'like_count', 'comment_count']

    def get_bid_count(self, obj):
        return obj.bid_set.count()

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comments.count()


class AuctionDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)

    # Add method fields
    bid_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    # Add nested serializers for related models
    bids = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'seller', 'title', 'description', 'image_url', 'starting_price', 'current_bid', 'start_time',
                  'end_time', 'status', 'created_at', 'updated_at', 'bid_count', 'like_count', 'comment_count', 'bids', 'comments']
        read_only_fields = ['id', 'seller', 'current_bid', 'bid_count',
                            'like_count', 'comment_count', 'start_time', 'created_at', 'updated_at']

    def get_bids(self, obj):
        return obj.bid_set.values_list('bid_amount', flat=True).order_by('-bid_amount')

    # def get_comments(self, obj):
    #     comments = Comment.objects.filter(auction=obj).order_by(
    #         '-created_at')
    #     return CommentSerializer(comments, many=True).data

    def get_bid_count(self, obj):
        return obj.bid_set.count()

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comments.count()
