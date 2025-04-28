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
        fields = ['id', 'auction', 'bidder', 'amount', 'created_at']
        read_only_fields = ['id', 'bidder', 'created_at']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Bid.objects.all(),
                fields=['user', 'auction', 'amount']
            )
        ]

    def validate_amount(self, value):
        auction = self.context['auction']
        user = self.context['request'].user
        if not auction.is_valid_bid(value, user):
            raise serializers.ValidationError("Invalid bid")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        auction = self.context['auction']

        validated_data['user'] = user
        validated_data['auction'] = auction

        auction.current_bid = validated_data['amount']
        auction.save()

        return Bid.objects.create(**validated_data)


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

    def create(self, validated_data):
        user = self.context['request'].user
        auction = self.context['auction']
        validated_data['user'] = user
        validated_data['auction'] = auction
        return Like.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'auction', 'user', 'comment_text',
                  'created_at', 'updated_at', 'is_deleted']
        read_only_fields = ['id', 'user', 'created_at',
                            'updated_at', 'is_deleted']


class AuctionListSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    # Add method fields
    highest_bid = serializers.SerializerMethodField()
    bid_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'seller', 'title', 'description', 'image_url', 'starting_price', 'current_bid', 'highest_bid',
                  'end_time', 'created_at', 'updated_at', 'is_active', 'bid_count', 'like_count', 'comment_count']
        read_only_fields = ['id', 'seller', 'current_bid', 'highest_bid',
                            'created_at', 'updated_at', 'bid_count', 'like_count', 'comment_count']

    def get_highest_bid(self, obj):
        """
        Returns the amount of the highest bid.
        """
        highest_bid = obj.get_highest_bid()
        if highest_bid:
            return highest_bid.amount
        return None

    def get_bid_count(self, obj):
        return obj.bid_set.count()

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()


class AuctionDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    # Add method fields
    bid_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    highest_bid = serializers.SerializerMethodField()

    # Add nested serializers for related models
    bids = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'seller', 'title', 'description', 'image_url', 'starting_price', 'current_bid', 'highest_bid' 'start_time',
                  'end_time', 'is_active', 'created_at', 'updated_at', 'bid_count', 'like_count', 'comment_count', 'bids', 'comments']
        read_only_fields = ['id', 'seller', 'current_bid', 'highest_bid', 'bid_count',
                            'like_count', 'comment_count', 'start_time', 'created_at', 'updated_at']

    def get_bids(self, obj):
        return obj.bid_set.values_list('amount', flat=True).order_by('-amount')

    def get_highest_bid(self, obj):
        """
        Returns the amount of the highest bid.
        """
        highest_bid = obj.get_highest_bid()
        if highest_bid:
            return highest_bid.amount
        return None

    def get_bid_count(self, obj):
        return obj.bid_set.count()

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comments.count()


class AuctionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new auction.
    """

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description',
                  'image_url', 'starting_price', 'end_time']
        read_only_fields = ['id']
