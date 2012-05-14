from appconf import AppConf

# Make this accessible to the rest of the application
from django.conf import settings


class PopsConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'POPS'
