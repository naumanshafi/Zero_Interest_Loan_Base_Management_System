import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '2aq8p_hdb#hy8i_44g-p84k10#cl13an2sd5e+)sfpq#a(+-v+'
DEBUG = True
# if DEBUG:
#     STATIC_ROOT = os.path.join(BASE_DIR, '/static')
# else:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_HTTPONLY = True

# Application definition

INSTALLED_APPS = [
    'Committee.apps.CommitteeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Facebook
    'social_django',  # add this

    # Payment
    'django.contrib.sites',  # added for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'stripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DKameti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'DKameti.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/images/'

##Payment

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_root'),
]

VENV_PATH = os.path.dirname(BASE_DIR)

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(VENV_PATH, 'media_root')

# Stripe and Braintree Settings

if DEBUG:
    # test keys
    STRIPE_PUBLISHABLE_KEY = 'pk_test_4SQORZRCHI95ZcHzppI5VeD200NRAN7Vlx'
    STRIPE_SECRET_KEY = 'sk_test_BuWVlqbCCzax1wBbWsFfKim200N4V2C7Ar'
    BT_ENVIRONMENT = 'sandbox'
    BT_MERCHANT_ID = 'YOUR BT_MERCHANT_ID'
    BT_PUBLIC_KEY = 'YOUR BT_PUBLIC_KEY'
    BT_PRIVATE_KEY = 'YOUR BT_PRIVATE_KEY'
else:
    # live keys
    STRIPE_PUBLISHABLE_KEY = 'YOUR STRIPE LIVE PUB KEY'
    STRIPE_SECRET_KEY = 'YOUR STRIPE LIVE SECRET KEY'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

#
# #facebook
# AUTHENTICATION_BACKENDS = [
#     'social_core.backends.linkedin.LinkedinOAuth2',
#     'social_core.backends.instagram.InstagramOAuth2',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# ]
SITE_ID = 1

# Facebook
LOGIN_REDIRECT_URL = 'Committee-Facebook'

SOCIAL_AUTH_FACEBOOK_KEY = 812444502460375  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "6855a4e79b4f7b516caab7916121612b"  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']  # add this
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {  # add this
    'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [  # add this
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]
