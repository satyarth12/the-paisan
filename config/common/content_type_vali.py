from django.contrib.contenttypes.models import ContentType


def check_content_object(model_name, object_id):
    """
    This module will check for the valid content type model
    and for its object id
    """
    # content type
    model_qs = ContentType.objects.filter(model=model_name)
    if not model_qs.exists() or model_qs.count() != 1:
        return False

    # object id
    SomeModel = model_qs.first().model_class()
    obj_qs = SomeModel.objects.filter(id=object_id)
    if not obj_qs.exists() or obj_qs.count() != 1:
        return False

    # returning data for the usage
    content_type = model_qs.first()
    object_id = obj_qs.first().id
    return content_type, object_id
