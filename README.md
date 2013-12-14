SYLWESTER
=========

Overview
--------

It's voting system based on `django`.

I wrote it before New Year's Eve party in 2012 for my friends.


Imagine an event for much more than 100 people, without DJ.
There are plenty of music collection created directly for such a occasions.
But there are without context, without connection to
the direct group of people.

We want to create Top Playlist by ourselfs. Best pieces of music, best for us.
Playlist has to be easy to download and with votes,
         we want to know the most popular song.

Moreover we need system to create simple communication schema.
I.e. to choose catering. But that part of this app didn't pass exam,
everyone just used facebook for this.

This app successfully created playlists for New Year's Eve 2012 party.
For 2013 is in progress.


Typical flow
------------

Deploy app on server. I suggest to turn off possibility of seeing
top playlist.
The element of astonishment is required. 

After you collected full list just download it (tool included).
Use title joiner to search for this same track with different links/names.


Language
--------

I have templates only in polish. Sorry.


WARNING
-------

Be aware of using this code in your project.
I wrote all this code in few evenings.
It certainly contains some bugs.


Requirements, used projects.
----------------------------

I used `django` in version 1.6.0, `python-social-auth` in version 0.1.17
and `gdata` 2.0.18. `youtube-dl` in version 2013.12.09.4.


License
-------

Full rights for use or change MY source code under new BSD license
(http://opensource.org/licenses/BSD-3-Clause).
    Remember that not all of this source was wrote by me
(see Requirements, used projects,
 if not it'll be written in the beginning of file).

All rights reserved for my photos in directory:
`/src/web/static/img/`
(my - all without that from bootstrap and bottle of champagne).

