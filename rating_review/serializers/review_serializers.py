from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rating_review.models.review import Review
User = get_user_model()


class ReviewCreateSerializer(serializers.ModelSerializer):
    object_type = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', "object_type", "object_id",
                  'parent', 'content', 'created_on')
        read_only_fields = [
            "user",
        ]
        ref_name = "Review Create"

    def validate(self, data):
        model_type = data.get('object_type')
        object_id = data.get('object_id')
        model_qs = ContentType.objects.filter(model=model_type)

        if not model_qs.exists() or model_qs.count() != 1:
            raise serializers.ValidationError(
                "This is not a valid content type")

        SomeModel = model_qs.first().model_class()
        obj_qs = SomeModel.objects.filter(id=object_id)

        if not obj_qs.exists() or obj_qs.count() != 1:
            raise serializers.ValidationError(
                "This is not the id for this content type")
        return data

    def create(self, validated_data):
        content = validated_data.get('content')
        user = self.context["request"].user
        object_type = validated_data.get('object_type')
        model_type_id = validated_data.get('object_id')
        parent_obj = validated_data.get('parent', None)

        if parent_obj:
            parent_qs = Review.objects.filter(id=parent_obj.id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        review = Review.objects.create_by_modeltype(
            model_type=object_type,
            pk=model_type_id,
            content=content,
            user=user,
            parent_obj=parent_obj)

        return review


class ReviewListSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(source='user')

    class Meta:
        model = Review
        # 'content_type', 'object_id', 'parent',
        fields = ('id', 'user', 'content', 'reply_count', 'created_on')

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_user(self, obj):
        return {
            'user_id': obj.user.id,
            'username': obj.user.username,
            'image': obj.user.profile.image_url

        }


class ReviewChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'content', 'created_on')


class ReviewDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(source='user')

    class Meta:
        model = Review
        fields = ('id', 'user', 'content', 'replies', 'reply_count',
                  'created_on', 'object_id')  # 'content_type', 'object_id',
        # 'content_type', 'object_id',
        read_only_fields = ('reply_count', 'replies', 'object_id')

    def get_replies(self, obj):
        if obj.is_parent:
            return ReviewChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_user(self, obj):
        return {
            'user_id': obj.user.id,
            'username': obj.user.username,
            'image': obj.user.profile.image_url

        }
