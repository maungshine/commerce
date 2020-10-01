from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("bid/<int:item_id>", views.place_bids, name="place_bids"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("watchlist/<int:item_id>", views.add_to_watchlist, name="add-to-watchlist"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("remove_from_watchlist<int:watchlist_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("catagory", views.catagory, name="catagory"),
    path("catagory_items/<int:catagory_id>", views.catagory_items, name="catagory_items"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("my_active_or_close/<str:status>", views.my_active_or_close, name="my_active_or_close")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
