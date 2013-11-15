#!/usr/bin/env python

# Author: Piotr Dobrowolski
# dobrypd@gmail.com

from sys import argv, exit
import os
import string
import re
from subprocess import Popen

ID3V2_CMD="/usr/bin/id3v2"

###############################################################################
class SInfo:
    def __init__(self, artist=None, title="notitle", album=None):
        self.artist = artist
        self.title = title
        self.album = album
    def get_artist(self):
        return self.artist
    def get_title(self):
        return self.title
    def get_album(self):
        return self.album
    def set_artist(self, value):
        self.artist = string.capitalize(value)
    def set_title(self, value):
        self.title = string.capitalize(value)
    def set_album(self, value):
        self.album = string.capitalize(value)
    def is_artist_set(self):
        return self.artist is not None
    def is_album_set(self):
        return self.album is not None
    def __str__(self):
        preety_str = ""
        if (self.is_artist_set()):
            preety_str += self.artist + " - "
        preety_str = self.title
        if (self.is_album_set()):
            preety_str += ", from " + self.album
        return preety_str
###############################################################################

###############################################################################
class Fixer:
    def fix(self, yt_title):
        return yt_title
class YTTitleSplitter:
    known_dirty_chars = set([
            '\'', '"', '`', '\t', '@', '#', '$', '%', '^', '&', ':', '*', 
            ',', '.', '/', '\\', ';', '+', '=', '~'
            ])
    white_space = set([
            ' ', '\t', '\n'
            ])
    dash = '-'
    def __init__(self, yt_title, verbose = False):
        self.yt_title = yt_title
        self.verbose = verbose
    def get_song_info(self):
        if self.verbose is True:
            print "Getting info from name `%s`." % self.yt_title
        for fixer in self.get_title_fixers():
            self.yt_title = fixer.fix(self.yt_title)
        if self.verbose is True:
            print "After fixing `%s`." % self.yt_title
        return self.parse()
    def get_title_fixers(self):
        raise "Abstract"
    def dashes(self):
        has_it = False
        has_one = filter(lambda x: x==YTTitleSplitter.dash, self.yt_title)
        if self.verbose is True:
            print "Found %d dashes." % len(has_one)
        return len(has_one)
    def remove_dirty_chars(self):
        new_title = ""
        for c in self.yt_title:
            if c not in YTTitleSplitter.known_dirty_chars:
                new_title += c
        self.yt_title = new_title
        if self.verbose is True:
            print "Removed unliked characters `%s`" % self.yt_title
    def fix_cases_and_white(self):
        new_title = ""
        after_dash = False
        for c in self.yt_title:
            after_dash = after_dash or c == YTTitleSplitter.dash
            if ((c != YTTitleSplitter.dash) and after_dash
                    and (c not in YTTitleSplitter.white_space)):
                after_dash = False
                c = (str(c)).upper()
            new_title += c
                
        self.yt_title = string.capwords(new_title, YTTitleSplitter.dash)
        if self.verbose is True:
            print "Capitalized `%s`" % self.yt_title

    def parse(self):
        sinfo = SInfo()
        dashes_no = self.dashes()
        if dashes_no == 0:
            #Try by Artist "Title"
            #Try by Artist Title
            pieces = self.yt_title.split('"')
            if (len(pieces) > 1):
                sinfo.set_artist(pieces[0])
                sinfo.set_title(" ".join(pieces[1:]))
            sinfo.set_title(self.yt_title)
        else:
            self.remove_dirty_chars()
            self.fix_cases_and_white()
            if self.verbose is True:
                print "Parsing..."
            #TODO:Try by Title-Artist (only when have list of artists)
            pieces = self.yt_title.split(YTTitleSplitter.dash)
            pieces = map(lambda x: x.strip(), pieces)
            if (dashes_no == 2):
                #Try by Artist-Album-Title
                sinfo.set_artist(pieces[0])
                sinfo.set_album(pieces[1])
                sinfo.set_title(" ".join(pieces[2:]))
            else:
                #Try by Artist-Title
                sinfo.set_artist(pieces[0])
                sinfo.set_title(" ".join(pieces[1:]))
        return sinfo

class HeuristicSplitter(YTTitleSplitter):
    class FixBrackets(Fixer):
        known_brackets_begins = set(['(', '[', '{', '<'])
        known_backets_ends = {')':'(', ']':'[', '}':'{', '>':'<'}

        def fix(self, yt_title):
            new = ""
            remove = False
            opened = {'(':0, '[':0, '{':0, '<':0}
            for c in yt_title:
                if c in self.known_brackets_begins:
                    opened[c] += 1
                    remove = True
                elif c in self.known_backets_ends.keys():
                    opened[c] = max(opened[self.known_backets_ends[c]] - 1, 0)
                    opened_sum = sum(opened.values())
                    if opened_sum <= 0:
                        remove = False
                if not remove:
                    new += c
            return new
    class FixKnownNames(Fixer):
        names_to_remove = ["live", "lyric", "lyrics", "HD", "HQ",
        "720", "720p", "official", "full album", "album", ""]
        def fix(self, yt_title):
            new = yt_title
            for name in self.names_to_remove:
                insensitive_name_rx = (
                        re.compile(re.escape(name), re.IGNORECASE))
                new = insensitive_name_rx.sub('', new)
            return new

    def get_title_fixers(self):
        yield HeuristicSplitter.FixBrackets()
        yield HeuristicSplitter.FixKnownNames()
###############################################################################

###############################################################################
def test_file(file_name):
    if not os.path.isfile(file_name):
        print "No such file: `%s`." % file_name
        exit(1)

def split_names(file_name):
    root_with_file_base, extension = os.path.splitext(file_name)
    root, file_base_name = os.path.split(root_with_file_base)
    return (root, file_base_name, extension)

def rename(root, base_name, ext, sinfo):
    new_file_name = os.path.join(root,
                sinfo.get_artist() + " - " + sinfo.get_title() + ext)
    os.rename(os.path.join(root, base_name + ext), new_file_name)
    return new_file_name

def generate_id3v2_args(file_name, sinfo):
    args = [ID3V2_CMD]
    if sinfo.is_artist_set():
        args.append("-a")
        args.append(sinfo.get_artist())
    args.append("-t")
    args.append(sinfo.get_title())
    if sinfo.is_album_set():
        args.append("-A")
        args.append(sinfo.get_album())
    args.append(os.path.abspath(file_name))
    return args

def main(file_name, id3v2):
    test_file(file_name)
    root, base_name, extension = split_names(file_name)
    splitter = HeuristicSplitter(base_name, id3v2 == False)
    sinfo = splitter.get_song_info()
    new_file_name = rename(root, base_name, extension, sinfo)
    if (id3v2):
        p = Popen(generate_id3v2_args(new_file_name, sinfo))
        stdout, stderr = p.communicate()
    else:
        print "Info:"
        print "\t%s" % sinfo
        print "has been renamed to"
        print "\t%s" % new_file_name
###############################################################################


if __name__ == "__main__":
    if ((not ((len(argv) == 2) or (len(argv) == 3)))
            or (len(argv) == 3 and argv[1] != "--id3v2")):
        print("usage %s [--id3v2] input_file" % argv[0])
        print("\t--id3v2 will execute the id3v2 on this file")
        exit(0)
    if (len(argv) == 2):
        file_name = argv[1]
    else:
        file_name = argv[2]
    main(file_name, (len(argv) == 3))

