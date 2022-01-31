"""
This is a general service unit that holds business logic
associated with PROFILE models's fav, watch and watched attrs
"""
from profiling.validation import validate_lists
from rest_framework import status
from user.models import UserActivity
from profiling.utils import toggle

from django.contrib.contenttypes.models import ContentType


@validate_lists  # decorator for validating the the action user
def profile_favoritelist_logic(profile, media_instance, key, curr_user):
    """Checking if key is present in the favouritelist or not
    """
    if profile.favoritelist is not None:
        if key not in profile.favoritelist.keys():
            profile.favoritelist[key] = []
            profile.save()
            lst = profile.favoritelist[key]

        else:
            lst = profile.favoritelist[key]
    else:
        profile.favoritelist = {key: []}
        profile.save()
        lst = profile.favoritelist[key]

    """Adding/Removing movie instance from the list
    """
    resp = toggle(media_instance, lst, profile)

    if resp == 'add':
        # for adding user into the favorites of the media instance
        media_instance.favorites.add(curr_user)
        media_instance.save()
        return 'Media Added into favoritelist', status.HTTP_200_OK

    elif resp == 'rem':
        # for removing user from the favorites of the media instance
        media_instance.favorites.remove(curr_user)
        media_instance.save()
        return 'Media Removed from favoritelist', status.HTTP_200_OK
    else:
        return 'Problem with toggle', status.HTTP_400_BAD_REQUEST


@validate_lists  # decorator for validating the the action user
def profile_watchlist_logic(profile, media_instance, key, curr_user):
    """Checking if key is present in the watchlist or not
    """
    if profile.watchlist is not None:
        if key not in profile.watchlist.keys():
            profile.watchlist[key] = []
            profile.save()
            lst = profile.watchlist[key]

        else:
            lst = profile.watchlist[key]
    else:
        profile.watchlist = {key: []}
        profile.save()
        lst = profile.watchlist[key]

    """Adding/Removing movie instance from the list
    Also, adding/removing the user from the movie attrs list
    """
    resp = toggle(media_instance, lst, profile)

    if resp == 'add':
        # for adding user into the watch_list of the media instance
        media_instance.watch_list.add(curr_user)
        media_instance.save()
        return ('Media Added into watchlist', status.HTTP_200_OK)

    elif resp == 'rem':
        # for removing user from the watch_list of the media instance
        media_instance.watch_list.remove(curr_user)
        media_instance.save()
        return ('Media Removed from watchlist', status.HTTP_200_OK)
    else:
        return ('Problem with toggle', status.HTTP_400_BAD_REQUEST)


@validate_lists  # decorator for validating the the action user
def profile_watchedlist_logic(profile, media_instance, key, curr_user):
    """Checking if key is present in the wathced_list or not
    """
    if profile.watchedlist is not None:
        if key not in profile.watchedlist.keys():
            profile.watchedlist[key] = []
            profile.save()
            lst = profile.watchedlist[key]

        else:
            lst = profile.watchedlist[key]
    else:
        profile.watchedlist = {key: []}
        profile.save()
        lst = profile.watchedlist[key]

    """Adding/Removing movie instance from the list
    """
    resp = toggle(media_instance, lst, profile)
    if resp == 'add':
        # for adding user into the wathced_list of the media instance
        media_instance.watched_list.add(curr_user)
        media_instance.save()

        # for creating the user activity of the user for the wathced_list
        user_activity = UserActivity.objects.create_by_modeltype(
            model_type=key, pk=media_instance.id,
            user=curr_user, action='watched_list')

        return ('Media Added into watchedlist', status.HTTP_200_OK)

    elif resp == 'rem':
        # for removing user from the wathced_list of the media instance
        media_instance.watched_list.remove(curr_user)
        media_instance.save()

        # for removing the user activity of the user for the wathced_list
        model = ContentType.objects.filter(model=key).first()
        user_activity = UserActivity.objects.get(
            content_type=model, object_id=media_instance.id,
            user=curr_user, action='watched_list')
        user_activity.delete()

        return ('Media Removed from watchedlist', status.HTTP_200_OK)
    else:
        return ('Problem with toggle', status.HTTP_400_BAD_REQUEST)
