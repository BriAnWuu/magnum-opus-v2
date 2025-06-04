from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from auction.models import Auction, Comment
from auction.serializers import CommentSerializer


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
