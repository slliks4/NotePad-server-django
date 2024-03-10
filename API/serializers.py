from rest_framework import serializers
from main_LOGICS .models import Notes
from main_AUTH .models import *


class Profile_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = User_profile
        fields = '__all__'

class User_serializers(serializers.ModelSerializer):
    
    profile = Profile_serializers()
    class Meta:
        model = User
        fields = '__all__'


class Notes_serializer(serializers.ModelSerializer):
    
    user_profile = Profile_serializers()
    class Meta:
        model = Notes
        fields = '__all__'