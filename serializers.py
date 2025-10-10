from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from email_validator import validate_email, EmailNotValidError
from .models import CustomHost


class HostRegistrationSerializer(serializers.ModelSerializer):
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
        model = CustomHost
        fields = (
            'username', 'email', 'full_name', 'phone_number', 
            'business_name', 'business_license', 'business_type',
            'address', 'city', 'state', 'country', 'postal_code',
            'bio', 'password', 'password_confirm'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'full_name': {'required': True},
            'phone_number': {'required': True},
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
        if CustomHost.objects.filter(email=value).exists():
            raise serializers.ValidationError("A host with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        host = CustomHost.objects.create_user(**validated_data)
        host.set_password(password)
        host.save()
        return host


class HostLoginSerializer(serializers.Serializer):
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
            try:
                host = CustomHost.objects.get(email=email)
                if host.check_password(password):
                    if not host.is_active:
                        raise serializers.ValidationError('Host account is disabled.')
                    vald['host'] = host
                    return vald
                else:
                    raise serializers.ValidationError('Invalid email or password.')
            except CustomHost.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Must include email and password.')


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomHost
        fields = (
            'id', 'username', 'email', 'full_name', 'phone_number',
            'business_name', 'business_license', 'business_type',
            'address', 'city', 'state', 'country', 'postal_code',
            'is_verified', 'bio', 'profile_image', 'date_joined', 'is_active'
        )
        read_only_fields = ('id', 'date_joined', 'is_active', 'is_verified')


class HostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomHost
        fields = (
            'full_name', 'phone_number', 'business_name', 'business_license',
            'business_type', 'address', 'city', 'state', 'country', 
            'postal_code', 'bio', 'profile_image'
        )

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class ChangeHostPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, vald):
        if vald['new_password'] != vald['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return vald

    def validate_old_password(self, value):
        host = self.context['request'].user
        if not host.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value