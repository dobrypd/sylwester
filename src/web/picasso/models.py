from django.db import models
from django.contrib.auth.models import User


class Thumbnail(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    url = models.URLField()

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)

    class Meta:
        ordering = ['width']


class Content(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    url = models.URLField()

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)

    class Meta:
        ordering = ['width']


class Album(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    published = models.DateTimeField()
    link = models.URLField()
    thumbnails = models.ManyToManyField(Thumbnail)
    albumid = models.CharField(max_length=25)
    summary = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published']

    @models.permalink
    def get_absolute_url(self):
        return ('picasso_view_album', (), {'album': self.name})


class Photo(models.Model):
    title = models.CharField(max_length=200)
    published = models.DateTimeField()
    link = models.URLField()
    thumbnails = models.ManyToManyField(Thumbnail)
    content = models.ManyToManyField(Content)
    album = models.ForeignKey(Album)
    photoid = models.CharField(max_length=25)
    summary = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published']

    @models.permalink
    def get_absolute_url(self):
        return ('picasso_view_photo', (), {'photoid': self.photoid})


class AlbumComment(models.Model):
    user = models.ForeignKey(User)
    album = models.ForeignKey(Album)
    comment = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (unicode(self.user) + " ::(ON):: " + unicode(self.album)
                + "::(COMMENT)::" + unicode(self.comment))


class PhotoComment(models.Model):
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    comment = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (unicode(self.user) + " ::(ON):: " + unicode(self.album)
                + "::(COMMENT)::" + unicode(self.comment))
