from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from picasso.models import (Album, Photo, Thumbnail, Content, AlbumComment,
                            PhotoComment)
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
import time

if getattr(settings, 'ALBUMS', False):
    ok_albums = settings.ALBUMS
else:
    ok_albums = []

if getattr(settings, 'PICASSO_INDEX_ALBUMS', False):
    index_albums = settings.PICASSO_INDEX_ALBUMS
else:
    index_albums = 4

if getattr(settings, 'PICASSO_INDEX_PHOTOS', False):
    index_photos = settings.PICASSO_INDEX_PHOTOS
else:
    index_photos = 8


def list_albums(request):
    albums = Album.objects.all()

    good_albums = []
    for album in albums:
        if album.name in ok_albums:
            good_albums.append(album)

    if 'all' in request.GET:
        good_albums = albums

    return render_to_response('picasso/list_albums.html',
                              {'albums': good_albums,
                               'title': 'photos'},
                              context_instance=RequestContext(request))


def view_album(request, album):
    selected_album = get_object_or_404(Album, name=album)

    photos = selected_album.photo_set.order_by('published').all()

    return render_to_response('picasso/view_album.html',
                              {'album': selected_album,
                               'album_name': album,
                               'photos': photos,
                               'title': 'photos'},
                              context_instance=RequestContext(request))


def view_photo(request):
    return render_to_response('picasso/view_photo.html',
                              context_instance=RequestContext(request))


def get_photo(request, photoid):
    xhr = 'xhr' in request.GET

    if xhr:
        selected_photo = get_object_or_404(Photo, photoid=photoid)

        thumbnails = []
        for thumb in selected_photo.thumbnails.all():
            thumbnails.append({
                'width': thumb.width,
                'height': thumb.height,
                'url': thumb.url,
            })
        contents = []
        for photo in selected_photo.content.all():
            contents.append({
                'width': photo.width,
                'height': photo.height,
                'url': photo.url,
            })
        select_photos_from_this_album = Photo.objects.filter(album=selected_photo.album).order_by('-published')
        last_photo = selected_photo
        next_photo = selected_photo
        found = False
        for x_photo in select_photos_from_this_album:
            if found:
                next_photo = x_photo
                break
            if x_photo == selected_photo:
                found = True
            else:
                last_photo = x_photo

        photo = {
            'title': selected_photo.title,
            'published': time.mktime(selected_photo.published.timetuple()),
            'link': selected_photo.link,
            'thumbnails': thumbnails,
            'content': contents,
            'album': selected_photo.album.name,
            'photoid': selected_photo.photoid,
            'summary': selected_photo.summary,
            'next': next_photo.photoid,
            'previous': last_photo.photoid
        }
        return HttpResponse(simplejson.dumps(photo),
                            mimetype='application/json')
    return Http404


def get_photo_comments(request, photoid):
    xhr = 'xhr' in request.GET

    if xhr:
        selected_photo = get_object_or_404(Photo, photoid=photoid)

        comments = []
        try:
            qs = PhotoComment.objects.filter(photo=selected_photo).order_by(
                                                                   "add_time")
            for row in qs:
                comments.append({
                    'id': row.id,
                    'user': unicode(row.user),
                    'time': unicode(row.add_time),
                    'comment': row.comment})
        except:
            pass

        return HttpResponse(simplejson.dumps(comments),
                            mimetype='application/json')

    return Http404


@login_required
def add_new_photo_comment(request):
    xhr = 'xhr' in request.GET

    if xhr and request.method == "POST":
        text = request.POST['text']
        photoid = request.POST['photoid']

        try:
            selected_photo = get_object_or_404(Photo, photoid=photoid)

            new_comment = PhotoComment(photo=selected_photo, user=request.user,
                                      comment=text)
            new_comment.save()

            result = "OK"
        except:
            result = "BAD"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


def get_album_comments(request, album):
    xhr = 'xhr' in request.GET

    if xhr:
        selected_album = get_object_or_404(Album, name=album)

        comments = []
        try:
            qs = AlbumComment.objects.filter(album=selected_album).order_by(
                                                                   "-add_time")
            for row in qs:
                comments.append({
                    'id': row.id,
                    'user': unicode(row.user),
                    'time': unicode(row.add_time),
                    'comment': row.comment})
        except Exception as e:
            print e
            pass

        return HttpResponse(simplejson.dumps(comments),
                            mimetype='application/json')

    return Http404


@login_required
def add_new_album_comment(request):
    xhr = 'xhr' in request.GET

    if xhr and request.method == "POST":
        text = request.POST['text']
        album_name = request.POST['album_name']

        try:
            selected_album = get_object_or_404(Album, name=album_name)

            new_comment = AlbumComment(album=selected_album, user=request.user,
                                      comment=text)
            new_comment.save()

            result = "OK"
        except:
            result = "BAD"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404
