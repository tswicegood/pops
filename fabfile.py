from fabric.api import local, task
from os.path import join, dirname


BASE_DIR = dirname(__file__)
VENDOR_PATH = join(BASE_DIR, "vendor")
STATIC_PATH = join(BASE_DIR, "pops", "static")
BOOTSTRAP_PATH = join(VENDOR_PATH, "bootstrap")

BOOTSTRAP = {
    "source": join(VENDOR_PATH, "bootstrap"),
    "compiled": join(VENDOR_PATH, "bootstrap", "docs", "assets"),
    "dest": join(STATIC_PATH, "bootstrap"),
}

CHOSEN = {
    "source": join(VENDOR_PATH, "chosen", "chosen"),
    "dest": join(STATIC_PATH, "chosen"),
}

JQUERY_UI = {
    "source": join(VENDOR_PATH, "jquery-ui-bootstrap"),
    "dest": join(STATIC_PATH, "jquery-ui-bootstrap"),
}


@task
def update_jquery_ui():
    local("cp -R %s/css/custom-theme/* %s/css" % (
            JQUERY_UI["source"], JQUERY_UI["dest"]))
    local("cp %s/js/jquery-ui-*.js %s/js" % (
            JQUERY_UI["source"], JQUERY_UI["dest"]))


@task
def update_bootstrap():
    local("cd vendor/bootstrap && make")
    local("cp %s/js/bootstrap.min.js %s/js/" % (
            BOOTSTRAP["compiled"], BOOTSTRAP["dest"]))
    local("cp %s/img/*.* %s/img" % (BOOTSTRAP["source"], BOOTSTRAP["dest"]))
    local("cp %s/css/bootstrap*.css %s/css" % (
            BOOTSTRAP["compiled"], BOOTSTRAP["dest"]))
    local("cp %s/less/*.* %s/less" % (BOOTSTRAP["source"], BOOTSTRAP["dest"]))
    local("cp %s/LICENSE %s" % (BOOTSTRAP["source"], BOOTSTRAP["dest"]))


@task
def update_chosen():
    local("cp %s/*.* %s" % (CHOSEN["source"], CHOSEN["dest"]))
