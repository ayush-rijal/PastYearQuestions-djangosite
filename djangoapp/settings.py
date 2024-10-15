import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')


ALLOWED_HOSTS = ["127.0.0.1", "localhost", "pastyearquestions.blog", "18.118.19.96"]
# ALLOWED_HOSTS = ["pastyearquestions.blog", "18.118.19.96"]

CSRF_TRUSTED_ORIGINS=["https://pastyearquestions.blog"]

# Application definition

INSTALLED_APPS = [
    'unfold',  # before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'base',
    'quiz',
    'account',
    'ckeditor',
    'ckeditor_uploader',
    'tailwind',
    'theme',
    'websites',
    'rest_framework',
     
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.TrafficMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

ROOT_URLCONF = 'djangoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'theme/templates'],
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

WSGI_APPLICATION = 'djangoapp.wsgi.application'
LOGIN_URL='login'

TAILWIND_APP_NAME = 'theme' # This is the name of the app that will be used to generate the tailwind files
INTERNAL_IPS = ['127.0.0.1']
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PGDATABASE"],
        'USER':os.environ["PGUSER"],
        'PASSWORD': os.environ["PGPASSWORD"] ,
        # 'HOST':'pyqdatabase.c1o2akk6an16.us-east-2.rds.amazonaws.com',
        'HOST':os.environ["PGHOST"],
        # 'PORT':'5432',
        'PORT':os.environ["PGPORT"],
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Directory where Django will collect static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# In development, Django will look for static files in these directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Specify the relative path for CKEditor uploads
CKEDITOR_UPLOAD_PATH = 'uploads/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# unfold admin config

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": 'Past Questions',
    "SITE_HEADER": 'pasr Questions',
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("images/icon-light.svg"),  # light mode
        "dark": lambda request: static("images/icon-dark.svg"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": lambda request: static("images/logo-white.png"),  # light mode
        "dark": lambda request: static("images/logo-black.png"),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/logo-white.png"),
        },
    ],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    
    
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("past Year Quesstions"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Home"),
                        "icon": "home",  
                        "link": reverse_lazy("admin:index"),
                        "badge": "Meain Admin",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Category"),
                        "icon": "category",  
                        "link": reverse_lazy("admin:quiz_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Quiz"),
                        "icon": "quiz",  
                        "link": reverse_lazy("admin:quiz_quiz_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Question"),
                        "icon": "question_mark",  
                        "link": reverse_lazy("admin:quiz_question_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Choice"),
                        "icon": "editor_choice",  
                        "link": reverse_lazy("admin:quiz_choice_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Quiz Submission"),
                        "icon": "upload",  
                        "link": reverse_lazy("admin:quiz_quizsubmission_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("User Rank"),
                        "icon": "group_add",  
                        "link": reverse_lazy("admin:quiz_userrank_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Message"),
                        "icon": "mail",  
                        "link": reverse_lazy("admin:base_message_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Blog"),
                        "icon": "rss_feed",  
                        "link": reverse_lazy("admin:base_blog_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Profile"),
                        "icon": "person",  
                        "link": reverse_lazy("admin:account_profile_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("TrafficData"),
                        "icon": "monitoring",  
                        "link": reverse_lazy("admin:account_trafficdata_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("slider"),
                        "icon": "monitoring",  
                        "link": reverse_lazy("admin:websites_slider_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
    
}


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "danger"] # info, danger, warning, success


def badge_callback(request):
    return 3

def permission_callback(request):
    return request.user.has_perm("sample_app.change_model")


# AWS_ACCESS_KEY_ID='AKIA5WLTTKTPG2E3RQXB'
# AWS_SECRET_ACCESS_KEY='ICm5D/z1+88o7JmhWsVeI6/cB1JXWkwIOJ13wVV2'
# AWS_STORAGE_BUCKET_NAME='pyqbucket'
# AWS_S3_SIGNATURE_NAME='s3v4'
# AWS_S3_REGION_NAME='us-east-2'
# AWS_S3_FILE_OVERWRITE=False
# AWS_DEFAULT_ACL=None
# AWS_S3_VERIFY=True
# DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'