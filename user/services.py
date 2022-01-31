"""
This is a general unit that holds business logic associated with USER app
"""
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User
from profiling.models.referral import ReferralSystem


def register_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    Token.objects.create(user=user)
    return user


def invite_code_logic(code, current_user):
    try:
        # gets the instance of the ref who invited the curr user
        referal_instance = ReferralSystem.objects.get(code=code)
        curr_user_ref_instance = ReferralSystem.objects.get(
            user=current_user)

        if not curr_user_ref_instance.referred_by:
            if referal_instance.invites < 6:
                referal_instance.my_referred_users.add(
                    current_user)
                referal_instance.invites += 1
                referal_instance.save()

                curr_user_ref_instance.referred_by = referal_instance.user
                curr_user_ref_instance.save()

                return ('Congratulations! Bingeman is unlocked for you.', status.HTTP_200_OK)
            return ('You have reached the maximum invites limit', status.HTTP_409_CONFLICT)
        return ('You have already been registered through the code', status.HTTP_409_CONFLICT)

    except ReferralSystem.DoesNotExist:
        return ('Invalid Invite Code', status.HTTP_404_NOT_FOUND)
