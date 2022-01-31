# from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model

from config.common.content_type_vali import check_content_object
from profiling.models.report import Report
User = get_user_model()


class ReportCreateSerializer(serializers.ModelSerializer):
    # an extra input for the model_type
    object_type = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = (
            "id",
            "user",
            "object_type",
            "object_id",
            "category",
            "description",
        )

        read_only_fields = [
            "user",
        ]
        ref_name = "Report Create"

    def get_model_type(self, obj):
        return str(obj.content_type.model_class())

    def validate(self, data):
        object_type = data.get('object_type')
        object_id = data.get('object_id')

        curr_user = self.context["request"].user

        # making sure user cannot report/block themselves
        if curr_user.id == object_id:
            raise serializers.ValidationError('Invalid Action')

        # will check for content type and object ID to be valid
        check_result = check_content_object(
            model_name=object_type, object_id=object_id)
        if bool(check_result):
            pass
            # c_type, o_id = check_result[0], check_result[1]
        else:
            raise serializers.ValidationError(
                'Invalid object type or object ID')

        # # to check that when was the last report made
        # try:
        #     last_report = Report.objects.filter(user_1=curr_user,
        #                                         content_type=c_type,
        #                                         object_id=o_id).latest('id')
        # except Exception:
        #     last_report = None

        # if last_report:
        #     """
        #     Preventing the user to report the same ID again in span of 7 days
        #     """
        #     delta_days = datetime.date.today() - last_report.created_at.date()
        #     if int(delta_days.days) < 7:
        #         raise serializers.ValidationError(
        #             'Cannot report this ID now. Report time is not expired')

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        category = validated_data.get("category")
        description = validated_data.get("description")
        object_type = validated_data.get('object_type')
        model_type_id = validated_data.get('object_id')

        # # will create the auto block object for the appuser
        # if object_type == 'USER':
        #     model_qs = ContentType.objects.filter(model=object_type)
        #     SomeModel = model_qs.first().model_class()

        #     blocked_user = SomeModel.objects.get(id=model_type_id)
        #     block_instance = Block.block_object(
        #         blocked_by=user_1, blocked_user=blocked_user)
        #     return block_instance

        # will create a report instance
        report_instance = Report.objects.create_by_modeltype(
            model_type=object_type,
            model_type_instance_id=model_type_id,
            user=user,
            category=category,
            description=description
        )
        return report_instance
