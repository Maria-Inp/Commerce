from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addProduct", views.addProduct, name="addProduct"),
    path("category", views.category, name="category"),
    path("listingPage/<int:id>", views.listingPage, name="listingPage"),
    path("watchList", views.watchList, name="watchList"),
    path("removeWatchList/<int:id>", views.removeWatchList, name="removeWatchList"),
    path("addWatchList/<int:id>", views.addWatchList, name="addWatchList"),
    path("comment/<int:id>", views.addComment, name="comment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
]
