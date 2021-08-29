"""User Views."""

# Django REST Fremework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)

# Serializers
from omnilatam.apps.user.api.serializers import ProfileModelSerializers
from omnilatam.apps.user.api.serializers.user import (
	UserModelSerializer,
	UserSignUpSerializer, 
	UserLoginSerializer,
	AccountVerificationSerializer
)


# Models
from omnilatam.apps.user.models import User, Profile

# Authenticate
from django.contrib.auth import login, logout


class UserViewSet(mixins.RetrieveModelMixin,
				  mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):
	"""User view set

	Handle sign up, login and account verification
	"""

	queryset = User.objects.filter(is_active=True)
	serializer_class = UserModelSerializer
	lookup_field='username'


	@action(detail=False, methods=['post'])
	def login(self, request):
		"""User sign in."""
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		login(request, user)
		data = {
			'user':UserModelSerializer(user).data,
			'acces_token':token
		}

		return Response(data, status=status.HTTP_201_CREATED)
	
	@action(detail=False, methods=['get'])
	def logout(self, request):
		request.user.auth_token.delete()
		logout(request)
		return Response(status=status.HTTP_200_OK)

	@action(detail=False, methods=['post'])
	def signup(self, request):
		"""User sign up."""
		serializer = UserSignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def verify(self, request):
		"""Account verification"""
		serializer = AccountVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = {'message':'Congratulation, now go and buy anything!'}
		return Response(data, status=status.HTTP_200_OK)

	@action(detail=True, methods=['put', 'patch'])
	def profile(self, request, *args, **kwargs):
		"""Update profile data."""
		user = self.get_object()
		profile = user.profile
		partial = request.method == 'PATCH'
		serializer = ProfileModelSerializers(
			profile,
			data=request.data,
			partial=partial
		)
