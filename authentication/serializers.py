from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from email_validator import validate_email, EmailNotValidError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
            'blank': 'Email address cannot be blank.'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone_number', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True},
            'full_name': {'required': True},
        }

    def validate(self, vald):
        if vald['password'] != vald['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return vald

    def validate_email(self, value):
        # Normalize email to lowercase
        value = value.lower().strip()
        
        try:
            # Use email-validator for robust validation
            validated_email = validate_email(value)
            value = validated_email.email  # Get the normalized email
        except EmailNotValidError as e:
            raise serializers.ValidationError(f"Please enter a valid email address: {str(e)}")
        
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
            'blank': 'Email address cannot be blank.'
        }
    )
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Normalize email to lowercase for consistent login
        value = value.lower().strip()
        
        try:
            # Use email-validator for robust validation
            validated_email = validate_email(value)
            value = validated_email.email  # Get the normalized email
        except EmailNotValidError as e:
            raise serializers.ValidationError(f"Please enter a valid email address: {str(e)}")
        
        return value

    def validate(self, vald):
        email = vald.get('email')
        password = vald.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            vald['user'] = user
            return vald
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone_number', 'date_joined', 'is_active')
        read_only_fields = ('id', 'date_joined', 'is_active')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'phone_number')

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, vald):
        if vald['new_password'] != vald['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return vald

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value