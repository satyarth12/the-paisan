from rest_framework import status
from rest_framework.response import Response


def validate_user(func):
    def wrapper(request, pk, *args, **kwargs):
        curr_user = int(request.user.id)

        if pk is not None and curr_user == int(pk):
            return func(request, pk, *args, **kwargs)

        elif request.user.id != pk:
            return Response({
                'success': False,
                'data': 'Forbidden action'
            },
               status=status.HTTP_403_FORBIDDEN)

    return wrapper


def validate_lists(func):
    def wrapper(profile, media_instance, key, curr_user):
        profile_user_id = profile.user.id

        if profile_user_id is not None \
                and profile_user_id == curr_user.id:
            return func(profile, media_instance, key, curr_user)

        elif profile_user_id != curr_user.id:
            return Response({
                'success': False,
                'data': 'Forbidden action'
            },
                status=status.HTTP_403_FORBIDDEN)

    return wrapper
