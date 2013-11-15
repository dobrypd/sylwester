from django.core.management.base import NoArgsCommand
from picasso.utils import picasa_sync
import sys

class Command(NoArgsCommand):
    help = 'Contacts Picasa and synchronizes Albums and Photos to the local '
    help += 'database'

    def handle_noargs(self, **options):
        from django.conf import settings
        
        if getattr(settings, 'PICASSO_USER', False):
            user = settings.PICASSO_USER
        else:
            sys.exit('Please set PICASSO_USER in your settings.py file')
        
        if getattr(settings, 'PICASSO_THUMBSIZES', False):
            thumbsizes = settings.PICASSO_THUMBSIZES
        else:
            sys.exit('Please set PICASSO_THUMBSIZES in your settings.py file')
        
        if getattr(settings, 'PICASSO_IMGMAX', False):
            imgmax = settings.PICASSO_IMGMAX
        else:
            sys.exit('Please set PICASSO_IMGMAX in your settings.py file')
        
        picasa_sync(user=user, thumbsizes=thumbsizes, imgmax=imgmax)