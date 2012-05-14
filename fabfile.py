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


@task
def update_jquery_ui():
    local("cp "
        "vendor/jquery-ui-bootstrap/css/custom-theme/jquery-ui-1.8.16.custom.css "
        "admintools_bootstrap/static/admin_tools/css/jquery-ui.css")


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
