#!/usr/bin/env python
"""
Søren Christian Aarup, 2022
https://github.com/scaarup/drtvGetURL
"""
import requests, sys, re
# decrypt kindly borrowed from: https://raw.githubusercontent.com/xbmc-danish-addons/plugin.video.drnu/41af8f6db574f2aa7a744aec15dfd3d2b5c56bc4/tvapi.py
from decrypt import *

def getMediaUrl(title):
    url = 'https://www.dr.dk/mu-online/api/1.4/search/tv/programcards-latest-episode-with-asset/series-title/'+title+'?orderBy=PrimaryBroadcastStartTime'
    m = requests.get(url)
    data = m.json()
    for item in data['Items']:
        if (item['SeasonTitle'] == title):
            m2 = requests.get('https://www.dr.dk/mu-online/api/1.4/programcard/'+item['Urn']+'?expanded=true')
            data2 = m2.json()
            encrypted_media_uri = data2['PrimaryAsset']['Links'][0]['EncryptedUri']
            decrypted_media_uri = decrypt_uri(encrypted_media_uri)
            r = requests.get(decrypted_media_uri)
            media_uri = re.search('.+index_3.+', r.text)
            return(media_uri[0])
            break

print(getMediaUrl(sys.argv[1]))