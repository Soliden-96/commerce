from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("<int:id>/listing", views.listing, name="listing"),
    path("<int:id>/addToWatchlist", views.addToWatchlist, name="addToWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/removeFromWatchlist", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("<int:id>/placeBid", views.placeBid, name="placeBid"),
    path("<int:id>/comment", views.comment, name="comment")
]
