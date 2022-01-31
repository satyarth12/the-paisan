from profiling.serializers.referral_serializer import ReferralSystemSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from oauth2_provider.views import TokenView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import json

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from profiling.models.referral import ReferralSystem
from .serializers import RegisteredUserSerializer, UserSerializer
from .services import register_user, invite_code_logic


User = get_user_model()


class customAuthToken(ObtainAuthToken):
    # permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user.id})


class RegisterUserViewSet(generics.CreateAPIView):

    serializer_class = RegisteredUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, **kwargs):
        """Implements an endpoint for registering a user
        """
        username = self.request.data.get('username')
        email = self.request.data.get('email', None)
        password = self.request.data.get('password')

        if username and password:
            serializer = self.serializer_class(
                data={'username': username,
                      'email': email,
                      'password': password})
            serializer.is_valid(raise_exception=True)
            register_user(**serializer.validated_data)

            url, headers, body, status_code = TokenView().create_token_response(request)
            return Response(json.loads(body), status=status_code)


class ReffView(viewsets.ViewSet):
    serializer_class = ReferralSystemSerializer

    def get_queryset(self):
        user = self.request.user
        return ReferralSystem.objects.prefetch_related('user').filter(user=user)

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['ref_code'],
        properties={
            'ref_code': openapi.Schema(type=openapi.TYPE_STRING),
        },
        description='Referral Code of the user by whom you are being referred'
    ))
    @action(detail=False, methods=['post'])
    def enter_invite_code(self, *args, **kwargs):
        """Implements an endpoint to take the invitation code

        ``{'ref_code': code}``
        This is the key-value pair that should be passed.

        """
        code = str(self.request.data.get('ref_code'))

        if code:
            result = invite_code_logic(code, self.request.user)
            return Response(result[0], status=result[1])

        return Response('Something wrong with the code',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_referral_data(self, request, pk=None):
        """Implements an endpoint to get referral data of the current user

        """
        ref = ReferralSystem.objects.get(user=self.request.user)
        return Response(ReferralSystemSerializer(ref).data)

    @action(detail=False, methods=['get'])
    def my_referrals(self, request):
        """Implements an endpoint for getting the total referrals of current user

        """
        ref = ReferralSystem.objects.get(user=self.request.user)
        my_refs = ref.get_referred_profiles
        return Response(UserSerializer(my_refs, many=True).data)


class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication, IsUserOrReadOnly)
    serializer_class = UserSerializer
    http_method_names = ['get', 'delete', 'put', 'patch']

    # @method_decorator(cache_page(CACHE_TTL))
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({"curr_user": self.request.user})
        return context
