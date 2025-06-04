from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auction.models import Auction
from auction.serializers import BidSerializer


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
