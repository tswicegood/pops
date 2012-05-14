"""
This setup file was built by [Flunky][], a tool for simplifying Python
package setup and creation.

You probably shouldn't need to edit this file directly, but feel free to.

[Flunky]: https://github.com/tswicegood/flunky
"""

from distutils.core import setup
import json
import os

info = json.load(open("./package.json"))


def convert_to_str(d):
    """
    Recursively convert all values in a dictionary to strings

    This is required because setup() does not like unicode in
    the values it is supplied.

    .. todo:: there has to be a better way
    """
    d2 = {}
    for k, v in d.items():
        k = str(k)
        if type(v) in [list, tuple]:
            d2[k] = [str(a) for a in v]
        elif type(v) is dict:
            d2[k] = convert_to_str(v)
        else:
            d2[k] = str(v)
    return d2

info = convert_to_str(info)
NAMESPACE_PACKAGES = []


# TODO: simplify this process
def generate_namespaces(package):
    if package.find(".") is -1:
        return
    new_package = ".".join(package.split(".")[0:-1])
    if new_package.count(".") > 0:
        generate_namespaces(new_package)
    NAMESPACE_PACKAGES.append(new_package)
generate_namespaces(info["name"])


if os.path.exists("MANIFEST"):
    os.unlink("MANIFEST")


# Borrowed from Django's setup.py
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
project_dir = info["name"].split(".")[0]

for dirpath, dirnames, filenames in os.walk(project_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))

    # This is different than Django's implementation -- we want to include
    # non-Python files as data files

    # Strip off the length of the package name plus the trailing slash
    prefix = dirpath[len(info["name"]) + 1:]
    for f in filenames:
        # Ignore all dot files and any compiled
        if not (f == "." or f == ".." or
                f.endswith(".pyc") or
                f.endswith(".py")):
            data_files.append(os.path.join(prefix, f))

setup_kwargs = {
    "packages": packages,
    "package_data": {info["name"]: data_files, },
}
if NAMESPACE_PACKAGES:
    setup_kwargs["namespace_packages"] = NAMESPACE_PACKAGES

if not "version" in info:
    import imp
    mod_args = imp.find_module(info["name"])
    mod = imp.load_module(info["name"], *mod_args)
    setup_kwargs["version"] = getattr(mod, "__version__")

setup_kwargs.update(info)
setup(**setup_kwargs)
