#!/usr/bin/env python


from sylwester import settings
from django.core.management  import setup_environ

setup_environ(settings)


from playlist.models import Track

import subprocess
import sys
import os

YT_D = "youtube-dl"
FFMPEG = "ffmpeg"

REMOVE_ORIGINALS = True
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
        cmd = [YT_D, track.link]
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


def change_to_mp3(directory, downloaded):
    cannot_change = []
    changed = []
    curr_pr = 0
    pids = []
    for track, file_name in downloaded:
        curr_pr += 1
        output_file_name = "".join(track.name.split()) + ".mp3"
        cmd = [FFMPEG, "-i", file_name, output_file_name]
        pids.append((subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               cwd=directory),
                     track, file_name))
        if (curr_pr >= PROCESSESS_CONCURRENT):            
            for pid, track, file_name in pids:
                pid.wait()
                errors = pid.stderr.readlines()
                bad = False
                for line in errors:
                    if line.find("Unable") != -1:
                        bad = True
                    if line.find("Invalid") != -1:
                        bad = True
                if bad:
                    cannot_change.append((track, file_name, output_file_name))
                else:
                    if REMOVE_ORIGINALS:
                        try:
                            os.remove(directory + "/" + file_name)
                        except:
                            pass
                    changed.append((track, file_name, output_file_name))
            curr_pr = 0
            pids = []

    for pid, track, file_name in pids:
        pid.wait()
        errors = pid.stderr.readlines()
        bad = False
        for line in errors:
            if line.find("Unable") != -1:
                bad = True
            if line.find("Invalid") != -1:
                bad = True
        if bad:
            cannot_change.append((track, file_name, output_file_name))
        else:
            if REMOVE_ORIGINALS:
                os.remove(directory + "/" + file_name)
            changed.append((track, file_name, output_file_name))
    
    print "-- CANNOT CHANGE TO MP3 --"
    for track, file_name, output_file_name in cannot_change:
        print track, file_name, output_file_name 
    print "---------------------"
    
    return changed


def main():
    if (len(sys.argv) != 2):
        print "Usage: " + sys.argv[0] + " output_directory"
        return
    output_directory = sys.argv[1]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if not os.path.isdir(output_directory):
        print output_directory + ": It's not directory!"
    
    change_to_mp3(output_directory, download(output_directory))

if __name__ == "__main__":
    main()
