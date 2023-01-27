"""eventeger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users import views
from groups.views import GroupViewSet, MembersAPIView, MemberDetailsAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="API documentation",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@eventeger.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[TokenAuthentication]
)

router = routers.DefaultRouter()

router.register('groups', GroupViewSet)
router.register('get_users', views.ListUsersView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', views.CreateUserView.as_view(), name='create'),
    path('api/token/', views.CreateTokenView.as_view(), name='token'),
    path('api/me/', views.ManageUserView.as_view(), name='me'),
    path('api/groups/<int:group_id>/add_member/users/<int:user_id>/',
         MembersAPIView.as_view(), name='add_member'),
    path('api/groups/<int:group_id>/members/',
         MembersAPIView.as_view(), name='members'),
    path('api/groups/<int:group_id>/members/<int:user_id>/',
         MemberDetailsAPIView.as_view(), name='member_details'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
