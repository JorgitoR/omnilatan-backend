"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator


# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from omnilatam.apps.user.models import User, Profile

# Serializers
from omnilatam.apps.user.api.serializers import ProfileModelSerializers

# Utilities
import jwt
from datetime import timedelta
from django.utils import timezone

# Email
from django.template.loader import render_to_string
from omnilatam.mail.email import send_mail_async as send_mail
from omnilatam.mail.settings_email import MTASKS_EMAIL_WITH_URL

class UserModelSerializer(serializers.ModelSerializer):
	"""User model serializer."""

	profile = ProfileModelSerializers(read_only=True)

	class Meta:
		"""Meta class."""

		model = User 
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'profile'
		)


class UserSignUpSerializer(serializers.Serializer):
	"""User sign up serializer.

	Handle sign up data validation and user/profile creation.
	"""

	email = serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
	username = serializers.CharField(
		min_length=4,
		max_length=20,
		validators=[UniqueValidator(queryset=User.objects.all())]
	)

	password = serializers.CharField(min_length=8, max_length=64)
	password_confirmation = serializers.CharField(min_length=8, max_length=64)

	first_name = serializers.CharField(min_length=2, max_length=30)
	last_name = serializers.CharField(min_length=2, max_length=30)

	def validate(self, data):
		"""Verify passsword match."""
		password = data['password']
		password_confirmation = data['password_confirmation']
		if password  != password_confirmation:
			raise serializers.ValidationError("Passwords don't match.")
		password_validation.validate_password(password)
		return data 

	def create(self, data):
		"""Handle user and profile creation."""
		data.pop("password_confirmation")
		user = User.objects.create_user(**data, is_verified=True, is_customer=True)
		Profile.objects.create(user=user)
		self.send_confirmation_email(user)
		return user

	def send_confirmation_email(self, user):
		"""Send account verification link to given user."""
		verification_token = self.get_verification_token(user)
		subject = 'Welcom @{} Verify your account to start using Comparte Ride'.format(user.username)
		from_email = 'E-commerce omnilatan <communitytask485@gmail.com>'
		content = render_to_string(
			'email/users/account_verification.html',
			{'token':verification_token, 'user':user}
		)

		values = {

				"id": verification_token,
				"usuario": user,
				"titulo": verification_token,
				"descripcion": 'token',
				"sign": 'Token',

		}

		send_mail(

				'Dev Django Nueva Tarea Creada',
				MTASKS_EMAIL_WITH_URL.format(**values),
				from_email,
				[user.email],

		)

	def get_verification_token(self, user):
		"""Create JWT token that allow user to verify the account."""

		exp_date = timezone.now() + timedelta(days=2)
		payload = {
			'user': user.username,
			'exp': int(exp_date.timestamp()),
			'type':'email confirmation'
		}

		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
		return token

class UserLoginSerializer(serializers.Serializer):
	"""User login serializer.

	Handle the login request data.
	"""

	username = serializers.CharField()
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		"""Check credentials."""
		user = authenticate(username=data['username'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Invalid credentials')
		if not user.is_verified:
			raise serializers.ValidationError('Acoount is not active yet.')
		self.context['user'] = user 
		return data

	def create(self, data):
		"""Generate or retrieve new Token."""
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key 

class AccountVerificationSerializer(serializers.Serializer):
	"""Account verification serializer."""

	token = serializers.CharField()

	