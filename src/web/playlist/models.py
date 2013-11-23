from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default


MAX_VOTES = 30


class Track(models.Model):
    name = models.CharField(max_length=128)
    link = models.URLField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name) + ' -> ' + unicode(self.link)


class Vote(models.Model):
    # 1 - x
    user = models.ForeignKey(User)
    track = models.ForeignKey(Track)

    def __unicode__(self):
        return unicode(self.user) + ' -> ' + unicode(self.track)


class DinnerMenu(models.Model):
    name = models.CharField(max_length=512)

    def __unicode__(self):
        return unicode(self.name)


class MenuChose(models.Model):
    # 1 - 1
    user = models.ForeignKey(User)
    menu_posiotion = models.ForeignKey(DinnerMenu)

    def __unicode__(self):
        return unicode(self.user) + ": " + unicode(self.menu_posiotion)


class Proposition(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField()
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (unicode(self.user) + ": " + unicode(self.comment)
                + " +:" + unicode(self.thumbs_up)
                + " -:" + unicode(self.thumbs_down))


class UserProp(models.Model):
    user = models.ForeignKey(User)
    proposition = models.ForeignKey(Proposition)
    up = models.BooleanField()

    def __unicode__(self):
        return (unicode(self.user) + " " + unicode(self.up) + ": "
                + unicode(self.proposition))


class PropComment(models.Model):
    user = models.ForeignKey(User)
    proposition = models.ForeignKey(Proposition)
    comment = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (unicode(self.user) + " ::(ON):: " + unicode(self.proposition)
                + "::(COMMENT)::" + unicode(self.comment))
