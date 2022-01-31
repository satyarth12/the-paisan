from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .models import Recommendation
from .serializers import (create_recommendation_serializer,
                          RecommendationListSerializer)

User = get_user_model()


class RecommendationCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recommendation.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """Implements an endpoint for creating generic recommendation System

        In query parameters, the following key-value pair has to be passed:
        ``
        {'type':Name of the model, 'pk':Instance id of that model}
        ``

        """
        model_type = self.request.GET.get('type')
        object_id = self.request.GET.get('pk')

        return create_recommendation_serializer(
            model_type=model_type,
            object_id=object_id)


class RecommendationListView(viewsets.ViewSet):
    serializer_class = RecommendationListSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['GET'])
    def received_recommendation(self, *args):
        """List each and every recommendation received to the current user
        """
        reviews = Recommendation.objects.select_related(
            'to_user').filter(to_user=self.request.user)
        if reviews:
            return Response(RecommendationListSerializer(
                            reviews, many=True,
                            context={'curr_user': self.request.user}).data)
        return Response('No Recommendation received yet',
                        status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def sent_recommendation(self, *args):
        """List each and every recommendation sent by the current user
        """
        reviews = Recommendation.objects.select_related(
            'from_user').filter(from_user=self.request.user)
        if reviews:
            return Response(RecommendationListSerializer(
                            reviews, many=True,
                            context={'curr_user': self.request.user}).data)
        return Response('No Recommendation sent yet',
                        status=status.HTTP_404_NOT_FOUND)
