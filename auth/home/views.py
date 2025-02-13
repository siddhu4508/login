from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class StudentApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "data": serializer.data
            }
        )


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "data": serializer.errors
                })
        username = serializer.data['username']
        password = serializer.data['password']

        user_obj = authenticate(username = username, password = password)
        if user_obj:
            token , _ = Token.objects.get_or_create(user=user_obj)
            return Response({
                "status": True,
                "data": {'token':str(token)}
            })
        return Response({
            "status": False,
            "data": {},
            "message": "Invalid credentials"
        })
