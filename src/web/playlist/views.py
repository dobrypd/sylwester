from django.views.generic import TemplateView
from playlist.models import (Track, Vote, MAX_VOTES, Proposition, UserProp,
                             MenuChose, DinnerMenu, PropComment)
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
import urllib2
from django.db.models.aggregates import Count
import datetime

EVE_YEAR = 2013


class HomeView(TemplateView):
    template_name = "default.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = "home"
        return context


class PlaylistView(TemplateView):
    template_name = "playlist.html"

    def get_context_data(self, **kwargs):
        context = super(PlaylistView, self).get_context_data(**kwargs)
        context['title'] = "playlist"
        context['max_votes'] = MAX_VOTES
        context['new_year'] = (datetime.datetime.today()).year > EVE_YEAR
        return context


class ProposeView(TemplateView):
    template_name = "propose.html"

    def get_context_data(self, **kwargs):
        context = super(ProposeView, self).get_context_data(**kwargs)
        context['title'] = "propose"
        return context


class FlavourView(TemplateView):
    template_name = "flavour.html"

    def get_menu(self, user):
        my_flavour = -120378
        try:
            m = MenuChose.objects.get(user=user)
            my_flavour = m.menu_posiotion.id
        except:
            pass
        m = DinnerMenu.objects.all()
        tabular = []
        for chose in m:
            tabular.append({
                'id': chose.id,
                'name': chose.name,
                'is_my': chose.id == my_flavour,
            })
        return tabular

    def get_context_data(self, request, **kwargs):
        context = super(FlavourView, self).get_context_data(**kwargs)
        context['title'] = "flavour"
        context['dinners'] = self.get_menu(request.user)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class ContactView(TemplateView):
    template_name = "contact.html"


# AJAX AND SIMMILAR


def find_track(track_name, track_link):
    tracks_by_link = Track.objects.filter(link=track_link)
    if len(tracks_by_link) == 1:
        return tracks_by_link[0]

    tracks = Track.objects.filter(name__icontains=track_name)
    if len(tracks) == 1:
        return tracks[0]

    return None


def crowl_known_services(track_link):
    if track_link.find("youtube") != -1:
        try:
            response = urllib2.urlopen(track_link)
            html = response.read()
            start = html.find("<title>") + len("<title>")
            end = html.find(" - YouTube</title>")
            return html[start:end]
        except:
            pass
    if track_link.find("wrzuta") != -1:
        try:
            response = urllib2.urlopen(track_link)
            html = response.read()
            start = html.find("<title>WRZUTA - ") + len("<title>WRZUTA - ")
            end = html.find("</title>")
            return html[start:end]
        except:
            pass
    return None


@login_required
def add_new_track(request):
    xhr = 'xhr' in request.GET

    if xhr and request.method == "POST":
        track_link = request.POST['track_link']
        s_name = crowl_known_services(track_link)
        if s_name is not None:
            track_name = s_name
        else:
            track_name = "NoName"

        result = ("?", None)
        try:
            new_track = find_track(track_name, track_link)
            if new_track is None:
                new_track = Track(name=track_name, link=track_link)
                new_track.save()
            result = ("OK", new_track.id)
        except ValueError:
            result = ("BadId", track_name)

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def add_track(request, track_id):
    xhr = 'xhr' in request.GET

    if xhr:
        result = "?"
        user = request.user
        try:
            this_user_votes = Vote.objects.filter(user=user)
            if (len(this_user_votes) >= MAX_VOTES):
                result = "ToMuch"
            else:
                track = Track.objects.get(id=track_id)
                new_vote = Vote(user=user, track=track)
                new_vote.save()
                result = "OK"
        except Track.DoesNotExist:
            result = "DoesNotExist"
        except Exception:
            result = "OtherError"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def remove_track(request, track_id):
    xhr = 'xhr' in request.GET

    if xhr:
        result = "?"
        user = request.user
        try:
            track = Track.objects.get(id=track_id)
            votes = Vote.objects.filter(track=track, user=user)
            for vote in votes:
                vote.delete()
            result = "OK"
        except Track.DoesNotExist:
            result = "TrackDoesNotExist"
        except Vote.DoesNotExist:
            result = "VoteDoesNotExist"
        except Exception:
            result = "OtherError"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def get_my_list(request):
    xhr = 'xhr' in request.GET

    if xhr:
        tracks = []
        try:
            qs = Vote.objects.filter(user=request.user)
            for row in qs:
                tracks.append({
                    'id': row.track.id,
                    'name': row.track.name,
                    'link': row.track.link})
        except:
            pass

        return HttpResponse(simplejson.dumps(tracks),
                            mimetype='application/json')

    return Http404


def get_list(request, how_many):
    xhr = 'xhr' in request.GET
    iam_hakier = 'hakier' in request.GET

    if xhr:
        tracks = []
        try:
            if ((datetime.datetime.today()).year > EVE_YEAR) or iam_hakier:
                qs = Vote.objects.values('track').annotate(
                        votes=Count('track')).order_by('-votes')
                last_votes = qs[0]['votes']
                last_position = 1
                for row in qs:
                    if row['votes'] < last_votes:
                        last_position += 1
                        last_votes = row['votes']
                    track = Track.objects.get(id=row['track'])
                    tracks.append({
                        'id': track.id,
                        'name': track.name,
                        'link': track.link,
                        'votes': row['votes'],
                        'position': last_position})
            else:
                qs = Track.objects.all().order_by("?")
                for row in qs[:how_many]:
                    tracks.append({
                        'id': row.id,
                        'name': row.name,
                        'link': row.link})
        except:
            pass

        return HttpResponse(simplejson.dumps(tracks),
                            mimetype='application/json')

    return Http404


@login_required
def get_top_list(request):
    xhr = 'xhr' in request.GET

    if xhr:
        tracks = []
        try:
            qs = Vote.objects.values('track').annotate(
                    votes=Count('track')).order_by('-votes')
            for row in qs:
                track = Track.objects.get(id=row['track'])
                tracks.append({
                    'id': track.id,
                    'name': track.name,
                    'link': track.link,
                    'votes': row['votes']})
        except:
            pass

        return HttpResponse(simplejson.dumps(tracks),
                            mimetype='application/json')

    return Http404


def get_comments(prop):
    comments = []
    try:
        qs = PropComment.objects.filter(proposition=prop).order_by("-add_time")
        for row in qs:
            comments.append({
                'id': row.id,
                'user': unicode(row.user),
                'comment': row.comment})
    except:
        pass
    return comments


@login_required
def get_propose_list(request):
    xhr = 'xhr' in request.GET

    if xhr:
        prop = []
        try:
            qs = Proposition.objects.extra(
                select={'thumbs': 'thumbs_up - thumbs_down'},
                order_by=('-add_time', '-thumbs'))
            for row in qs:
                prop.append({
                    'id': row.id,
                    'user': unicode(row.user),
                    'text': row.comment,
                    'comments': get_comments(row),
                    'thumbs_up': row.thumbs_up,
                    'thumbs_down': row.thumbs_down,
                    })
        except Exception as e:
            print e
            pass

        return HttpResponse(simplejson.dumps(prop),
                            mimetype='application/json')

    return Http404


@login_required
def thumb_up(request, prop_id):
    xhr = 'xhr' in request.GET

    if xhr:
        result = "?"
        user = request.user
        try:
            get_prop = Proposition.objects.get(id=prop_id)
            user_prop = UserProp.objects.filter(user=user,
                                             proposition=get_prop)
            if (len(user_prop) > 0) and (user.username != "piotrek"):
                result = "AlreadyVoted"
            else:
                user_prop = UserProp(user=user, proposition=get_prop, up=True)
                user_prop.save()
                get_prop.thumbs_up += 1
                get_prop.save()
                result = "OK"

        except Proposition.DoesNotExist:
            result = "PropositionNotExist"
        except Exception as e:
            print e
            result = "OtherError"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def thumb_down(request, prop_id):
    xhr = 'xhr' in request.GET

    if xhr:
        result = "?"
        user = request.user
        try:
            get_prop = Proposition.objects.get(id=prop_id)
            user_prop = UserProp.objects.filter(user=user,
                                             proposition=get_prop)
            if (len(user_prop) > 0) and (user.username != "piotrek"):
                result = "AlreadyVoted"
            else:
                user_prop = UserProp(user=user, proposition=get_prop, up=False)
                user_prop.save()
                get_prop.thumbs_down += 1
                get_prop.save()
                result = "OK"

        except Proposition.DoesNotExist:
            result = "PropositionNotExist"
        except Exception as e:
            print e
            result = "OtherError"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def add_new_proposition(request):
    xhr = 'xhr' in request.GET

    if xhr and request.method == "POST":
        text = request.POST['text']

        try:
            new_prop = Proposition(user=request.user, comment=text)
            new_prop.save()

            result = "OK"
        except:
            result = "BAD"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def add_new_comment(request):
    xhr = 'xhr' in request.GET

    if xhr and request.method == "POST":
        text = request.POST['text']
        proposition_id = request.POST['proposition_id']

        try:
            prop = Proposition.objects.get(id=proposition_id)

            new_comment = PropComment(proposition=prop, user=request.user,
                                      comment=text)
            new_comment.save()

            result = "OK"
        except:
            result = "BAD"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


@login_required
def set_menu(request, menu_pos):
    xhr = 'xhr' in request.GET

    if xhr:
        result = "?"
        user = request.user
        try:
            menu_position = DinnerMenu.objects.get(id=menu_pos)

            my_menu = MenuChose.objects.filter(user=user)
            if len(my_menu) > 0:
                my_menu = my_menu[0]
                my_menu.menu_posiotion = menu_position
            else:
                my_menu = MenuChose(user=user, menu_posiotion=menu_position)
            my_menu.save()
            result = "OK"
        except DinnerMenu.DoesNotExist:
            result = "MenuDoesNotExist"
        except Exception as e:
            print e
            result = "OtherError"

        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')

    return Http404


###  USERS

def new_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                HttpResponseRedirect('/accounts/newaccount/')
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {
        'form': form,
    })

