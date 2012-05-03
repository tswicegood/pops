from fabric.api import local, task
from os.path import join, dirname


BOOTSTRAP_PATH = join(dirname(__file__), "vendor", "bootstrap")
DESTINATION_PATH = join(dirname(__file__), "admintools_bootstrap", "static",
        "admintools_bootstrap", "bootstrap")


@task
def update_bootstrap():
    local("cp %s/js/*.js %s/js/" % (BOOTSTRAP_PATH, DESTINATION_PATH))
    local("cp %s/img/*.* %s/img" % (BOOTSTRAP_PATH, DESTINATION_PATH))
    local("cp %s/less/*.* %s/less" % (BOOTSTRAP_PATH, DESTINATION_PATH))
    # for path in ["img", "js", "less", "LICENSE"]:
    #     full_path = join(BOOTSTRAP_PATH, path)
    #     local("cp -R %s %s" % (full_path, DESTINATION_PATH))
