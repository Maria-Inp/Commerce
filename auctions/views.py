from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    activeList = Active_List.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "activeList": activeList,
        "categories": categories
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

def addProduct(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/addProductForm.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        categoryType = request.POST["category"]

        category = Category.objects.get(categoryName=categoryType)
        user = request.user
        bid = Bid(bid=float(price), user=user)
        bid.save()

        activeList = Active_List(title=title, category=category, description=description, price=bid, imageUrl=imageUrl, owner=user)

        activeList.save()

        return HttpResponseRedirect(reverse(index))

def category(request):
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        categories = Category.objects.get(categoryName=categoryFromForm)
        activeList = Active_List.objects.filter(isActive=True, category=categories)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "activeList": activeList,
            "categories": categories
        })

# show product information
def listingPage(request, id):
    listInfo = Active_List.objects.get(pk=id)
    inWatchList = request.user in listInfo.watchList.all()
    comments = Comment.objects.filter(activeList=listInfo)
    isOwner = request.user.username == listInfo.owner.username
    return render(request, "auctions/listingPage.html", {
        "listInfo": listInfo,
        "inWatchList": inWatchList,
        "comments": comments,
        "isOwner": isOwner
    })

def watchList(request):
    currentUser = request.user
    userWatchList = currentUser.watchList.all()
    # watchList name in urls.py
    return render(request, "auctions/watchList.html", {
        "watchList": userWatchList
    })

def removeWatchList(request, id):
    listInfo = Active_List.objects.get(pk=id)
    currentUser = request.user
    listInfo.watchList.remove(currentUser)
    return HttpResponseRedirect(reverse("listingPage", args=(id, )))

def addWatchList(request, id):
    listInfo = Active_List.objects.get(pk=id)
    currentUser = request.user
    listInfo.watchList.add(currentUser)
    return HttpResponseRedirect(reverse("listingPage", args=(id, )))

def addComment(request, id):
    currentUser = request.user
    listInfo = Active_List.objects.get(pk=id)
    message = request.POST['comment']
    # comment name of textarea tag
    newComment = Comment(author=currentUser, text=message, activeList=listInfo)
    newComment.save()
    return HttpResponseRedirect(reverse("listingPage", args=(id, )))

def addBid(request, id):
    newBid = request.POST['bid']
    listInfo = Active_List.objects.get(pk=id)
    isOwner = request.user.username == listInfo.owner.username
    comments = Comment.objects.filter(activeList=listInfo)
    inWatchList = request.user in listInfo.watchList.all()

    if float(newBid) > listInfo.price.bid:
        updateBid = Bid(user=request.user, bid=float(newBid))
        updateBid.save()
        listInfo.price = updateBid
        listInfo.save()
        return render(request, "auctions/listingPage.html", {
            "listInfo": listInfo,
            "message":"Price changed successfully!",
            "update": True,
            "inWatchList": inWatchList,
            "comments": comments,
            "isOwner": isOwner
        })
    else:
        return render(request, "auctions/listingPage.html", {
            "listInfo": listInfo,
            "message":"The suggestion price should be more than current price!",
            "update": False,
            "inWatchList": inWatchList,
            "comments": comments,
            "isOwner": isOwner
        })

def closeAuction(request, id):
    listInfo = Active_List.objects.get(pk=id)
    listInfo.isActive = False
    listInfo.save()
    inWatchList = request.user in listInfo.watchList.all()
    comments = Comment.objects.filter(activeList=listInfo)
    isOwner = request.user.username == listInfo.owner.username
    messageAuction = "Auction is closed."

    return render(request, "auctions/listingPage.html", {
            "listInfo": listInfo,
            "inWatchList": inWatchList,
            "comments": comments,
            "isOwner": isOwner,
            "updateAuction": True,
            "messageAuction": messageAuction
        })
