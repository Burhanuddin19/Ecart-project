
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
   path('',views.index,name='shophome'),
   path("about",views.about, name="About"),
   path("tracker",views.tracker, name="Tracker"),
   path("contact",views.contact, name="ContactUs"),
   path("search",views.search, name="Search"),
   path("products/<int:myid>",views.productview, name="Productview"),
   path("checkout",views.checkout, name="Checkout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

