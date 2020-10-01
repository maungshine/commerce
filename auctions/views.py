from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Catagory, Watchlist


def index(request):
    active_listings = Listing.objects.order_by('date_placed').reverse()
    comments = Comment.objects.all()
    return render(request, "auctions/index.html", {
        'active_listings': active_listings,
        'comments': comments
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

@login_required
def listing(request, item_id):
    listing_item = Listing.objects.get(pk=item_id)

    bids = listing_item.item_bids.all()
    largest_bid = None
    if bids:
        for bid in bids:
            if not largest_bid:
                largest_bid = bid
            if bid.bid_price > largest_bid.bid_price:
                largest_bid = bid 

    try:
        watchlist = Watchlist.objects.get(user=request.user, watchlist_item=listing_item)
    except Watchlist.DoesNotExist:
        watchlist = None    
    return render(request, "auctions/listing.html", {
        "listing_item": listing_item,
        "watchlist": watchlist,
        "winner_bid": largest_bid
    })

@login_required
def create_listing(request):
    values = Catagory.objects.all()
    if request.method == "POST":
        item_name = request.POST["name"]
        item_catagory = request.POST["catagory"]
        catagory = Catagory.objects.filter(catagory=item_catagory).first()
        item_description = request.POST["description"]
        item_price = request.POST["price"]
        item_image = request.FILES["image"]
        Listing.createListing(request.user, item_name, item_price, catagory, item_description, item_image)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "values": values
    })

@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()

    #find the winner for the closed auction
    bids = listing.item_bids.all()
    largest_bid = None
    if bids:
        for bid in bids:
            if not largest_bid:
                largest_bid = bid
            if bid.bid_price > largest_bid.bid_price:
                largest_bid = bid    

    return render(request, "auctions/listing.html", {
        "winner_bid": largest_bid,
        "listing_item": listing,
        "watchlist": None
    })

@login_required
def place_bids(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            bid_item = Listing.objects.get(pk=item_id)
            bid_price = int(request.POST["bid"])
            bids = bid_item.item_bids.all()
            largest_bid = bid_item.item_price
            if bids:
                for bid in bids:
                    if largest_bid == bid_item.item_price:
                        largest_bid = bid.bid_price
                    elif bid.bid_price > largest_bid:
                        largest_bid = bid.bid_price    

            if not bid_price or not bid_item.is_active:
                return HttpResponseRedirect(reverse("index"))
            if bid_price <= bid_item.item_price or bid_price <= largest_bid:
                return HttpResponseRedirect(reverse("listing", kwargs={
                    "item_id": item_id
                }))
            Bid.place_bid(request.user, bid_item, bid_price)
            bid_item.item_price = bid_price
            bid_item.save() 
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("register"))

@login_required
def comment(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            comment = request.POST["comment"]
            if not comment:
                return HttpResponseRedirect(reverse("index"))
            comment_item = Listing.objects.get(pk=item_id)
            Comment.save_comment(request.user, comment_item, comment)
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("register"))

@login_required
def add_to_watchlist(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            item = Listing.objects.get(pk=item_id)
            Watchlist.save_watchlist(request.user, item)
        return HttpResponseRedirect(reverse("listing", kwargs={
            "item_id": item_id
        }))

@login_required
def my_watchlist(request):
    watchlists = request.user.user_watchlists.all()
    return render(request, "auctions/my_watchlist.html", {
        "watchlists": watchlists
    })            

@login_required
def remove_from_watchlist(request, watchlist_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            watchlist = Watchlist.objects.get(pk=watchlist_id)
            print(watchlist)
            item_id = watchlist.watchlist_item.id
            watchlist.delete()
        return HttpResponseRedirect(reverse("listing", kwargs={
            "item_id": item_id
        }))

def catagory(request):
    catagories = Catagory.objects.all()
    return render(request, "auctions/catagory.html", {
        "catagories": catagories
    })

def catagory_items(request, catagory_id):
    catagory_items = Catagory.objects.get(pk=catagory_id).items.all()
    return render(request, "auctions/catagory_items.html", {
        "catagory_items": catagory_items,
        "catagory": Catagory.objects.get(pk=catagory_id)
    })

@login_required
def my_active_or_close(request, status):
    if status == "active":
        user_lists = request.user.user_lists.filter(is_active=True)
    else:
        user_lists = request.user.user_lists.filter(is_active=False)
    print(user_lists)
    return render(request, "auctions/my_listing.html", {
        "user_lists": user_lists
    })            

                    