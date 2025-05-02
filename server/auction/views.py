from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Auction, Like, Comment
from .serializers import AuctionListSerializer, AuctionDetailSerializer, AuctionCreateSerializer, BidSerializer, CommentSerializer, LikeSerializer


class AuctionListView(generics.ListAPIView):
    """
    Lists all active auctions.
    """
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
def auction_cancel(request, pk):
    """
    Cancels an auction.
    """
    auction = get_object_or_404(Auction, pk=pk)
    if auction.seller != request.user:
        return Response({'error': 'You are not the owner of this auction.'}, status=status.HTTP_403_FORBIDDEN)
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
        pk=pk
    )

    if auction.seller == request.user:
        return Response({'error': 'You cannot bid on your own auction.'}, status=status.HTTP_403_FORBIDDEN)

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


class ManageCommentView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    """
    View for listing comments for a specific auction (GET),
    creating new comments (POST), updating a comment (PUT),
    and deleting a comment (DELETE).
    """

    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Return the queryset for retrieving comments.  This will be used
        by the mixins.  It is important to define this, and to make
        it specific to the auction.
        """
        auction_pk = self.kwargs['pk']  # Get auction primary key from URL
        auction = get_object_or_404(Auction, pk=auction_pk)
        return Comment.objects.filter(auction=auction)

    def get_object(self):
        """
        Gets a single comment instance.  Overriding this is necessary
        to ensure that the comment is retrieved in the context of the
        correct auction.
        """
        queryset = self.get_queryset()  # Get the base queryset for this view
        comment_id = self.kwargs['comment_id']
        obj = get_object_or_404(queryset, pk=comment_id)
        self.check_object_permissions(self.request, obj)  # check permission
        return obj

    def get_serializer_context(self):
        """
        Provides additional context to the serializer.  This is useful
        for create, update, and other operations that need request data
        or other contextual information.
        """
        context = super().get_serializer_context()
        context['auction'] = get_object_or_404(Auction, pk=self.kwargs['pk'])
        return context

    def create(self, request, *args, **kwargs):
        """
        Create a new comment.  Override the default create method to
        add the auction to the comment.
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Save a new comment instance, adding the user and auction.
        """
        auction = get_object_or_404(Auction, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, auction=auction)

    def update(self, request, *args, **kwargs):
        """
        Update an existing comment.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'You are not the author of this comment.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a comment.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'You are not the author of this comment.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Define the handler methods (get, post, put, delete)
    def get(self, request, *args, **kwargs):
        if 'comment_id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
