"""
This is a general service unit that holds business logic
associated with PROFILE models's interest attr
"""


def profile_interest_logic(profile, key=None, interest_instance=None):
    key = key.lower()

    # to check if the interests dict is none.
    # if none then create a key and if not none then get that key value
    if profile.interests is not None:
        if key not in profile.interests.keys():
            profile.interests[key] = []
            profile.save()

    else:
        profile.interests = {key: []}
        profile.save()

    # check if the list of that interest key is not more than 5
    if len(interest_instance) <= 5:  # 4 because list index starts from 0

        profile.interests[key] = interest_instance
        profile.save()
        return 'updated'

    else:
        return 'exceeded'
