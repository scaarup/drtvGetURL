#!/usr/bin/env python
"""
Søren Christian Aarup, 2022
https://github.com/scaarup/drtvGetURL
"""
import requests, sys, re
# decrypt kindly borrowed from: https://raw.githubusercontent.com/xbmc-danish-addons/plugin.video.drnu/master/resources/lib/tvapi.py
from decrypt import *

debug=0

def dbg(msg):
    if debug == 1:
        print('DEBUG: '+str(msg))

def getMediaUrl(title):
    url = 'https://www.dr.dk/mu-online/api/1.4/page/tv/programs-search/'+title+'?orderBy=PrimaryBroadcastStartTime'
    m = requests.get(url)
    data = m.json()
    for item in data['Episodes']['Items']:
        if (item['SeriesTitle'].casefold() == title.casefold()):
            dbg('HIT: '+item['SeriesTitle']+' Published: '+item['PrimaryAsset']['StartPublish'])
            m2 = requests.get('https://www.dr.dk/mu-online/api/1.4/programcard/'+item['Urn']+'?expanded=true')
            data2 = m2.json()
            encrypted_media_uri = data2['PrimaryAsset']['Links'][0]['EncryptedUri']
            dbg(encrypted_media_uri)
            decrypted_media_uri = decrypt_uri(encrypted_media_uri)
            dbg(decrypted_media_uri)
            r = requests.get(decrypted_media_uri)
            media_uri = re.search('.+index_3.+', r.text)
            return(media_uri[0])
            break

print(getMediaUrl(sys.argv[1]))