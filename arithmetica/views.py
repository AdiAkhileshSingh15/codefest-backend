from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, authentication
from rest_framework.views import APIView
from .models import *
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied


# Create your views here.
class UserInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.validated_data


class UserInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "pk"

    def get_queryset(self):
        return UserInfo.objects.filter(id=self.kwargs.get("pk"))

    def perform_update(self, serializer):
        if self.get_queryset().first().user != self.request.user:
            raise PermissionDenied(
                detail="You are not slloed to update other users info"
            )
        serializer.save(user=self.request.user)
        return serializer.validated_data


class RoundInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    # def perform_create(self, serializer):
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return serializer.validated_data


class RoundInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "round_number"

    def get_queryset(self):
        return RoundInfo.objects.filter(round_number=self.kwargs.get("round_number"))


class ErrorInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        round_number = self.request.data.get("round_number")
        round = RoundInfo.objects.filter(round_number=round_number)
        if not round.exists():
            raise ParseError(detail="Round does not exist")

        u_info = UserInfo.objects.filter(user=self.request.user)
        if not u_info.exists():
            raise ParseError(detail="User not registered for contest")
        serializer.is_valid(raise_exception=True)
        serializer.save(user_info=u_info.first(), round=round.first())
        return serializer.validated_data


class ErrorInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    lookup_field = "round"

    def get_queryset(self):
        return ErrorInfo.objects.filter(
            round__round_number=self.kwargs.get("round"),
            user_info__user=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data
