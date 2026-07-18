from django.urls import path
from .views import *

urlpatterns = [
    path('home/', Home),
    path('view_cart/', view_cart),
    path('seller_order/', seller_order),
    path('review/', review.as_view()),
    path('ProductReviewsView/', ProductReviewsView.as_view())
]
