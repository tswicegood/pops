from fabric.api import local, task
from os.path import join, dirname


BOOTSTRAP_PATH = join(dirname(__file__), "vendor", "bootstrap")
COMPILED_BOOTSTRAP_PATH = join(BOOTSTRAP_PATH, "docs", "assets")
DESTINATION_PATH = join(dirname(__file__), "admintools_bootstrap", "static",
        "bootstrap")


@task
def update_jquery_ui():
    local("cp "
        "vendor/jquery-ui-bootstrap/css/custom-theme/jquery-ui-1.8.16.custom.css "
        "admintools_bootstrap/static/admin_tools/css/jquery-ui.css")


@task
def update_bootstrap():
    local("cd vendor/bootstrap && make")
    local("cp %s/js/bootstrap.min.js %s/js/" % (
            COMPILED_BOOTSTRAP_PATH, DESTINATION_PATH))
    local("cp %s/img/*.* %s/img" % (BOOTSTRAP_PATH, DESTINATION_PATH))
    local("cp %s/css/bootstrap*.css %s/css" % (
            COMPILED_BOOTSTRAP_PATH, DESTINATION_PATH))
    local("cp %s/less/*.* %s/less" % (BOOTSTRAP_PATH, DESTINATION_PATH))
    # for path in ["img", "js", "less", "LICENSE"]:
    #     full_path = join(BOOTSTRAP_PATH, path)
    #     local("cp -R %s %s" % (full_path, DESTINATION_PATH))
