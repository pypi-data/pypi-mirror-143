#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=W,C

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
#

"""
Script for exporting tracks through audioscrobbler API.
Usage: lastexport.py -u USER [-o OUTFILE] [-p STARTPAGE] [-s SERVER]
"""

import logging
import sys, time, re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from optparse import OptionParser

__version__ = '0.0.4'

log = logging.getLogger(__name__)

def get_options(parser):
    """ Define command line options."""
    parser.add_option("-u", "--user", dest="username", default=None,
                      help="User name.")
    parser.add_option("-o", "--outfile", dest="outfile", default="exported_tracks.txt",
                      help="Output file, default is exported_tracks.txt")
    parser.add_option("-p", "--page", dest="startpage", type="int", default="1",
                      help="Page to start fetching tracks from, default is 1")
    parser.add_option("-s", "--server", dest="server", default="last.fm",
                      help="Server to fetch track info from, default is last.fm")
    parser.add_option("-t", "--type", dest="infotype", default="scrobbles",
                      help="Type of information to export, scrobbles|loved|banned, default is scrobbles")
    options, args = parser.parse_args()

    if not options.username:
        sys.exit("User name not specified, see --help")

    if options.infotype == "loved":
        infotype = "lovedtracks"
    elif options.infotype == "banned":
        infotype = "bannedtracks"
    else:
        infotype = "recenttracks"
         
    return options.username, options.outfile, options.startpage, options.server, infotype

def connect_server(server, username, startpage, sleep_func=time.sleep, tracktype='recenttracks', retry_on_error=True):
    """ Connect to server and get a XML page."""
    if server == "libre.fm":
        baseurl = 'http://alpha.libre.fm/2.0/?'
        urlvars = dict(method='user.get%s' % tracktype,
                    api_key=('lastexport.py-%s' % __version__).ljust(32, '-'),
                    user=username,
                    page=startpage,
                    limit=200)

    elif server == "last.fm":
        baseurl = 'http://ws.audioscrobbler.com/2.0/?'
        urlvars = dict(method='user.get%s' % tracktype,
                    api_key='e38cc7822bd7476fe4083e36ee69748e',
                    user=username,
                    page=startpage,
                    limit=50)
    else:
        if server[:7] != 'http://':
            server = 'http://%s' % server
        baseurl = server + '/2.0/?'
        urlvars = dict(method='user.get%s' % tracktype,
                    api_key=('lastexport.py-%s' % __version__).ljust(32, '-'),
                    user=username,
                    page=startpage,
                    limit=200)

    url = baseurl + urllib.parse.urlencode(urlvars)

    for interval in (1, 5, 10, 62):
        try:
            f = urllib.request.urlopen(url)  # pylint: disable=all
            break
        except Exception as e:
            if retry_on_error:
                last_exc = e
                log.warning("Exception occured while fetching last.fm listen "
                            "history: %s. Retrying in %ds. Use --no-sync to disable "
                            "network access.", e, interval)
                sleep_func(interval)
            else:
                raise
    else:
        raise last_exc

    response = f.read()
    f.close()

    #bad hack to fix bad xml
    response = re.sub('\xef\xbf\xbe', '', response.decode())
    return response

def get_pageinfo(response, tracktype='recenttracks'):
    """Check how many pages of tracks and total tracks the user has."""
    xmlpage = ET.fromstring(response)
    totalpages = xmlpage.find(tracktype).attrib.get('totalPages')
    totaltracks = xmlpage.find(tracktype).attrib.get('total')
    return int(totalpages), int(totaltracks)

def get_tracklist(response):
    """Read XML page and get a list of tracks and their info."""
    xmlpage = ET.fromstring(response)
    tracklist = xmlpage.iter('track')
    return tracklist

def parse_track(trackelement):
    """Extract info from every track entry and output to list."""
    if list(trackelement.find('artist')):
        #artist info is nested in loved/banned tracks xml
        artistname = trackelement.find('artist').find('name').text
        artistmbid = trackelement.find('artist').find('mbid').text
    else:
        artistname = trackelement.find('artist').text
        artistmbid = trackelement.find('artist').get('mbid')

    if trackelement.find('album') is None:
        #no album info for loved/banned tracks
        albumname = ''
        albummbid = ''
    else:
        albumname = trackelement.find('album').text
        albummbid = trackelement.find('album').get('mbid')

    trackname = trackelement.find('name').text
    trackmbid = trackelement.find('mbid').text
    date = trackelement.find('date').get('uts')

    output = [date, trackname, artistname, albumname, trackmbid, artistmbid, albummbid]

    for i, v in enumerate(output):
        if v is None:
            output[i] = ''

    return output

def write_tracks(tracks, outfileobj):
    """Write tracks to an open file"""
    for fields in tracks:
        outfileobj.write(("\t".join(fields) + "\n").encode('utf-8'))

def get_tracks(server, username, startpage=1, sleep_func=time.sleep, tracktype='recenttracks', retry_on_error=True):
    page = startpage
    response = connect_server(server, username, page, sleep_func, tracktype, retry_on_error)
    totalpages, totaltracks = get_pageinfo(response, tracktype)

    if startpage > totalpages:
        raise ValueError("First page (%s) is higher than total pages (%s)." % (startpage, totalpages))

    while page <= totalpages:
        #Skip connect if on first page, already have that one stored.

        if page > startpage:
            response =  connect_server(server, username, page, sleep_func, tracktype, retry_on_error)

        tracklist = get_tracklist(response)
		
        tracks = []
        for trackelement in tracklist:
            # do not export the currently playing track.
            if not trackelement.attrib.get('nowplaying', None):
                tracks.append(parse_track(trackelement))

        yield page, totalpages, totaltracks, tracks

        page += 1
        sleep_func(.5)

def main(server, username, startpage, outfile, infotype='recenttracks'):
    trackdict = dict()
    page = startpage  # for case of exception
    totalpages = -1  # ditto
    n = 0
    try:
        for page, totalpages, tracks in get_tracks(server, username, startpage, tracktype=infotype):
            log.debug("Got page %s of %s..", page, totalpages)
            for track in tracks:
                if infotype == 'recenttracks':
                    trackdict.setdefault(track[0], track)
                else:
                    #Can not use timestamp as key for loved/banned tracks as it's not unique
                    n += 1
                    trackdict.setdefault(n, track)
    except ValueError as e:
        sys.exit(e)
    except Exception:
        raise
    finally:
        with open(outfile, 'a') as outfileobj:
            tracks = sorted(trackdict.values(), reverse=True)
            write_tracks(tracks, outfileobj)
            log.debug("Wrote page %s-%s of %s to file %s", startpage, page, totalpages, outfile)

if __name__ == "__main__":
    parser = OptionParser()
    username, outfile, startpage, server, infotype = get_options(parser)
    main(server, username, startpage, outfile, infotype)
