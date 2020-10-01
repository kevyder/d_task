from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Authorization token serializer"""

    email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)

        if not user:
            raise serializers.ValidationError("Unable to authenticate", code="authentication")

        attrs["user"] = user
        return attrs
