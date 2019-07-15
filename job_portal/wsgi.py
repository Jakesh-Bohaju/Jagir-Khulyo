"""
WSGI config for job_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')

application = get_wsgi_application()



# # +++++++++++ DJANGO +++++++++++
# # To use your own django app use code like this:
# import os
# import sys

# # assuming your django settings file is at '/home/jakeshb/mysite/mysite/settings.py'
# # and your manage.py is is at '/home/jakeshb/mysite/manage.py'
# path = '/home/jakeshb/jagirkhulyo/jagirkhulyo'
# if path not in sys.path:
#     # sys.path.append(path)
#     sys.path.insert(0, path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'job_portal.settings'

# # then:
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

