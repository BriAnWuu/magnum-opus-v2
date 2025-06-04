from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from auction.models import Auction
from auction.serializers import (
    AuctionListSerializer,
    AuctionDetailSerializer,
    AuctionCreateSerializer,
)


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
