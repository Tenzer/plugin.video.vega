'''
	Streams concerts from www.vega-tdc-player.dk
	
	Starting a concert at a specific track does currently not work, if using the old version of librtmp, this should work with the next stable release of XBMC.
'''

from resources.lib import getter, printer


# Plugin constants
__plugin__ = 'VEGA Concerts'
__author__ = 'Tenzer'
__url__ = 'http://code.google.com/p/xbmc-addons/'
__svn_url__ = 'http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/VEGA%20Concerts'
__version__ = '1.0.0'


if(sys.argv[2].startswith('?concert=')):
	# Print the track listing for a concert
	import re
	info = re.search('\?concert=([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})', sys.argv[2])
	printer.printConcertInfo(info.group(1), getter.getConcertInfo(info.group(1)))
elif(sys.argv[2].startswith('?track=')):
	# Play a concert from the track number provided
	import re
	info = re.search('\?track=(\d+)&concert=([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})', sys.argv[2])
	printer.playTrack(info.group(1), getter.getConcertInfo(info.group(2)))
else:
	# Print the concert listing
	concerts = getter.getConcerts()
	printer.printConcerts(concerts)