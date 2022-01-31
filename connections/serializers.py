from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from .models import FriendRequest, Friends
from user.serializers import UserSerializer
from user.models import UserActivity


class FriendRequestSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'to_user', 'from_user', 'created_on']

    def get_from_user(self, obj):
        curr_user = self.context['curr_user']
        return UserSerializer(obj.from_user,
                              context={'curr_user': curr_user}).data

    def get_to_user(self, obj):
        curr_user = self.context['curr_user']
        return UserSerializer(obj.to_user,
                              context={'curr_user': curr_user}).data


class FriendsSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    user = UserSerializer()
    friends_list = serializers.SerializerMethodField()

    class Meta:
        model = Friends
        fields = ['id', 'user', 'friends_list', 'updated_on']

    def get_friends_list(self, obj):
        curr_user = self.context['curr_user']
        return UserSerializer(obj.friends_list, many=True,
                              context={'curr_user': curr_user}).data


class FriendActivitesSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """
    This serializer module is for serializing the UserActivity model
    and getting all the required response
    """

    target = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'action', 'target']

    def get_target(self, obj):
        target_dict = {'type': str(obj.content_type.model_class()),
                       'id': obj.object_id}
        return target_dict
