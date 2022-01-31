from django.shortcuts import get_object_or_404
from movie_tv.models import TV, Movie
import uuid


def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:3]
    return code


def media_key_check(pk, type=None):
    """
    This module will check and return the key present in the json file
    (fav, watch, watched).
    """
    type = type.lower()

    if type == 'movies' or type == 'movie':
        media_instance = get_object_or_404(Movie, id=pk)
        key = "movie"
        return media_instance, key
    elif type == 'tv_shows' or type == 'tv_show' or type == 'tv':
        media_instance = get_object_or_404(TV, id=pk)
        print(media_instance)
        key = "tv_show"
        return media_instance, key
    else:
        return False


def toggle(media_instance, lst, profile):
    """
    This module will add/remove the objects in the json file
    (fav, watch, watched).
    """
    if media_instance.id in lst:
        lst.remove(media_instance.id)
        profile.save()
        return 'rem'
    else:
        lst.append(media_instance.id)
        profile.save()
        return 'add'
