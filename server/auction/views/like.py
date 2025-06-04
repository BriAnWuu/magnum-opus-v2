from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auction.models import Auction, Like
from auction.serializers import LikeSerializer


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
