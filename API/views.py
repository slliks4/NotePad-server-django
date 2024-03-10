from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.urls import reverse_lazy
from .serializers import Notes_serializer,User_serializers
from main_LOGICS .models import Notes
from main_AUTH.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def Endpoints(request):
    data = {
        'token [POST]' : '/token/',
        'refresh token [POST]' : '/token/refresh/',
        'create [POST]' : '/create_user/',
        '':'',
        'TOKEN REQUIRED':'MUST BE AUTHENTICATED',
        'userdetail [GET, PUT, DELETE]' : '/user_detail/',
        'user notes [GET, POST]':'/notes/',
        'user note_detail [GET, PUT, DELETE]' : '/note_detail/noteid/noteslug'
    }

    return Response(data)

@api_view(['POST'])
def Create_user(request):  
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            confirm_passowrd = request.data.get('confirm_password')

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return Response({'error': 'User with that username or email already exists'}, status=400)

            if password != confirm_passowrd:
                return Response ({'error' : 'password mismatch'}, status=400)
            
            try:
                validate_password(password)

            except ValidationError as validation_error:
                return Response({'error': validation_error.messages}, status=400)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password = password
            )

            serializer = User_serializers(user, many = False)
            return Response (serializer.data, status = 201)
        
        except Exception as error:
            return Response ({'error': str(error)}, status=400)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def User_detail(request):
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'GET':
        serializer = User_serializers(user, many = False)
        return Response (serializer.data, status=200)
    
    if request.method == 'PUT':
        try:
            username = request.data.get('username', user.username)
            email = request.data.get('email', user.email)
            password = request.data.get('password', None)
            first_name = request.data.get('first_name', user.first_name)
            last_name = request.data.get('last_name', user.last_name)

            if username != user.username and User.objects.filter(username=username).exists():
                return Response ({'error' : 'User with that username already exists'}, status=400)
            
            if email != user.email and User.objects.filter(email=email).exists():
                return Response ({'error' : 'User with that email already exists'}, status=400)            

            if (
                username == user.username and 
                email == user.email and 
                password is None and 
                first_name == user.first_name and 
                last_name == user.last_name 
            ):
                return Response ({'error': 'no changes made'}, status=400)
                         
            if password:
                try:
                    validate_password(password)
                except ValidationError as validation_error:
                    return Response({'error': validation_error.messages}, status=400)
                user.set_password(password)
            
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            
            user.save()

            serializer = User_serializers(user, many = False)
            return Response (serializer.data, status = 200)
        
        except Exception as error:
            return Response ({'error': str(error)}, status=400)

    if request.method == 'DELETE':
        user.delete()
        return HttpResponseRedirect(reverse_lazy('user_list'))

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def All_notes(request):
    user = get_object_or_404(User, id=request.user.id)
    user_profile = get_object_or_404(User_profile, user=user)
    query = request.GET.get('query', '')
    if request.method == 'GET':
        notes = Notes.objects.filter( Q(user_profile=user_profile) & (Q(heading__icontains=query) | Q(body__icontains = query)))
        serializer = Notes_serializer(notes, many = True)
        return Response (serializer.data)
    
    if request.method == 'POST':
        try:
            heading = request.data.get('heading')
            sub_heading = request.data.get('sub_heading', '')
            body = request.data.get('body', '')
            status = request.data.get('status')

            if status not in ['draft', 'published', '']:
                return Response({'error': 'invalid status'}, status=400)
            if heading == '':
                return Response({'error': 'Heading can not be blank'}, status=400)
            note = Notes.objects.create(
                user_profile = user_profile,
                heading = heading,
                sub_heading = sub_heading,
                body = body,
                status = status
            )

            serializer = Notes_serializer(note, many=False)
            return Response(serializer.data, status=201)
        
        except Exception as error:
            return Response ({'error': str(error)}, status=400)

    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def Note_detail(request,noteid,noteslug):
    user = get_object_or_404(User, id=request.user.id)
    note = get_object_or_404(Notes, user_profile = user.profile, id=noteid, slug=noteslug)
    if request.method == 'GET':
        serializer = Notes_serializer(note, many = False)
        return Response (serializer.data)

    if request.method == 'PUT':
        try:
            heading = request.data.get('heading', note.heading)
            sub_heading = request.data.get('sub_heading', note.sub_heading)
            body = request.data.get('body', note.body)
            status = request.data.get('status', note.status)

            if (
                heading == note.heading and 
                sub_heading == note.sub_heading and 
                body == note.body and 
                status == note.status
            ) :
                return Response ('no changes made', status= 400)
            
            if status not in ['draft', 'published', '']:
                return Response ('error: invalid status', status=400)
            
            note.heading = heading
            note.sub_heading = sub_heading
            note.body = body
            note.status = status
            note.save()

            serializer = Notes_serializer(note, many = False)
            return Response(serializer.data, status=200)
        
        except Exception as error:
            return Response ({'error': str(error)}, status=400)
    
    if request.method == 'DELETE':
        note.delete()
        return Response(f"{note.heading} deleted successfully")