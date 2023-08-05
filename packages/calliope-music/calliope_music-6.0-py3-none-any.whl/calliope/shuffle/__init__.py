# Calliope
# Copyright (C) 2017  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import click

import argparse
import copy
import itertools
import os
import random
import sys
import urllib.parse
import warnings

import calliope.playlist


def shuffle(playlist: calliope.playlist.Playlist, count: int=None) -> calliope.playlist.Playlist:
    """Simple playlist shuffle.

    This randomises the order of the items in the playlist.

    There is a lot more involved in creating "good" shuffled playlists. For
    example see https://labs.spotify.com/2014/02/28/how-to-shuffle-songs/

    Args:
        playlist: Input playlist.
        count: Maximum number of items in the output playlist (default: unlimited).

    Returns:
        A playlist.
    """
    corpus = copy.copy(list(playlist))
    random.shuffle(corpus)
    if count:
        corpus = corpus[0:count]

    return corpus
