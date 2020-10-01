from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass

class Catagory(models.Model):
    catagory = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"Catagory: {self.catagory}"

class Listing(models.Model):
    list_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_lists')
    item_name = models.CharField(max_length=255)
    item_price = models.FloatField(null=False)
    item_catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, related_name='items')
    item_description = models.TextField(blank=False, null=False, default=None)
    date_placed = models.DateTimeField(auto_now_add=True)
    item_image = models.ImageField(blank=True, null=True,upload_to='images')
    is_active = models.BooleanField(default=True)

    @staticmethod
    def createListing(user, name, price, catagory, description, image):
        listing = Listing(list_user=user, item_name=name, item_price=price, item_catagory=catagory, item_description=description, item_image=image)
        listing.save()

    def __str__(self):
        return f"""Item: {self.item_name},
Price: {self.item_price} USD,
Placed at {self.date_placed}"""



class Bid(models.Model):
    bid_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_bids')
    bid_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='item_bids')
    bid_price = models.FloatField(null=False)
    bid_datetime = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def place_bid(user, item, price):
        bid = Bid(bid_user=user, bid_item=item, bid_price=price)
        bid.save()

    def __str__(self):
        return f"Bidding User: {self.bid_user}, Bidded Item: {self.bid_item}, Price: {self.bid_price} At {self.bid_datetime}"

class Comment(models.Model):
    comment_uesr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comments")
    comment      = models.TextField(blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def save_comment(user, item, comment):
        cmt = Comment(comment_uesr=user, comment_item=item, comment=comment)
        cmt.save()

    def __str__(self):
        return f"Comment: '{self.comment}' by {self.comment_uesr} on {self.comment_item} at {self.comment_date}"

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_watchlists')
    watchlist_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlisted')

    @staticmethod
    def save_watchlist(user, item):
        wl = Watchlist(user=user, watchlist_item=item)
        wl.save()        

    def __str__(self):
        return f"{self.user} added {self.watchlist_item} to watchlists"

