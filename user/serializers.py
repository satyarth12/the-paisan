from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from connections.models import FriendRequest, Friends
import re
from .models import User


class RegisteredUserSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True}, 'email': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username)

        # Checking if the user already exists
        if user.exists():
            raise serializers.ValidationError("Username is taken.")

        # checking if email is valid and unique
        if email:
            if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
                if user.email == email:
                    raise serializers.ValidationError("Email is taken.")
                raise serializers.ValidationError("Email is invalid.")

        return data


class UserSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    user_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'user_status']

    def get_user_status(self, obj):
        curr_user = self.context['curr_user']

        """
        This module will be checking for following contraints to show the user_status :
        1: If the friend_obj exists then they ARE friends

        2. If friend_obj doesn't exist along with any sent_request and received_request, then they ARE NOT friends.
        
        3. If sent_request exists then the current user has SENT a friend request from the obj.user

        4. If received_request exists then the current user has RECEIVED a friend request from the obj.user
        """

        if obj != curr_user:
            sent_request = FriendRequest.objects.select_related(
                'from_user').filter(from_user=curr_user, to_user=obj)
            received_request = FriendRequest.objects.select_related(
                'to_user').filter(from_user=obj, to_user=curr_user)
            friend_obj = Friends.objects.filter(
                user=curr_user, friends_list=obj)

            if friend_obj.exists():
                return 'Friends'
            elif not friend_obj.exists() and sent_request.exists() and received_request.exists():
                return 'Not Friends'
            elif sent_request.exists():
                return 'Connection Request Sent'
            elif received_request.exists():
                return 'Connection Request Received'
        else:
            return 'Current User'
