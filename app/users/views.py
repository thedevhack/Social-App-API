from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView, Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from users import serializers

User = get_user_model()


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSignUpSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(Q(email__iexact=email)).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": str(token), "status": "Successful Login"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
