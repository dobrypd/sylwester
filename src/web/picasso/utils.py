from picasso.models import Album, Photo, Thumbnail, Content
from gdata.photos.service import PhotosService
from datetime import datetime

def picasa_sync(user, thumbsizes, imgmax):    
    print 'Adding new albums:'
    
    gd_client = PhotosService()
    
    feed_url = '/data/feed/api/user/%s' % user
    feed_url += '?kind=album&thumbsize=%s' % ','.join(thumbsizes) 
    
    feed = gd_client.GetFeed(feed_url)
    
    for entry in feed.entry:
        try:
            a = Album.objects.get(albumid=entry.gphoto_id.text)
            print 'Album %s already exists' % (a.title)
        except:
            published = datetime.strptime(entry.published.text[:-5],
                                          '%Y-%m-%dT%H:%M:%S')
            
            a = Album.objects.create(title=entry.title.text,
                                     name=entry.name.text,
                                     published=published,
                                     link=entry.link[1].href,
                                     albumid=entry.gphoto_id.text,
                                     summary=entry.summary.text)
            
            for thumb in entry.media.thumbnail:
                try:
                    t = Thumbnail.objects.get(url=thumb.url)
                except:
                    t = Thumbnail.objects.create(url=thumb.url,
                                                 height=thumb.height,
                                                 width=thumb.width)
                a.thumbnails.add(t)
            
            a.save()
            
            print 'Saved -', a.title
    
    print 'Adding new photos:'
    
    for album in Album.objects.all():
        feed_url = '/data/feed/api/user/%s/album/%s' % (user, str(album.name)) 
        feed_url += '?kind=photo&thumbsize=%s' % ','.join(thumbsizes)
        feed_url += '&imgmax=%s' % imgmax
        
        feed = gd_client.GetFeed(feed_url)
        
        for entry in feed.entry:
            try:
                p = Photo.objects.get(photoid=entry.gphoto_id.text)
                print 'Photo %s already exists' % (p.title)
            except:
                published = datetime.strptime(entry.published.text[:-5],
                                              '%Y-%m-%dT%H:%M:%S')
                
                a = Album.objects.get(albumid=entry.albumid.text)
                
                p = Photo.objects.create(title=entry.title.text,
                                         published=published,
                                         link=entry.link[1].href,
                                         photoid=entry.gphoto_id.text,
                                         summary=entry.summary.text,
                                         album=a)
                
                for thumb in entry.media.thumbnail:
                    try:
                        t = Thumbnail.objects.get(url=thumb.url)
                    except:
                        t = Thumbnail.objects.create(url=thumb.url,
                                                     height=thumb.height,
                                                     width=thumb.width)
                    p.thumbnails.add(t)
                
                content = entry.media.content[0]                
                try:
                    c = Content.objects.get(url=content.url)
                except:
                    c = Content.objects.create(url=content.url,
                                              height=content.height,
                                              width=content.width)
                
                p.content.add(c)
                
                p.save()
                
                print 'Saved -', p.title