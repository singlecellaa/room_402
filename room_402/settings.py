"""
Django settings for room_402 project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qbobtp%2^=e_n01om04^-xx*i!ff3m#(tqkyt8@&gk8fpc#)!('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'room_app.apps.RoomAppConfig',
    'user'
]

# 修改DRF认证
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 使用rest_framework_simplejwt(token)验证身份
        'rest_framework.authentication.SessionAuthentication',  # 基于用户名密码认证方式
        'rest_framework.authentication.BasicAuthentication'  # 基于Session认证方式
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'  # 默认权限为验证用户
    ],
}
# 修改simplejwt
# simplejwt配置， 需要导入datetime模块
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),  # 访问令牌的有效时间
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),  # 刷新令牌的有效时间

    'ROTATE_REFRESH_TOKENS': False,  # 若为True，则刷新后新的refresh_token有更新的有效时间
    'BLACKLIST_AFTER_ROTATION': True,  # 若为True，刷新后的token将添加到黑名单中,
    # When True,'rest_framework_simplejwt.token_blacklist',should add to INSTALLED_APPS

    'ALGORITHM': 'HS256',  # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,  # if signing_key, verifying_key will be ignore.
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    'USER_ID_FIELD': 'id',  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    'USER_ID_CLAIM': 'user_id',
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTH_USER_MODEL = 'room_app.User'

CORS_ALLOW_CREDENTIALS = True  # 允许跨域时携带Cookie，默认为False
CORS_ORIGIN_ALLOW_ALL = True  # 所有ip都可以访问后端接口
# CORS_ORIGIN_WHITELIST = ["http://localhost:8080/"]  # 指定能够访问后端接口的ip或域名列表

# 允许访问的请求方法
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

# 允许的headers
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token'
)



ROOT_URLCONF = 'room_402.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'room_402.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

#  用户自己上传文件
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
