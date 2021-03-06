'''
Local DB Authentication module.

.. moduleauthor:: Gerson Galang <gerson.galang@versi.edu.au>
.. moduleauthor:: Steve Androulakis <gerson.galang@versi.edu.au>
'''

import logging

from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend

from tardis.tardis_portal.auth.interfaces import AuthProvider, GroupProvider, UserProvider


logger = logging.getLogger(__name__)


auth_key = u'aaf'
auth_display_name = u'Australian Access Federation'


_modelBackend = ModelBackend()


class DjangoAuthBackend(AuthProvider):
    """Authenticate against Django's Model Backend.

    """

    def authenticate(self, request):
        pass

    def get_user(self, user_id):
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            user = None
        return user


class DjangoGroupProvider(GroupProvider):
    name = u'django_group'

    def getGroups(self, request):
        """return an iteration of the available groups.
        """
        groups = request.user.groups.all()
        return [g.id for g in groups]

    def getGroupById(self, id):
        """return the group associated with the id::

            {"id": 123,
            "display": "Group Name",}

        """
        groupObj = Group.objects.get(id=id)
        if groupObj:
            return {'id': id, 'display': groupObj.name}
        return None

    def searchGroups(self, **filter):
        result = []
        groups = Group.objects.filter(**filter)
        for g in groups:
            users = [u.username for u in User.objects.filter(groups=g)]
            result += [{'id': g.id,
                        'display': g.name,
                        'members': users}]
        return result


class DjangoUserProvider(UserProvider):
    name = u'django_user'

    def getUserById(self, id):
        """
        return the user dictionary in the format of::

            {"id": 123,
            "display": "John Smith",
            "email": "john@example.com"}

        """
        try:
            userObj = User.objects.get(username=id)
            return {'id': id, 'display': userObj.first_name + ' ' +
                    userObj.last_name, 'first_name': userObj.first_name,
                    'last_name': userObj.last_name, 'email': userObj.email}
        except User.DoesNotExist:
            return None


django_user = DjangoUserProvider.name
django_group = DjangoGroupProvider.name
