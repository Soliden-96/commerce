from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.TextField()
    category = models.CharField(max_length = 64)
    imageUrl = models.ImageField(upload_to = '')
    startingBid = models.DecimalField(max_digits = 10, decimal_places = 2)
    currentBid = models.DecimalField(max_digits = 10, decimal_places = 2)
    active = models.BooleanField()

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "offers")
    value = models.DecimalField(max_digits = 10, decimal_places = 2)


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments_made")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    content = models.TextField()
    


