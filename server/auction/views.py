from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Auction
from .serializers import AuctionSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([AllowAny])
def auction_list(request):
    auctions = Auction.objects.all()
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    serializer = AuctionSerializer(auction)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_auction(request):
    serializer = AuctionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
