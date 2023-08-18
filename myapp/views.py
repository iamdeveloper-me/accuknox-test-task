from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, FriendSerializer, UserSearchSerializer, FriendRequestSerializer
from django.contrib.auth import authenticate,login
from .models import User, FriendRequest
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email').lower()
            password = request.data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e :
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSearchView(APIView):
    class UserSearchPagination(PageNumberPagination):
        page_size = 10

    @method_decorator(login_required)
    def get(self, request):
        try:
            search_keyword = request.query_params.get('search')
            users = User.objects.none()

            if search_keyword:
                users = User.objects.filter(
                    Q(email__iexact=search_keyword) |
                    Q(first_name__icontains=search_keyword)
                )

            paginator = self.UserSearchPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            serializer = UserSearchSerializer(paginated_users, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e :
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendRequestView(APIView):
    def post(self, request):
        try:
            receiver_id = request.data.get('recepient')
            if not User.objects.filter(id=receiver_id).exists():
                return Response({'message': 'Receiver does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.is_authenticated:
                sender = request.user

            '''
            Handling the User can not send more than 3 friend requests within a minute.
            '''
            
            cache_key = f'friend_request_attempt:{request.user.id}'
            attempts = cache.get(cache_key, 0)
            if attempts >= 3:
                return Response({'error': 'You have reached the friend request limit.'}, status=400)

            cache.set(cache_key, attempts + 1, timeout=60)

            if sender is None:
                return Response({'message': 'You need to be authenticated to send friend requests'}, status=status.HTTP_401_UNAUTHORIZED)

            if FriendRequest.objects.filter(sender=sender, recepient=receiver_id, status='pending').exists():
                return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.data['sender'] = request.user.id
            serializer = FriendRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=sender, status='pending')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e :
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RespondToRequestView(APIView):
    def post(self, request, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(
                id=friend_request_id, recepient=request.user, status='pending')
            action = request.data.get('action')
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
            else:
                return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Action successful'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AcceptedRequestListView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        try:
            authenticated_user = request.user
            friends = FriendRequest.objects.filter(
                status='accepted',
                sender=authenticated_user
            )
            serializer = FriendSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PendingRequestsView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        try:
            pending_requests = FriendRequest.objects.filter(recepient=request.user, status='pending')
            serializer = FriendRequestSerializer(pending_requests, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error': f'{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
