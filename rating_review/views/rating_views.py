from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from rating_review.models.rating import Rating
from rating_review.serializers.rating_serializers \
    import (RatingCreateSerializer,
            RatingDetailSerializer)


class RatingCreateView(generics.CreateAPIView):
    """Implements an endpoint for creating generic Rating System

    In form-data, the following key-value pair has to be passed:
    ``
    {'object_type':Name of the model on which rating has to be made,
    'object_id':Instance id of that model,
    'stars':stars (int)}
    ``
    """
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={'request': self.request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'success': True,
                'data': 'Rating Created',
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'message': serializer.errors
            }
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RatingDetailView(DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Rating.objects.filter(id__gte=0)
    serializer_class = RatingDetailSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        """Implements an endpoint for updating a Rating

        In form-data, the following key-value pair has to be passed:
        ``
        {'stars':stars (int)}
        ``

        """

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
