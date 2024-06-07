from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from api.models import Friends
from api.serializers import UserSerializer, FriendsSerializer

User = get_user_model()


class ListUserView(generics.ListAPIView):
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q')
        if search_keyword:
            if "@" in search_keyword:
                user = User.objects.filter(
                    email=search_keyword
                )
                return user
            else:
                users = User.objects.filter(
                    name__icontains=search_keyword
                )
                return users

        return User.objects.all()

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if not queryset.exists():
            return Response({'results': 'No results found.'})

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateFriendRequest(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendsSerializer
    queryset = Friends.objects.all()
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        sender_id = self.request.data.get('sender')
        if (Friends.objects.filter(sender=sender_id,
                                   receiver=receiver_id).exists()
                or Friends.objects.filter(sender=receiver_id,
                                          receiver=sender_id).exists()):
            raise ValidationError("Friend Request Already exists")
        serializer.save()


class UpdateFriendRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendsSerializer

    def post(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        type_request = request.data.get('type_request')

        friend_request = Friends.objects.get(sender=sender_id,
                                             receiver=receiver_id)
        if type_request == "Accept":
            friend_request.status = "Accepted"
        elif type_request == "Reject":
            friend_request.status = "Rejected"

        friend_request.save()

        return Response({"status": type_request}, status=status.HTTP_200_OK)


class ListAllAcceptedFriends(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            User.objects.get(id=request.data.get("sender"))
        except:
            return Response({"result": "User does not exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        sender = request.data.get("sender")
        if not sender:
            return Response({"result": "We cannot process your request as it"
                            " does not contain the necessary sender"
                                       " information required to retrieve the "
                                       "friend list."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Friends.objects.filter(Q(sender=sender) | Q(receiver=sender),
                                          status="Accepted")
        if not queryset.exists():
            return Response({"result": "No Accepted Friends"},
                            status=status.HTTP_200_OK)
        serializer = FriendsSerializer(queryset, many=True)
        return Response(serializer.data)


class ListAllPendingFriends(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            User.objects.get(id=request.data.get("receiver"))
        except:
            return Response({"result": "User does not exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        receiver = request.data.get("receiver")
        if not receiver:
            return Response({"result": "We cannot process your request as it"
                                      " does not contain the necessary sender"
                                      " information required to retrieve the"
                                      " friend list."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Friends.objects.filter(receiver=receiver, status="Pending")
        if not queryset.exists():
            return Response({"result": "No Pending Requests"},
                            status=status.HTTP_200_OK)
        serializer = FriendsSerializer(queryset, many=True)
        return Response(serializer.data)
