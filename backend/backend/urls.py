"""backend URL Configuration

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
from django.urls import path
from django.urls import include

# noinspection PyUnresolvedReferences
from uflix import views

# import routers from the REST framework
# it is necessary for routing
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView

# create a router object
router = routers.DefaultRouter(trailing_slash=False)

# register the router
router.register(r'movies', views.MovieView, 'movie')
router.register(r'genres', views.GenreView)
router.register(r'comments', views.CommentView)

urlpatterns = [
    path('admin/', admin.site.urls),

    # add another path to the url patterns
    # when you visit the localhost:8000/api
    # you should be routed to the django Rest framework
    path('api/', include(router.urls)),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', views.RegisterView.as_view(), name="signup"),
    path('api/change_password/', views.ChangePasswordView.as_view(), name="change_password"),
    path('api/change_name/', views.ChangeNameView.as_view(), name="change_name"),
]
