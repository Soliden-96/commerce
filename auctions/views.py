from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import User, Listing, Bid, Comment, Watchlist

categories = [
    (None,"Category"),
    ("Rock","Rock"),
    ("Pop","Pop"),
    ("Jazz","Jazz"),
    ("HipHop/RnB","HipHop/RnB"),
    ("Electronic/Dance","Electronic/Dance")
    ]
class createListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Artist'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Provide a brief description of the article'}))
    category = forms.ChoiceField(choices=categories)
    startingPrice = forms.DecimalField(min_value=0, decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={'placeholder':'Starting Price'}))
    imageUrl = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'Provide Url for an image'}))


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "listings":listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def createListing(request):
    if request.method == "POST":
        form = createListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            artist = form.cleaned_data["artist"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            startingPrice = form.cleaned_data["startingPrice"]
            imageUrl = form.cleaned_data["imageUrl"]
            seller = request.user

            listing = Listing(
                title=title,
                artist=artist,
                description=description,
                category=category,
                startingPrice=startingPrice,
                imageUrl=imageUrl,
                active=True,
                seller=seller
            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))


    return render(request,"auctions/createListings.html",{
        "categories":categories, "form":createListingForm()
    })


def listing(request,id):
    
    listing = Listing.objects.get(id=id)
    comments = range(100)
    existing = None
    low_offer = None

    if request.user.is_authenticated:
        user = request.user
        if user.watchlist.filter(watched=listing).exists():
            existing = True
    
    if request.method == "POST":
        offer = float(request.POST["offer"])
        if offer <= listing.currentBid or offer <= listing.startingPrice:
            low_offer = True
        else:
            listing.currentBid = offer
            bid = Bid(bidder=user, listing=listing, value=offer)
     
        
    return render(request,"auctions/listing.html",{
        "listing":listing, "comments":comments, "existing":existing, "low_offer":low_offer 
    })


@login_required
def addToWatchlist(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        user = request.user

        if user.watchlist.filter(watched=listing).exists():
            return HttpResponseRedirect(reverse("listing",args=[listing.id])) 

        watchlist = Watchlist(watcher=user, watched=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing",args=[listing.id]))

    return HttpResponseRedirect(reverse("listing",args=[listing.id]))


@login_required
def removeFromWatchlist(request,id):
    listing = Listing.objects.get(id=id)
    user = request.user

    if request.method == "POST":
        user.watchlist.filter(watched=listing).delete()
        return HttpResponseRedirect(reverse("listing",args=[listing.id]))
            
    return HttpResponseRedirect(reverse("listing",args=[listing.id]))


    
    

