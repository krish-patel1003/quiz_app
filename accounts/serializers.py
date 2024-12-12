from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib import auth
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'is_admin', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def validate(self, attrs):
        '''
        validate method - validates the instance passed to the serializer
        '''

        username = attrs.get('username', None)

        if not username:
            raise serializers.ValidationError("Username is required")

        if not username.isalnum():
            raise serializers.ValidationError("Username should be alphnumeric")
        
        return attrs
    

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    '''
    Login serializer
    '''
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(min_length=1, write_only=True)
    token = serializers.SerializerMethodField()
    
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'token')

    def get_token(self, obj):
        user = CustomUser.objects.get(username=obj['username'])
        token = Token.objects.get(user=user)
        return token.key

    def validate(self, attrs):
        '''
        validate method - validates the instance passed to the serializer
        '''

        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account Disabled, contact admin')

        return attrs
