#!/usr/bin/env python


from sylwester import settings
from django.core.management  import setup_environ

setup_environ(settings)


from playlist.models import Track
from playlist.models import Vote


def DamerauLevenshteinDistance(source, target):
    # Not so elegant way to implement this algorithm, but it's working!
    if len(source) < 1:
        if len(target) < 1:
            return 0
        else:
            return len(target)

    elif len(target) < 1:
        return len(source)

    score = list(list(range(len(target) + 2)) for _ in list(range(len(source)
                                                                  + 2)))

    INF = len(source) + len(target)
    score[0][0] = INF
    for i in range(len(source) + 1):
        score[i + 1][1] = i
        score[i + 1][0] = INF
    for j in range(len(target) + 1):
        score[1][j + 1] = j
        score[0][j + 1] = INF

    sd = {}
    for x in source:
        sd[x] = 0
    for x in target:
        sd[x] = 0

    for i in range(1, len(source) + 1):
        DB = 0
        for j in range(1, len(target) + 1):
            i1 = sd[target[j - 1]]
            j1 = DB

            if (source[i - 1] == target[j - 1]):
                score[i + 1][j + 1] = score[i][j]
                DB = j
            else:
                score[i + 1][j + 1] = min(score[i][j],
                                          min(score[i + 1][j],
                                              score[i][j + 1])) + 1

            score[i + 1][j + 1] = min(score[i + 1][j + 1],
                                      (score[i1][j1] + (i - i1 - 1) + 1
                                       + (j - j1 - 1)))
        sd[source[i - 1]] = i
    return score[len(source) + 1][len(target) + 1]


def check_is_this_same(track1, track2):
    # Is maybe this same!
    if track1.link == track2.link:
        # Check if empty or invalid
        return True

    if track1.name == track2.name:
        return True

    strings1 = track1.name.split()
    strings2 = track2.name.split()
    found_w = 0
    for word_in_1 in strings1:
        for word_in_2 in strings2:
            if ((len(word_in_1) > 3)
            and (len(word_in_2) > 3)
            and DamerauLevenshteinDistance(word_in_1.lower(),
                                           word_in_2.lower()) < 2):
                found_w += 1
                if (found_w > 1):
                    return True

    if DamerauLevenshteinDistance(track1.name, track2.name) < 10:
        return True

    return False


def fix_votes(track_good, track_to_erase):
    qs = Vote.objects.filter(track=track_to_erase)
    for vote in qs:
        vote.track = track_good
        vote.save()


def main():
    maybe_this_same = set()
    qs = Track.objects.all()
    for t1 in qs:
        for t2 in qs:
            if (t1 != t2) and check_is_this_same(t1, t2):
                if (t1.add_time > t2.add_time):
                    maybe_this_same.add((t1, t2))
                else:
                    maybe_this_same.add((t2, t1))

    to_delete = set()
    for (t1, t2) in maybe_this_same:
        print t1
        print t2
        to_join = raw_input('Join it [Y/(N | Enter)], or save only [1/2]:')
        if to_join.lower() == 'y':
            to_delete.add((t1, t2))
        if to_join == '1':
            to_delete.add((t1, t2))
        if to_join == '2':
            to_delete.add((t2, t1))

    for (t1, t2) in to_delete:
        fix_votes(t1, t2)
    for (t1, t2) in to_delete:
        t2.delete()

    print "DONE"


if __name__ == "__main__":
    main()

