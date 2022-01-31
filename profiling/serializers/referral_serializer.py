from rest_framework import serializers
from profiling.models.referral import ReferralSystem
from user.serializers import UserSerializer


class ReferralSystemSerializer(serializers.ModelSerializer):
    my_referred_users = serializers.SerializerMethodField()
    referred_by = serializers.SerializerMethodField()

    class Meta:
        model = ReferralSystem
        fields = "__all__"

    def get_my_referred_users(self, obj):
        return UserSerializer(obj.my_referred_users, many=True).data

    def get_referred_by(self, obj):
        return UserSerializer(obj.referred_by, many=True).data
