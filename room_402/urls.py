"""
URL configuration for room_402 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from reservation import views
from user.views import sign, login
# 导入 simplejwt 提供的几个验证视图类
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
# 'get':'retrive','put':'update','delete':'destroy'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('reservation/',views.ReservationView.as_view({'get':'list','post':'create'})),
    path('cancel/',views.CancelView.as_view({'get':'list'})),
    path('cancel/<int:pk>',views.CancelView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('sign/',views.SignInAndOutView.as_view()),
    path('feedback/',views.FeedbackView.as_view()),
    path('dsyfunc/',views.DsyfuncView.as_view()),
    path('sign/',views.SignInAndOutView.as_view({'get':'list'})),
    path('sign/<int:pk>',views.SignInAndOutView.as_view({'put':'update'})),
    path('api/sign/',sign.SignView.as_view()),
    # 获取Token的接口
    path('api/login/', login.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
