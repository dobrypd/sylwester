from picasso.models import Photo
from django.conf import settings

def latest_photos(request):
    if getattr(settings, 'PICASSO_LATEST_PHOTOS', False):
        latest = settings.PICASSO_LATEST_PHOTOS
    else:
        latest = 10
    
    latest_photos = Photo.objects.all()[:latest]
    
    return {'latest_photos': latest_photos}