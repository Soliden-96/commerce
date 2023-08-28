from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    artist = models.CharField(max_length = 64, null=True)
    description = models.TextField()
    category = models.CharField(max_length = 64)
    imageUrl = models.URLField()
    startingPrice = models.DecimalField(max_digits = 10, decimal_places = 2)
    currentBid = models.DecimalField(max_digits = 10, decimal_places = 2)
    active = models.BooleanField()
    seller = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listings")

    def __str__(self):
        return f"{self.title} by {self.artist} listed by {self.seller}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "offers")
    value = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    def __str__(self):
        return f"{self.value} has been offered by {self.bidder} for {self.listing}"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments_made")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    content = models.TextField()
    
    def __str__(self):
        return f"Comment posted by {self.commenter} for {self.listing}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete = models.CASCADE,  related_name = "watchlist")
    watched = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "watchedBy")

    def __str__(self):
        return f"{self.watcher} has {self.watched} on his watchlist"
    


