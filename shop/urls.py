from django.urls import path
from .views import *

urlpatterns = [
    path('add_to_cart/', add_to_cart, name="add-to-cart"),
    path('view_cart/', view_cart),
    path('create_order/', create_order),
    path('seller_order/', seller_order),
    path('review/', review.as_view()),
    path('ProductReviewsView/', ProductReviewsView.as_view())
]
