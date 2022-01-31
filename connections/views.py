from celery.exceptions import InvalidTaskError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, views
from rest_framework import permissions
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from rest_framework import filters

from .serializers import (FriendRequestSerializer,
                          FriendsSerializer,
                          FriendActivitesSerializer)
from .models import FriendRequest, Friends
from user.models import UserActivity


User = get_user_model()


class FriendRequestViewSet(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['to_user']
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=False, methods=['GET'])
    def received_requests(self, request):
        """Implements an endpoint for seeing the
           received friend request to current user

        """
        user = request.user
        myRequests = FriendRequest.objects.select_related(
            'to_user').filter(to_user=user)
        response = FriendRequestSerializer(myRequests, many=True, context={
                                           'curr_user': self.request.user})
        return Response(response.data)

    @action(detail=False, methods=['GET'])
    def sent_requests(self, request):
        """Implements an endpoint for seeing the sent friend request by current user

        """
        user = request.user
        myRequests = FriendRequest.objects.select_related(
            'to_user').filter(from_user=user)
        response = FriendRequestSerializer(myRequests, many=True, context={
                                           'curr_user': self.request.user})
        return Response(response.data)

    @action(detail=True, methods=['POST'])
    def frequest_toggle(self, request, pk=None):
        """Implements an endpoint for sending/deleting the
        friend request send by current user

        ``
        id : ID of the user to whom request has to be send
        ``
        """
        current_user = self.request.user
        wanted_friend = User.objects.get(id=pk)
        if wanted_friend == current_user:
            return Response('Invalid Action', status=status.HTTP_409_CONFLICT)
        else:
            if Friends.objects.filter(user=current_user,
                                      friends_list=wanted_friend).exists():
                return Response('Already In Friend-List',
                                status=status.HTTP_409_CONFLICT)
            else:
                response = FriendRequest.toggle_request(
                    current_user, wanted_friend)
                return Response(response)

    @action(detail=True, methods=['POST'],
            url_path='(?P<operation>.+)/request')
    def accept_delete_request(self, request, operation, pk=None):
        """Implements an endpoint for accepting/deleting the friend request received

        The is API for the user who wants to accept/delete
        a friend request received
        ``
        Pass operation as "accept" for accepting request and
        "delete" for deleting request
        id : ID of a friend request
        ``
        """
        current_user = self.request.user

        try:
            fr_instance = FriendRequest.objects.get(
                id=pk, to_user=current_user)
            if operation == 'accept':
                accepted = Friends.add_friend(
                    current_user, fr_instance.from_user)
                fr_instance.delete()
                return Response(accepted)
            elif operation == 'delete':
                fr_instance.delete()
                return Response('Connection Request Removed')

        except InvalidTaskError:
            return Response('Invalid Request',
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def remove_friend(self, request, pk=None):
        """Implements an endpoint for removing a friend from friend list

        ``
        id : ID of the friend that has to be  removed
        ``
        """
        current_user = self.request.user
        friend_instance = get_object_or_404(User, id=pk)
        try:
            confirm_friend = Friends.objects.get(
                user=current_user, friends_list=friend_instance)
            if confirm_friend:
                unfriend = Friends.remove_friend(current_user, friend_instance)
                return Response(unfriend)
        except Exception:
            return Response('Cannot Perform this action',
                            status=status.HTTP_409_CONFLICT)


class FriendViewset(views.APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FriendsSerializer

    def get_queryset(self):
        return Friends.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        user = self.request.user
        friends = Friends.objects.prefetch_related('user').get(user=user)
        return Response(self.serializer_class(friends,
                        context={'curr_user': self.request.user}).data)


class FriendActivites(views.APIView):
    """
    This class for the getting the activities of the friends of a user
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        user = self.request.user
        user_friends = Friends.objects.get(user=user)
        friends_list = user_friends.friends_list.all()
        frnd_act = UserActivity.objects.filter(user_id__in=friends_list)
        return Response(FriendActivitesSerializer(frnd_act,
                                                  many=True).data)
