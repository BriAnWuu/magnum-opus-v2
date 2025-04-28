from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Auction, Like, Comment
from .serializers import AuctionListSerializer, AuctionDetailSerializer, AuctionCreateSerializer, BidSerializer, CommentSerializer, LikeSerializer


class AuctionListView(generics.ListAPIView):
    """
    Lists all active auctions.
    """
    queryset = Auction.objects.filter(is_active=True)
    serializer_class = AuctionListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            if is_active.lower() == 'true':
                return Auction.objects.filter(is_active=True)
            elif is_active.lower() == 'false':
                return Auction.objects.filter(is_active=False)
            else:
                raise ValidationError('Invalid query parameter for is_active.')
        return Auction.objects.all()


class AuctionDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single auction.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class AuctionCreateView(generics.CreateAPIView):
    """
    Creates a new auction.
    """
    serializer_class = AuctionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Assigns the seller to the auction.
        """
        serializer.save(seller=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_auction(request, pk):
    """
    Cancels an auction.
    """
    auction = get_object_or_404(Auction, pk=pk)
    if auction.seller != request.user:
        return Response({'error': 'You are not the seller of this auction.'}, status=status.HTTP_403_FORBIDDEN)
    if not auction.can_cancel():
        return Response(
            {'error': 'Auction cannot be canceled.  It either has bids or the end time has passed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    auction.is_active = False
    auction.save()
    return Response({'message': 'Auction canceled successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, pk):
    """
    Places a bid on an auction.
    """
    auction = get_object_or_404(
        Auction,
        pk=pk,
        is_active=True
    )
    serializer = BidSerializer(
        data=request.data,
        context={
            'request': request,
            'auction': auction
        }
    )
    if serializer.is_valid():
        try:
            # Involves multiple models, therefore using transaction/commit
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_comment(request, pk, comment_id=None):
    """
    Creates, edits, or deletes a comment on an auction.
    """
    auction = get_object_or_404(
        Auction,
        pk=pk
    )

    if request.method == 'POST':
        serializer = CommentSerializer(
            data=request.data,
            context={
                'request': request,
                'auction': auction
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not comment_id:
            return Response({'error': 'Comment ID is required for editing.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment = Comment.objects.get(pk=comment_id, auction=auction)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({'error': 'You are not the author of this comment.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(
            comment,
            data=request.data,
            context={
                'request': request,
                'auction': auction
            },
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not comment_id:
            return Response({'error': 'Comment ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment = Comment.objects.get(pk=comment_id, auction=auction)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
        if comment.user != request.user:
            return Response({'error': 'You are not the author of this comment.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_like(request, pk):
    """
    Likes or removes a like from an auction.
    """
    auction = get_object_or_404(
        Auction,
        pk=pk
    )

    if request.method == 'POST':
        serializer = LikeSerializer(
            data=request.data,
            context={
                'request': request,
                'auction': auction
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            like = Like.objects.get(user=request.user, auction=auction)
            like.delete()
            return Response({'message': 'Like removed successfully.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'You have not liked this auction.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
