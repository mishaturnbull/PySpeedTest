# -*- coding: utf-8 -*-
"""
Automatically update the program if needed.
"""

import requests

__major__ = '0'
__minor__ = '4'
__patch__ = '3'
__version__ = '.'.join([__major__, __minor__, __patch__])
__int_version__ = int(''.join([__major__, __minor__, __patch__]))

def has_update():
    versions = requests.get("https://api.github.com/repos/mishaturnbull/PySpeedTest/releases")
    latest_version = versions.json()[0]['tag_name']
    latest_int_version = int(''.join(latest_version[1:].split('.')))
    return latest_int_version > __int_version__

def get_download_url():
    versions = requests.get("https://api.github.com/repos/mishaturnbull/PySpeedTest/releases")
    exe_url = versions.json()[0]['assets'][0]['browser_download_url']
    return exe_url

# this is shamefully stolen from:
# https://stackoverflow.com/a/16696317/4612410
# because no matter how I wrote it mine wouldn't work.  >:/    
def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def download_update():
    download_file(get_download_url())
