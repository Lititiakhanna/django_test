import os.path
from django.core.mail import send_mail
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer, LoginSerializer
from .serializers import LoginOperationalSerializer, LoginClientSerializer
from .models import UserProf, Login, LoginOperational, LoginClient


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializerr = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializerr.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user_type = serializerr.validated_data.get('user_type')
        password = serializer.validated_data.get('password')
        email_id = serializer.validated_data.get('email')
        user = serializer.save()
        entry = UserProf.objects.create(user=user, username=username, password=password, user_type=user_type)
        #send_mail('Email Verification', 'Your Email ID is successfully verified.', 'tishakhanna1111@gmail.com',
        #          [str(email_id)], fail_silently=False,)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            check_login = UserProf.objects.filter(username=username)

            if check_login:
                if check_login[0].password == password:
                    if check_login[0].user_type == "Client":
                        Login.objects.create(username=username, password=password)
                        return Response({"Success": True, "User_Type": "Client User"}, status=status.HTTP_200_OK)
                    else:
                        Login.objects.create(username=username, password=password)
                        return Response({"Success": True, "User_Type": "Operational User"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Success": False, "Message": "Incorrect Password"},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"Success": False, "Message": "Username doesn't exists, please register"},
                                status=status.HTTP_400_BAD_REQUEST)


class LoginOperationalAPI(generics.GenericAPIView):
    serializer_class = LoginOperationalSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginOperationalSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            fileop = serializer.validated_data.get('fileop')
            check_user = UserProf.objects.filter(username=username)

            if check_user[0].user_type == "Operational":
                entry = LoginOperational.objects.create(username=username, fileop=fileop)
                data = {
                    'success': True,
                    'data': {
                        'id': entry.id,
                        'username': entry.username,
                        'file_upload': True
                    }
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Success": False,
                                 "Message": "Only Operational User has the permission to upload the file"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginClientAPI(generics.GenericAPIView):
    serializer_class = LoginClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginClientSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            username_file_uploader = serializer.validated_data.get('username_file_uploader')
            check_user = UserProf.objects.filter(username=username)
            check_userr = UserProf.objects.filter(username=username_file_uploader)

            if check_user[0].user_type == "Client":
                if check_userr[0].user_type == "Operational":
                    check_file = LoginOperational.objects.filter(username=username_file_uploader)
                    if check_file:
                        entry = LoginClient.objects.create(username=username,
                                                           username_file_uploader=username_file_uploader)
                        data = {
                            'success': True,
                            'data': {
                                'id': entry.id,
                                'username': entry.username,
                                'file_download_link': "http://127.0.0.1:8000/media/media/" +
                                                      os.path.basename(check_file[0].fileop.name)
                            }
                        }
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"Success": False, "Message": "Operational User doesn't uploaded the file"},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Success": False, "Message": "Uploader is not an Operational User"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Success": False,
                                 "Message": "Only Client User has the permission to download the file"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
