from django.contrib import admin
from playlist.models import MenuChose, DinnerMenu, Vote,\
    Proposition, Track, UserProp, PropComment

admin.site.register(Vote)
admin.site.register(Track)
admin.site.register(DinnerMenu)
admin.site.register(MenuChose)
admin.site.register(Proposition)
admin.site.register(UserProp)
admin.site.register(PropComment)
