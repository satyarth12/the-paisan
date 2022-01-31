from django.urls import path

from .views.review_views import (ReviewDetailView,
                                 ReviewCreateView)

from .views.rating_views import RatingCreateView, RatingDetailView
app_name = 'rating_review'

urlpatterns = [
    # path('my-reviews/', ReviewListView.as_view(), name = 'my-review'),
    path('review/create/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-thread'),

    path('rating/create_update/', RatingCreateView.as_view(),
         name='rating-create_update'),
    path('rating/<int:pk>/', RatingDetailView.as_view(), name='rating-thread'),

]
