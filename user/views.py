from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import Member
from user.serializers import MemberSerializer


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        return Member.objects.all.filter(id=self.request.user.member.id)

    def create(self, request, *args, **kwargs):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['email']
            email = serializer.data['email']
            password = serializer.data['password']

            with transaction.atomic():
                django_user = User.objects.create_user(username, email, password)
                member = Member.objects.create(**serializer.data, django_user=django_user)
                return Response(member.id)

        return Response('/error')






