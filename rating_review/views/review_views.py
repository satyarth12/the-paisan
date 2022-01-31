from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from rating_review.models.review import Review
from rating_review.serializers.review_serializers \
    import (ReviewCreateSerializer,
            ReviewListSerializer,
            ReviewDetailSerializer)


class ReviewListView(generics.ListAPIView):
    """List each and every review made by the current user
    """
    serializer_class = ReviewListSerializer

    def get_queryset(self, *args, **kwargs):
        querylist = Review.objects.select_related(
            'user').filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            querylist = querylist.filter(
                Q(content__icontains=query)) .distinct()
        return querylist

    def get(self, *args):
        reviews = Review.objects.select_related(
            'user').filter(user=self.request.user)
        return Response(ReviewListSerializer(reviews, many=True).data)


class ReviewCreateView(generics.CreateAPIView):
    """Implements an endpoint for creating generic review System

    In form-data, the following key-value pair has to be passed:
    ``
    {'object_type':Name of the model on which review has to be made,
    'object_id':Instance id of that model,
    'parent_id':Review instance id, if it's a reply in the thread,
    'content':content}
    ``
    """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={'request': self.request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'success': True,
                'data': 'Review Created',
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'message': serializer.errors
            }
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ReviewDetailView(DestroyModelMixin,
                       UpdateModelMixin,
                       generics.RetrieveAPIView):
    queryset = Review.objects.filter(id__gte=0)
    serializer_class = ReviewDetailSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        """Implements an endpoint for updating a review

        In form-data, the following key-value pair has to be passed:
        ``
        {'content':content}
        ``

        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
