from django.db import models
from django.contrib.auth import get_user_model
from utils.models import Timestamps

User = get_user_model()


class FriendRequest(Timestamps):

    """This class is use to send the request by one user to another user.

    Parameters:

    to_user (ForeignKey): Stores the instance of a user,
            to whom the request is send.
    from_user (ForeignKey):
            Stores the instance of a user, by whom the request is send

    """

    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)

    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return "from {}, to {}".format(self.from_user.username,
                                       self.to_user.username)

    @classmethod
    def toggle_request(cls, current_user, friend):
        '''
        Using classemthod because, If you want to access a property of a
        class as a whole, and not the property of a specific instance
        of that class, use a class method.
        '''
        obj, created = cls.objects.get_or_create(
            to_user=friend, from_user=current_user)

        if created:
            return 'Sent Connection Request'
        else:
            obj.delete()
            return 'Connection Request Deleted'


class Friends(Timestamps):

    """This class stores the data of the connections between two users

    Parameters:

    user (ForeignKey): Stores the instance of a user,
            who holds other users as his/her connection.
    friends_list (ManyToManyField): Stores the list of users
            who are friends with the main holding user.

    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='owner')
    friends_list = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.user.username}'

    @classmethod
    def add_friend(cls, current_user, friend):
        # for creating the friend model of the current user
        obj, created = cls.objects.get_or_create(user=current_user)
        # for creating the friend model of the friend
        obj2, created2 = cls.objects.get_or_create(user=friend)

        # for adding the friend into the friends_list of current_user
        obj.friends_list.add(friend)
        # for adding the current_user into the friends_list of friend
        obj2.friends_list.add(current_user)
        return 'Friend Request Accepted'

    @classmethod
    def remove_friend(cls, current_user, friend):

        obj, created = cls.objects.get(user=current_user)
        obj2, created2 = cls.objects.get(user=friend)

        # removing the friend from the friends_list of the current_user
        obj.friends_list.remove(friend)
        # removing the current_user from the friends_list of the friend
        obj2.friends_list.remove(current_user)
        return 'Friend Removed from friend list'
