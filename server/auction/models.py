from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_highest_bid(self):
        """
        Returns the highest bid for this auction.
        """
        if self.bid_set.exists():
            return self.bid_set.order_by('-amount').first()
        return None

    def can_cancel(self):
        """
        Determines if the auction can be canceled.
        Auctions can be canceled if they have no bids and the end time has not passed.
        """
        return self.bid_set.count() == 0 and self.end_time > timezone.now()


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('auction', 'bidder', 'amount')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.auction.title}"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('auction', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.auction.title}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # soft delete

    def __str__(self):
        return f"{self.user.username} commented on {self.auction.title}"

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete the comment by setting is_deleted to True.
        """
        self.is_deleted = True
        self.save()
