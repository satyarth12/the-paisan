from django.contrib import admin
from rating_review.models.rating import Rating
from rating_review.models.review import Review

admin.site.register(Review)
admin.site.register(Rating)
