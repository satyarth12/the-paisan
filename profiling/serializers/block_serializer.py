from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiling.models.block import Block

USER = get_user_model()


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['user', 'blocked_user', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, attrs):
        blocked_by = self.context["request"].user
        blocked_user = attrs.get('blocked_user')

        # making sure user cannot report/block themselves
        if blocked_by.id == blocked_user.id:
            raise serializers.ValidationError('Invalid Action')

        return attrs

    def create(self, validated_data):
        blocked_by = self.context["request"].user
        blocked_user = validated_data.get('blocked_user')
        instance = Block.block_object(
            blocked_by=blocked_by, blocked_user=blocked_user)

        return instance
