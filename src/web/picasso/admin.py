from django.contrib import admin
from picasso.models import (Album, Photo, Thumbnail, Content, AlbumComment,
                            PhotoComment)


class AlbumAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass


class ThumbnailAdmin(admin.ModelAdmin):
    pass


class ContentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(AlbumComment)
admin.site.register(PhotoComment)
