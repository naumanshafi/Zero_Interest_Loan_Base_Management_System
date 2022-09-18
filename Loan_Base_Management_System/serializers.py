from rest_framework.serializers import ModelSerializer
from Committee.models import userInfo


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = userInfo
        fields = [
            'FullName', 'Email', 'Username', 'City', 'Password', 'ProfilePicture', ]


class LoginSerializer(ModelSerializer):
    class Meta:
        model = userInfo
        fields = [
            'Email', 'Password', ]


class UpdateUserSerialzer(ModelSerializer):
    class Meta:
        model = userInfo
        fields = [
            'FullName', 'Username', 'City', 'Password', 'ProfilePicture'
        ]
