import sys
import site
import os

vepath = '/home/piotrek/sylwester2012/page_env/lib/python2.7/site-packages'

prev_sys_path = list(sys.path)

# add the site-packages of our virtualenv as a site dir

site.addsitedir(vepath)

# add the app's directory to the PYTHONPATH

sys.path.append('/home/piotrek/sylwester2012/src/sylwester2012')

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)

sys.path[:0] = new_sys_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sylwester2012.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
