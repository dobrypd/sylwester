#!/usr/bin/env python

from sylwester import settings
from django.core.management  import setup_environ

setup_environ(settings)


from playlist.models import Track

import subprocess
import sys
import os


GRABBER = "grabber" # grabber is youtube-dl wrapper

REMOVE_ORIGINALS = False
PROCESSESS_CONCURRENT = 3  # x2 because of ffmpeg


def want_download(directory, track):
    # Check if already downloaded:
    file_name = "".join(track.name.split()) + ".mp3"
    if os.path.exists(directory + "/" + file_name):
        return False
    return True

def download(directory):
    cannot_download = []
    qs = Track.objects.all()
    pids = []
    curr_pr = 0
    all_tracks = len(qs)
    done = 0
    for track in qs:
        done += 1
        curr_pr += 1
        cmd = [GRABBER, track.link]
        if (want_download(directory, track)):
            pids.append((subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   cwd=directory), track))
        if (curr_pr >= PROCESSESS_CONCURRENT) or (done == all_tracks):
            for pid, track in pids:
                pid.wait()
                errors = pid.stderr.readlines()
                if len(errors) > 0:
                    cannot_download.append(track)
                else:
                    file_name  = ""
                    has_been_downloaded = False
                    for line in pid.stdout.readlines():
                        if line.find("Destination:") != -1:
                            index = line.find(":")
                            file_name = line[index + 2:-1]
                        if line.find("has already been downloaded") != -1:
                            has_been_downloaded = True
                    if not has_been_downloaded:
                        yield (track, file_name)
            curr_pr = 0
            pids = []
        print str(done) + " / " + str(all_tracks)
                
    
    print "-- CANNOT DOWNLOAD --"
    for track in cannot_download:
        print track
        print "".join(track.name.split()) + ".mp3"
    print "---------------------"


def main():
    if (len(sys.argv) != 2):
        print "Usage: " + sys.argv[0] + " output_directory"
        return
    output_directory = sys.argv[1]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if not os.path.isdir(output_directory):
        print output_directory + ": It's not a directory!"
    
    download(output_directory)

if __name__ == "__main__":
    main()
