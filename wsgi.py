# from django.core.wsgi import get_wsgi_application
# from dj_static import Cling

# application = Cling(get_wsgi_application())

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quote_ninja.settings")
application = get_wsgi_application()
application = DjangoWhiteNoise(application)