import sys, re, time
import xbmc, xbmcgui, xbmcplugin


__rtmpurl__ = 'rtmp://vegasrv1.dedicated.cohaesio.net/vod/'


def printConcerts(concerts):
	xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
	
	total = len(concerts)
	for concert in concerts:
		id = concert.getAttribute('id')
		artist = concert.getElementsByTagName('name').item(0).firstChild.data
		date = concert.getElementsByTagName('date').item(0).firstChild.data
		thumbnail = 'http://www.vega-tdc-player.dk/' + concert.getElementsByTagName('teaserimage').item(0).firstChild.data
		url = sys.argv[0] + '?concert=' + id
		
		listitem = xbmcgui.ListItem()
		listitem.setLabel(artist)
		listitem.setLabel2(date)
		if re.search('jpg$', thumbnail):
			listitem.setThumbnailImage(thumbnail)
		listitem.setInfo('video', {'date': date, 'title': artist})
		xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True, totalItems=total)

	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def printConcertInfo(concertid, concert):
	artist = concert.get('info').getElementsByTagName('name').item(0).firstChild.data
	date = concert.get('info').getElementsByTagName('date').item(0).firstChild.data
	
	xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
	
	tracks = concert.get('tracks').item(0).getElementsByTagName('track')
	trackId = 0
	total = len(tracks)
	for track in tracks:
		name = track.getElementsByTagName('name').item(0).firstChild.data
		
		url = sys.argv[0] + '?track=' + str(trackId) + '&concert=' + concertid
		
		listitem = xbmcgui.ListItem(name)
		listitem.setInfo('video', {'date': date, 'title': name, 'artist': artist})
		xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True, totalItems=total)
		
		trackId += 1
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def playTrack(trackId, concert):
	artist = concert.get('info').getElementsByTagName('name').item(0).firstChild.data
	stream = concert.get('info').getElementsByTagName('stream').item(0).firstChild.data[4:] # Removes 'flv:' from the string

	track = concert.get('tracks').item(0).getElementsByTagName('track').item(int(trackId))
	start = int(track.getAttribute('startms'))
	
	listitem = xbmcgui.ListItem(artist) # It doesn't make sense to include the track name, since it's one stream for the entire concert
	listitem.setProperty('PlayPath', stream)
	listitem.setProperty('tcUrl', __rtmpurl__)
	xbmc.Player().play(__rtmpurl__ + ' start=%d' % start, listitem)
