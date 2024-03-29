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
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users import views
from groups.views import (
    GroupViewSet,
    AddMembersAPIView,
    MemberDetailsAPIView,
    ImageAPIView, ListMembersAPIView,
)
from events.views import EventAPIViewSet, EventAPIView


router = routers.DefaultRouter()

router.register('groups', GroupViewSet)
router.register('get_users', views.ListUsersView)
router.register(r'group/(?P<group_pk>\d+)/events',
                EventAPIViewSet, basename='event')


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', views.CreateUserView.as_view(), name='create'),
    path('api/token/', views.CreateTokenView.as_view(), name='token'),
    path('api/group/<int:group_id>/add_image/', ImageAPIView.as_view()),
    path('api/group/<int:group_id>/images/<int:image_id>/',
         ImageAPIView.as_view()),
    path('api/me/', views.ManageUserView.as_view(), name='me'),
    path('api/groups/<int:group_id>/add_member/users/<int:user_id>/',
         AddMembersAPIView.as_view(), name='add_member'),
    path('api/groups/<int:group_id>/members/',
         ListMembersAPIView.as_view(), name='members'),
    path('api/groups/<int:group_id>/members/<int:user_id>/',
         MemberDetailsAPIView.as_view(), name='member_details'),
    path('api/group/<int:group_id>/add_event/',
         EventAPIView.as_view(), name='add_event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
