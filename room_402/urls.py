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
from room_app import views
# 'get':'retrive','put':'update','delete':'destroy'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('reservation/',views.ReservationView.as_view({'get':'list','post':'create'})),
    path('cancel/',views.CancelView.as_view({'get':'list'})),
    path('cancel/<int:pk>',views.CancelView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('sign/',views.SignInAndOutView.as_view()),
    path('feedback/',views.FeedbackView.as_view()),
    path('dsyfunc/',views.DsyfuncView.as_view()),
]
