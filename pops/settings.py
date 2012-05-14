from appconf import AppConf


class PopsConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'POPS'
