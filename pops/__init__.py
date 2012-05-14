major = "0"
minor = "1"
third = "0alpha"
extra = "0"

# You should not need to edit anything beyond this point.
__version_parts__ = (major, minor, third)

if not third.isdigit() or extra is not 0:
    __version_parts__ += (extra, )
__version__ = ".".join(__version_parts__)

version = "%s version %s" % (__name__, __version__)
